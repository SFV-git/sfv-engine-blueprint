---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-06-09
CREATED_BY: Claude Chat
MERGE_INTO: STANDALONE or ENGINE_COMMUNICATION_MODEL
---

# OUTPUTS RETENTION POLICY

> Defines what lives in 99_INBOX/OUTPUTS/, what gets pruned, and when.
> Without this, OUTPUTS/ accumulates indefinitely and becomes noise.

---

## CURRENT STATE (problem)

As of 2026-06-09, OUTPUTS/ contains:
- Triplicate test artifacts from 2026-05-28 batch runs (same content, different timestamps)
- Validated test results (TEST_CLASSIFY_002, TEST_CODE_004, etc.) — keepers
- One legitimate audit output (20260525-002_INGEST_WASTE_AUDIT)
- README.md

No retention rule exists. No pruning has ever run.

---

## PROPOSED RULES

### Rule 1 — Test artifacts expire in 14 days
Files matching `TEST_*` or `*_TEST_*` in OUTPUTS/ older than 14 days are safe to delete.
They exist only to confirm the pipeline works — once confirmed, they have no long-term value.

### Rule 2 — VALIDATED outputs move to QUEUE/DONE/ at 30 days
OUTPUTS/ files with status VALIDATED and age > 30 days move to QUEUE/DONE/ for cold archival.
They are not deleted — just out of the active review path.

### Rule 3 — FLAGGED outputs stay until Will resolves them
No automated pruning of FLAGGED files. Will clears them manually after review.

### Rule 4 — DRAFT outputs expire in 7 days if not promoted
A DRAFT that sits for 7 days without becoming VALIDATED or FLAGGED is stale — something in the
pipeline failed to run the validation pass. These get tagged STALE and surfaced to Will.

### Rule 5 — Triplicate/duplicate outputs
If two or more files share the same task_id prefix, keep the newest, delete the rest.
Cause: multiple n8n re-runs without cleanup. The newest is authoritative.

---

## IMMEDIATE CLEANUP (safe to run now)

The following files in OUTPUTS/ are safe to delete — they are triplicate test artifacts
from 2026-05-28 import debugging where the same tasks ran 4+ times:

```
202605280629197_20260525-001_PERPLEXITY_N8N_INGEST_RESEARCH.md
202605280629197_20260525-TEST-001_OLLAMA_BRANCH_CLASSIFY.md
202605280629197_test_001.md
202605280629572_20260525-001_PERPLEXITY_N8N_INGEST_RESEARCH.md
202605280629572_20260525-TEST-001_OLLAMA_BRANCH_CLASSIFY.md
202605280629572_test_001.md
202605280630043_20260525-001_PERPLEXITY_N8N_INGEST_RESEARCH.md
202605280630043_20260525-TEST-001_OLLAMA_BRANCH_CLASSIFY.md
202605280630043_test_001.md
202605280630088_20260525-001_PERPLEXITY_N8N_INGEST_RESEARCH.md
202605280630088_20260525-TEST-001_OLLAMA_BRANCH_CLASSIFY.md
202605280630088_test_001.md
20260525-TEST-001_OLLAMA_BRANCH_CLASSIFY.md   (superseded by timestamped versions)
```

Keep:
- 20260525-002_INGEST_WASTE_AUDIT.md
- CLASSIFY-TEST-002_RESULT.md
- CODE-TEST-004_RESULT.md
- TEST_CLASSIFY_002_RESULT.md
- TEST_CODE_004_RESULT.md
- TEST_VALIDATION_001_RESULT.md
- VISION-TEST-002_RESULT.md
- README.md

[FOR HUMAN REVIEW]: Approve cleanup of the 13 triplicate files listed above?

---

## CONNECTED FILES
- [[ENGINE_COMMUNICATION_MODEL|ENGINE COMMUNICATION MODEL]]
- [[FAILURE_TESTS|FAILURE TESTS]]
- [[EDGE_CASES|EDGE CASES]]
- [[CURRENT_DIRECTIVE|CURRENT DIRECTIVE]]
