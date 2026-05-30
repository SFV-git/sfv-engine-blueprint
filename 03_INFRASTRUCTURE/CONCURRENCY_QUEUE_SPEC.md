---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: AI_STACK_ARCHITECTURE_BLUEPRINT §4 when CANON
---

# CONCURRENCY AND QUEUE SPEC — SFV n8n TASK PIPELINE

> Covers PRIORITY field enforcement, max-concurrent task limits by task_type, Redis queue mode (FUTURE), and the Phase 1 implementation path without Redis.
> Values marked [INFERENCE] — Will confirms before implementation.

---

## SECTION 1 — CURRENT STATE

The n8n task pipeline currently operates as a single-threaded FIFO queue.

- Tasks are processed one at a time in arrival order.
- No concurrency control is implemented.
- The PRIORITY field exists in the job envelope schema but has no enforcement logic.
- No max-concurrent task limit is documented for any task_type.

**Result:** Every task waits in line regardless of urgency or resource profile.

---

## SECTION 2 — WHY THIS IS A PROBLEM

As queue volume grows, the current architecture creates two compounding failure modes:

**Problem 1 — Priority inversion.**
A HIGH priority editorial task (CLASSIFY, SUMMARIZE) waits behind a backlog of bulk NORMAL jobs. There is no mechanism to advance urgent tasks without manual n8n intervention.

**Problem 2 — Resource blocking.**
A single slow MEDIA task (Whisper transcription on a long video) holds the FIFO position and blocks all subsequent tasks — including lightweight CODE or CLASSIFY jobs that could complete in seconds. One heavy job can stall the entire queue.

**Impact:** Both problems get worse as the Engine scales. Neither requires Redis to fix — PRIORITY enforcement can be implemented with the current file-based queue.

---

## SECTION 3 — PRIORITY FIELD ENFORCEMENT SPEC

The job envelope already contains a PRIORITY field with three valid values: `NORMAL | HIGH | CRITICAL`.

### 3.1 Proposed enforcement rules

| Priority | Behavior |
|---|---|
| CRITICAL | Process immediately. n8n reads the full PENDING list, selects CRITICAL tasks first, regardless of arrival time. |
| HIGH | Move to front of queue after any currently IN_PROGRESS task completes. Does not interrupt an active execution. |
| NORMAL | Standard FIFO. Process in arrival order after all CRITICAL and HIGH tasks are cleared. |

### 3.2 How to implement in n8n (no Redis required)

At the start of workflow1's pickup loop:

1. Read all files in the PENDING queue directory.
2. Parse the PRIORITY field from each task JSON.
3. Sort by: CRITICAL first → HIGH second → NORMAL third → within each tier, sort by `CREATED_AT` ascending (FIFO within tier).
4. Pick the first task from the sorted list.
5. Write `status: IN_PROGRESS` to the task file immediately on pickup (see Section 6).

This logic runs entirely in n8n using a Function node or a Set node with expression sorting. No external broker required.

> [FOR HUMAN REVIEW] — n8n does not have a native priority queue node. The sort must be implemented in a Code/Function node. Confirm approach before building.

---

## SECTION 4 — MAX-CONCURRENT TASK LIMITS BY TASK_TYPE

> [INFERENCE] — All values below are proposed defaults based on hardware profile and API rate limits.
> Will confirms exact numbers before these limits are enforced.

| task_type | Max concurrent | Reason |
|---|---|---|
| MEDIA (Whisper) | 1 | OOM risk on RTX 3060 — Whisper loads full model into VRAM; two simultaneous jobs will crash |
| VISION (minicpm-v) | 2 | VRAM limit on RTX 5080 — two concurrent vision jobs is the estimated safe ceiling |
| CODE | 4 | CPU-bound, no GPU dependency — safe to parallelize on Ryzen 9 9900X |
| CLASSIFY | 4 | CPU-bound, lightweight Ollama inference — high throughput safe |
| SUMMARIZE | 4 | Same profile as CLASSIFY |
| RESEARCH | 2 | API rate limit consideration — Tavily and Perplexity have RPM constraints |
| GEMINI | 3 | Gemini Flash RPM limit — three concurrent calls is the estimated safe ceiling before rate errors appear |

> [INFERENCE] — VISION max of 2 assumes RTX 5080 with sufficient VRAM headroom. Reduce to 1 if memory pressure is observed. Confirm after first production run.

### 4.1 How to enforce concurrency limits

Before starting a new task of type X:
1. Count all tasks with `status: IN_PROGRESS` and `task_type: X` in the queue directory.
2. If count >= max_concurrent[X], do not pick up a new task of that type this cycle.
3. Pick the next eligible task of a different type instead.
4. Re-evaluate on the next polling interval.

