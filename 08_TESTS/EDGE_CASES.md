---
STATUS: UNCONFIRMED
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# EDGE CASES

Unusual situations the Engine needs to handle gracefully.

---

## CONTENT EDGE CASES
- Photo could belong to multiple branches → FOR HUMAN REVIEW flag
- Duplicate file with different names → flag both, Will decides
- File from another shooter (Google Drive intake) → separate intake flow
- Video and photo from same event on different cards → link by event ID

## STUDIO EDGE CASES
- 50+ model shoot: timestamp grouping to identify 3-shot sets per model
- Model appears in multiple sets (re-shoots) → manual review
- Wrong backdrop in some shots → flag for review

## DELIVERY EDGE CASES
- Client disputes delivered files → QC log is the record
- Pixieset link expires before all models claim → regenerate link

## SCALING EDGE CASES
- Operator shoots content that doesn't meet SFV standards → QC rejects, operator retakes
- Two operators shoot same event independently → merge into one project folder, deduplicate

## TECHNICAL EDGE CASES
- File system on Porsche SSD still broken → Engine routes around it, flags for fix
- Drive nearly full during ingest → warning at 85%, stop at 95%

## CONNECTED FILES
- [[04_WORKFLOWS/DELIVERY|Delivery Workflow]]
- [[05_AI_LAYER/QUALITY_CONTROL|Quality Control]]
- [[04_WORKFLOWS/INGEST|Ingest Workflow]]
- [[07_SCALING/BRANCH_INDEPENDENCE|Branch Independence]]
- [[00_DEV_LOG/PENDING_REVIEW|Pending Review]]
- [[03_INFRASTRUCTURE/STORAGE_ARCHITECTURE|Storage Architecture]]
- [[FOR_HUMAN_REVIEW/PROPOSALS|Proposals]]
