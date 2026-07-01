---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-25
---

# ENGINE COMMUNICATION MODEL

> Agents and tools do not talk to each other directly. They communicate by writing and reading structured files.
> Will does not jump between agents manually. The queue routes the work.

---

## CORE PRINCIPLE

```
Will request
  → TASK_QUEUE (structured file)
  → cheapest capable layer picks it up
  → writes output to OUTPUTS folder
  → review layer if needed
  → canon update ONLY after Will approves
```

No agent edits canon directly. No agent assumes approval. All handoffs are file-based.

---

## FOLDER STRUCTURE

```
C:\SFV_BLUEPRINT\
  99_INBOX\
    QUEUE\                ← LIVE production queue — job envelope JSONs, n8n workflow1 trigger
    QUEUE\DONE\           ← processed task files (archival)
    TASK_QUEUE.md         ← LEGACY task list (standalone Ollama daemon only)
    OLLAMA_RESULTS.md     ← Ollama writes output here
    OUTPUTS\              ← all agent output files land here
    HANDOFFS\             ← structured handoff notes between agents
    DECISION_LOG.md       ← log of routing decisions made
    QUESTIONS_FOR_WILL.md ← questions that blocked execution (see also 00_DEV_LOG)
  FOR_HUMAN_REVIEW\
    PROPOSALS.md          ← anything requiring Will's approval before canon
```

---

## FILE DEFINITIONS

### TASK_QUEUE.md (LEGACY — Ollama daemon path)
- LEGACY as of 2026-05-29: the live production queue is `99_INBOX\QUEUE\*.json` processed by n8n workflow1. See JOB_ENVELOPE_SPEC.md.
- TASK_QUEUE.md remains valid only for the standalone ollama_daemon.py loop (manual/ad-hoc use)
- One task per section, separated by `---`
- Required fields: ID, DATE, ASSIGNED_TO, PRIORITY, STATUS, PROMPT, OUTPUT_TARGET
- Status values: PENDING | IN_PROGRESS | COMPLETE | BLOCKED | CANCELLED
- Ollama polls this file on daemon cycle
- Claude and Antigravity can also read and pick up tasks

### OLLAMA_RESULTS.md
- Ollama writes all output here
- Format: task ID, timestamp, model used, raw output
- Do not treat as canon — treat as draft for review

### OUTPUTS\
- Named: `YYYYMMDD-###_DESCRIPTION_TOOL.md` or `.json`
- Any agent can write here
- Nothing in OUTPUTS is canon until reviewed and approved

### HANDOFFS\
- Named: `YYYYMMDD-###_FROM_TO_TOPIC.md`
- Format: summary of what was done, what is needed next, which tool should receive it
- Example: Ollama → Claude handoff with compressed context

### DECISION_LOG.md
- Log of every routing decision: what came in, what layer handled it, why
- Written by whichever layer handled the task
- Used by Antigravity for audits

### QUESTIONS_FOR_WILL.md (00_DEV_LOG version)
- Anything that blocked execution gets logged here
- Format: question, blocking task ID, date
- Claude session reads this at start

---

## AGENT ASSIGNMENT RULES

| Task Type | Assigned To |
|-----------|------------|
| Current web research | Perplexity |
| Repeatable triggered workflow | n8n |
| Summary, classification, routing draft | Ollama |
| Architecture, blueprint, complex code | Claude |
| System audit, orchestration, codebase review | Antigravity |
| Anything n8n/PowerShell/Python can do alone | No AI |

---

## STATUS TAGS (use in all files)

| Tag | Meaning |
|-----|---------|
| CANON | Approved by Will, locked |
| UNCONFIRMED | Not yet verified — do not act on |
| INFERENCE | Derived from context — needs Will confirmation |
| FOR HUMAN REVIEW | Requires Will approval before canon |
| PENDING | In queue, not started |
| IN_PROGRESS | Being worked |
| COMPLETE | Done, output written |
| ESCALATED | Sent to HANDOFFS/ — requires Claude or Antigravity review |
| DEFERRED | Intentionally postponed — do not process yet |
| BLOCKED | Cannot proceed — question logged |
| DRAFT | Output written, not reviewed |

---

## TOKEN OPTIMIZATION ROUTING

Cheapest capable layer always gets the task first.

```
Cost order (cheapest → most expensive):
  PowerShell / Python / n8n (free)
  → Ollama local (free)
  → Antigravity on Gemini Flash (free during preview — default model MUST be Gemini Flash)
  → Perplexity (subscription, fixed cost)
  → Claude Sonnet (per token)
  → Claude Opus (per token, highest — Will-request only)
```

Rule: If a cheaper layer can produce a 70%+ quality result, use it.
Escalate only when quality threshold is not met or task requires judgment.

---

## PERPLEXITY INTEGRATION FLOW

```
Will or Claude identifies research need
  → Create task file in 99_INBOX\TASK_QUEUE.md (ASSIGNED_TO: PERPLEXITY)
  → Run Perplexity with structured prompt
  → Save output to OUTPUTS\YYYYMMDD-###_PERPLEXITY_TOPIC.md
  → Claude or Antigravity reviews
  → Approved findings move to relevant blueprint doc or Obsidian note
  → Canon only after Will approves
```

---

## OLLAMA TASK LOOP — FIRST TEST DESIGN

Goal: Prove Ollama can read a task, process it, and write an output. No production media.

```
Step 1: Write one test task to TASK_QUEUE.md
Step 2: Ollama daemon reads task on next cycle
Step 3: Ollama processes with local model
Step 4: Ollama writes result to OLLAMA_RESULTS.md and OUTPUTS\
Step 5: Log status to DECISION_LOG.md
Step 6: Claude reviews output quality
```

Test prompt: "Read this task. Classify which SFV branch it belongs to. Output: branch name, confidence, reason."

---

## WHAT THIS REPLACES
Previously: Will manually coordinated between agents.
Now: Will puts a request in the queue. The system routes it, processes it, and surfaces output for review.
Will's role is direction and approval — not agent-jumping.

## CONNECTED FILES
- [[JOB_ENVELOPE_SPEC|Job Envelope Specification]]
- [[ANTIGRAVITY|Antigravity System]]
- [[OUTPUT_VALIDATION|Output Validation Protocol]]
- [[TOOL_STACK|Tool Stack Configuration]]
- [[OLLAMA_SETUP|Ollama Setup Guide]]
- [[QUESTIONS_FOR_WILL|Questions for Will Log]]
