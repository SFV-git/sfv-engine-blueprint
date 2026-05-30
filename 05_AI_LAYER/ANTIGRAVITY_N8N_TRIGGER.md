---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE — or merge into STACK_INTEGRATION_PLAN when CANON
---

# ANTIGRAVITY → n8n TRIGGER SPEC

> How Antigravity dispatches tasks into the n8n queue.
> Currently unwired — this doc specs the connection.

---

## CURRENT STATE

SESSION_STATE flags: "Antigravity → n8n direct trigger not wired."

Antigravity can write files and run PowerShell. n8n watches `C:\SFV_BLUEPRINT\99_INBOX\QUEUE` via Local File Trigger. These two facts are the foundation of the integration — no additional infrastructure is required for the basic path.

---

## TRIGGER METHOD — CANONICAL CHOICE: FILE DROP

Antigravity writes a valid job envelope JSON to `C:\SFV_BLUEPRINT\99_INBOX\QUEUE\`. n8n's Local File Trigger fires within ~1–2 seconds and routes the task.

**Why file drop over webhook:**
- No auth required (localhost-only, no port exposure)
- Antigravity already has file write permissions to vault
- Decoupled — Antigravity does not need to know if n8n is running
- Failed tasks persist on disk and are picked up on n8n restart
- Matches existing queue design in ENGINE_COMMUNICATION_MODEL.md

**Why not webhook:**
- Requires n8n webhook endpoint to be exposed
- Adds auth complexity
- Tight coupling — Antigravity must handle n8n downtime

---

## JOB ENVELOPE FORMAT

Antigravity must write files conforming to the canonical job envelope schema.
See `05_AI_LAYER/JOB_ENVELOPE_SPEC.md` for the full schema, required vs optional fields, and examples.

**Key rules for Antigravity dispatch:**
- `status` must be `"PENDING"` — workflow1 skips non-PENDING files
- `task_id` must be unique — use `YYYYMMDD-NNN` format
- File must be valid JSON — malformed files are silently dropped
- File extension must be `.json`
- Set `"client_facing": true` on any task that will go directly to a client

---

## ANTIGRAVITY TASK — HOW TO DISPATCH

In an Antigravity session, dispatching a task to n8n looks like:

```
Write this JSON to C:\SFV_BLUEPRINT\99_INBOX\QUEUE\[task_id].json:
{
  "task_id": "20260529-001",
  "task_type": "CLASSIFY",
  "topic": "Branch classification for new files",
  "prompt": "[prompt text]",
  "priority": "NORMAL",
  "status": "PENDING",
  "output_target": "C:/SFV_BLUEPRINT/99_INBOX/OUTPUTS/20260529-001_RESULT.md"
}
```

n8n picks it up automatically. No further action from Antigravity.

---

## CHECKING RESULTS

Antigravity can poll for completion by reading the task file:
```
Read C:\SFV_BLUEPRINT\99_INBOX\QUEUE\[task_id].json
```
When `status` changes from `"PENDING"` to `"COMPLETE"` or `"ESCALATED"`, the task is done.

Output is at `output_target` (for COMPLETE) or `HANDOFFS/[task_id]_HANDOFF.json` (for ESCALATED).

---

## WEBHOOK TRIGGER (FUTURE — Phase 2)

For time-critical tasks where Antigravity needs a synchronous response, a webhook path can be added:

```
POST http://127.0.0.1:5678/webhook/sfv-dispatch
Body: { job envelope JSON }
Response: { task_id, status, output_target }
```

**Auth:** n8n webhook nodes support header-based auth tokens. Set `X-SFV-Key` header.
**[FOR HUMAN REVIEW]:** Add webhook path only if file-drop latency (~2s) proves insufficient for Antigravity use cases. Not blocking Phase 1.

---

## PRIORITY HANDLING

The `priority` field in the job envelope is written and logged but not currently enforced by workflow1 — all tasks run in FIFO order as files arrive.

Priority enforcement is documented in CONCURRENCY_QUEUE_SPEC.md (Gap 16) and requires Redis queue mode.

For now: use `priority` as metadata only. HIGH/CRITICAL tasks can be manually moved to the front by renaming them with an earlier timestamp prefix.

---

## CONNECTED FILES
- [[ENGINE_COMMUNICATION_MODEL|Engine Communication Model]]
- [[STACK_INTEGRATION_PLAN|Stack Integration Plan]]
- [[ANTIGRAVITY_RULES|Antigravity Rules]]
- [[AI_STACK_ARCHITECTURE_BLUEPRINT|AI Stack Architecture]]
- [[CONCURRENCY_QUEUE_SPEC|Concurrency and Queue Mode]]
- [[workflow1_queue_processor|Workflow 1 JSON]]
