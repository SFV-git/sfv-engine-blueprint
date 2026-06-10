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
- ✅ May 28 — Morning Walk (COMPLETE)
- ✅ June 6 — Shamar Tournament (COMPLETE)
- No hard deadlines currently — Blueprint Lock phase, correctness over delivery

## CURRENT BUILD PHASE
v0.x — Blueprint Lock COMPLETE. Execution prerequisites pending Will.

## WHAT NEEDS WORK
1. PostgreSQL migration (Will supervises — backup SQLite first)
2. Docker install on Engine Body (needs restart)
3. R&D Terminal reinstalls: Ollama → Syncthing → Claude Code → windows_exporter
4. Review remaining FOR HUMAN REVIEW docs (see PROPOSALS.md 2026-06-09 entry)
5. backup_n8n.ps1 — n8n DB has ZERO backup (DR critical gap)

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
