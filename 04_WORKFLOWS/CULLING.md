---
STATUS: UNCONFIRMED
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# CULLING WORKFLOW

## PURPOSE
Reduce raw file count to selects only.
AI handles technical culling. Will handles creative culling.

## FLOW
```
[BRANCH]/INGEST/ files
→ blur detection (local model, R&D terminal)
→ exposure flagging (local model, R&D terminal)
→ duplicate grouping (Python script)
→ auto-rejects moved to [BRANCH]/REJECTS/
→ remaining files moved to [BRANCH]/REVIEW/
→ Will reviews and makes final selects
→ selects moved to [BRANCH]/SELECTS/
→ cull log written
```

## TOOLS
- Local model on R&D terminal: blur detection, exposure flagging
- Python: duplicate grouping, file movement
- Human: final creative selects (always)

## NOTES
- AI never makes final creative selections
- Auto-rejects are flagged, never permanently deleted until Will confirms
- Duplicate grouping shows groups for Will to pick best from

## CONNECTED FILES
- [[05_AI_LAYER/RD_TERMINAL_ARCHITECTURE|RD Terminal Architecture]]
- [[03_INFRASTRUCTURE/MULTI_AGENT_WORKFLOW|Multi-Agent Workflow]]
- [[02_BRANCHES/BRANCH_OUTPUTS|Branch Outputs]]
- [[00_DEV_LOG/DECISIONS|Decisions]]
- [[00_DEV_LOG/PENDING_REVIEW|Pending Review]]
