---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# SFV ENGINE — DASHBOARD

> Open this every session. It tells you what needs you.

---

## NEEDS YOUR ATTENTION

```dataview
LIST
FROM "FOR_HUMAN_REVIEW"
WHERE file.name != "PROPOSALS"
SORT file.mtime DESC
```

## UNCONFIRMED ITEMS

```dataview
LIST file.path
FROM ""
WHERE STATUS = "UNCONFIRMED"
SORT file.name ASC
```

## OPEN QUESTIONS
![[QUESTIONS_FOR_WILL]]

## RECENT CHANGES

```dataview
TABLE file.mtime AS "Modified"
FROM ""
WHERE file.mtime >= date(today) - dur(3 days)
SORT file.mtime DESC
LIMIT 10
```

## CRITICAL DEADLINES
- 🔴 May 28 (Thursday) — Morning Walk, 50+ models, Studio pipeline
- 🟡 June 6 — Shamar Tournament, Live pipeline
- 🟢 This week — Brandon Bellotti visit, first UGC client

## CURRENT BUILD PHASE
v0.x — Blueprint Foundation

## WHAT NEEDS WORK
1. 04_WORKFLOWS/INGEST.md — needs full detail before Thursday
2. 08_TESTS/PAPER_TRIAL_RUNS.md — Morning Walk walk-through
3. Scheduling tool decision (Later vs Buffer)
4. 04_WORKFLOWS/DELIVERY.md — Pixieset setup detail

## SESSION START PROTOCOL
Claude reads SESSION_STATE.md + this file + QUESTIONS_FOR_WILL.md
Reports in 3 lines. Waits for Will.

## CONNECTED FILES
- [[QUESTIONS_FOR_WILL|Questions for Will]]
- [[INGEST|Ingest Workflow]]
- [[PAPER_TRIAL_RUNS|Paper Trial Runs]]
- [[DELIVERY|Delivery Workflow]]
- [[SESSION_STATE|Session State]]
- [[SFV_STUDIO|SFV Studio]]
- [[SFV_LIVE|SFV Live]]
- [[SFV_UGC|SFV UGC]]
- [[CHAT_EXTRACTS|Chat Extracts]]
- [[DECISION_LOG|Decision Log]]
- [[OLLAMA_RESULTS|Ollama Results]]
- [[RAW_IDEAS|Raw Ideas]]
- [[SCRATCHPAD|Scratchpad]]
- [[TASK_QUEUE|Task Queue]]
- [[TEMPLATE_DEFAULT|Template Default]]
- [[TO_REVIEW|To Review]]