This can be implemented in the same Function node as the PRIORITY sort (Section 3.2).

---

## SECTION 5 — REDIS QUEUE MODE (FUTURE)

> STATUS: FUTURE. Do not implement until PostgreSQL migration is stable.
> Pre-requisite: POSTGRES_MIGRATION.md must reach STATUS: CANON and be deployed.

### 5.1 What Redis queue mode changes

In the current architecture, n8n runs a single process that handles both the editor UI and all workflow executions. Under load, executions can starve the editor.

Redis queue mode separates these concerns:
- n8n editor process: serves the UI, handles webhook triggers, writes jobs to Redis queue
- n8n worker processes: pull jobs from the Redis queue and execute them independently
- Multiple workers can run in parallel, each processing different jobs

### 5.2 Configuration

```
N8N_EXECUTIONS_MODE=queue
QUEUE_BULL_REDIS_HOST=127.0.0.1
QUEUE_BULL_REDIS_PORT=6379
```

Redis runs as a Docker container on Node A alongside PostgreSQL.

### 5.3 What this enables

- Horizontal scaling: add worker containers when queue depth grows
- Editor remains responsive during heavy batch execution
- Clean separation of scheduling logic from execution logic
- Foundation for future multi-node execution (Node B workers pulling from Node A queue)

### 5.4 Pre-requisites (in order)

1. PostgreSQL must be live and n8n configured to use it (SQLite is incompatible with queue mode)
2. Docker must be installed on Node A (see DOCKER_INSTALL_CHECKLIST.md)
3. Redis container deployed and reachable on localhost:6379
4. n8n restarted with `N8N_EXECUTIONS_MODE=queue` and Redis connection env vars set
5. At least one n8n worker process launched alongside the main process

> [FOR HUMAN REVIEW] — Redis queue mode changes how n8n handles all executions. Test in a non-production n8n instance before switching. Confirm timing with Will.

### 5.5 When to implement

After PostgreSQL migration is stable (defined as: n8n running on PostgreSQL for 7+ days with no data integrity issues) AND queue volume justifies it (defined as: queue consistently hitting >20 pending tasks OR editor UI lag becomes noticeable during batch runs).

---

## SECTION 6 — PHASE 1 IMPLEMENTATION PATH (NO REDIS)

Phase 1 delivers meaningful concurrency control using only the existing n8n + file-based queue setup.

### 6.1 Changes to workflow1

**Step 1: Immediate status write on pickup.**
When workflow1 picks up a task, the first node writes `status: IN_PROGRESS` and a `picked_up_at` timestamp to the task JSON file before any execution begins. This prevents duplicate processing if n8n restarts mid-job.

```json
{
  "status": "IN_PROGRESS",
  "picked_up_at": "2026-05-29T14:32:00Z"
}
```

**Step 2: Concurrency check before pickup.**
Before picking a task, workflow1 counts IN_PROGRESS tasks of the same type. If at the max-concurrent limit, skip and check for a task of a different type.

**Step 3: Priority sort on PENDING list.**
Before any pickup, sort PENDING tasks by PRIORITY (CRITICAL → HIGH → NORMAL), then by `created_at` within each tier.

### 6.2 What Phase 1 does NOT solve

- Does not enable true parallel execution within n8n (n8n is still single-threaded per execution)
- Does not prevent queue starvation if CRITICAL tasks arrive continuously
- Does not give MEDIA tasks their own isolated worker — they still block during execution

These are Redis queue mode concerns. Phase 1 improves ordering and prevents the worst blocking scenarios without requiring infrastructure changes.

---

## SECTION 7 — SQLITE LOCKING NOTE

> Existing constraint from AI_STACK_ARCHITECTURE_BLUEPRINT.md.

SQLite corrupts under parallel webhook hits. This is a separate issue from queue concurrency but is related: any Phase 1 changes that increase parallel n8n activity (multiple workflow instances) will accelerate the SQLite corruption risk.

PostgreSQL migration must be completed before Phase 1 concurrency changes are deployed at any meaningful scale. Running Phase 1 on SQLite with light volume is acceptable for testing only.

---

## CONNECTED FILES
- [[AI_STACK_ARCHITECTURE_BLUEPRINT|AI Stack Architecture Blueprint]]
- [[POSTGRES_MIGRATION|PostgreSQL Migration]]
- [[FAILOVER_MODEL|Failover Model]]
- [[MEDIA_PIPELINE|Media Pipeline]]
- [[ENGINE_COMMUNICATION_MODEL|Engine Communication Model]]
