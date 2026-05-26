---
STATUS: FOR HUMAN REVIEW
DATE: 2026-05-25
AUDITOR: CLAUDE
CANON_FILE: 04_WORKFLOWS/INGEST.md
---

# INGEST.md — WASTE AUDIT (n8n-first logic)

> No rewrites. Flags only. Will approves before anything changes.

---

## FINDINGS

### 1. CLAUDE IS NOT IN THIS WORKFLOW — GOOD
INGEST.md as written does not call Claude at any step. That is correct.
Steps 1-8 are all Python stdlib. No AI cost in the happy path.
No flags here.

### 2. STEPS THAT N8N COULD OWN INSTEAD OF PYTHON

| Step | Current | n8n Alternative | Verdict |
|------|---------|-----------------|---------|
| Step 1 — File watcher / staging trigger | Manual or Python | n8n file watcher node → trigger on E:\ connect or new files in staging | n8n is better here |
| Step 7 — Log write | Python writes .txt | n8n can write log and send desktop notification | n8n handles this cleanly |
| Step 8 — Notify | Terminal print only | n8n → Windows toast via webhook or local HTTP call | n8n is better here |
| Repeat ingest for multiple branches | Will runs script twice manually | n8n multi-branch trigger loop | Worth evaluating |

**Recommendation (FOR HUMAN REVIEW):** Step 1 trigger and Step 8 notify are strong n8n candidates. Steps 2-6 (copy, checksum, rename, dedup, move) stay in Python — n8n is not suited for file-level checksum logic.

---

### 3. HARDCODED PATH VIOLATIONS

The following paths appear in INGEST.md and may violate the no-hardcode rule (all paths should come from ENVIRONMENT_CONFIG.md):

| Location in doc | Hardcoded path | Risk |
|----------------|---------------|------|
| STEP 1 target | `D:\SFV_ACTIVE\INGEST_STAGING\` | MEDIUM — should be env var |
| STEP 6 target | `D:\SFV_ACTIVE\BRANCHES\[BRANCH]\INGEST\` | MEDIUM — should be env var |
| QUARANTINE path | `D:\SFV_ACTIVE\FOR_HUMAN_REVIEW\QUARANTINE\` | MEDIUM — should be env var |
| Morning Walk step 7 | `D:\SFV_ACTIVE\BRANCHES\SFV_STUDIO\INGEST\20260528\` | HIGH — date hardcoded |
| Script path | `C:\SFV_BLUEPRINT\99_INBOX\ingest.py` | LOW — vault path is locked |
| Log path | `D:\SFV_ACTIVE\BRANCHES\SFV_STUDIO\LOGS\INGEST_LOG_20260528.txt` | HIGH — date hardcoded |

**Verdict:** The script spec section (arguments/output/log format) is illustrative, not production code — hardcoded dates there are acceptable as examples. But the workflow steps themselves reference hardcoded D:\ paths. ingest.py should load all base paths from ENVIRONMENT_CONFIG.md, not hardcode them.

INFERENCE: ingest.py v2 (already written) may already handle this via config loader. Needs verification before flagging as a real bug.

---

### 4. GOOGLE DRIVE MANUAL STEP — CANNOT BE AUTOMATED CHEAPLY

Step: "Download Google Drive folder → drag to staging"

This step is manual by design. No automation flag needed unless Will wants to set up a Google Drive watch in n8n (possible but adds complexity). Leave manual for now.

---

### 5. BRANCH DETECTION IS A REAL GAP

Step 3 says: "Auto-detect from folder structure or filename if possible. Unknown branch → FOR_HUMAN_REVIEW."

The v1 spec requires `--branch` as a required argument — meaning auto-detection is not implemented. For multi-shooter Morning Walk scenarios, this means Will must run the script multiple times with different `--branch` flags.

INFERENCE: Ollama could handle lightweight branch classification from filename patterns after ingest. This would be a Tier 5 task: free, local, no Claude cost.

FOR HUMAN REVIEW: Should Ollama be added as a post-ingest branch classifier for unknown files?

---

### 6. NO DUPLICATE CHECK ACROSS BRANCHES

Current dedup: compares against the destination branch folder only.
Risk: If a file was already ingested to SFV_STUDIO and someone tries to ingest it to SFV_EVENTS, it would not be caught.

UNCONFIRMED: Whether cross-branch dedup is a real requirement for Will's workflow. Flag for discussion.

---

### 7. FUTURE ENHANCEMENTS SECTION — OLLAMA BLUR CHECK

"Blur/exposure pre-check via Ollama immediately post-ingest" is listed as a future enhancement. This is consistent with the communication model. No action needed now.

---

## SUMMARY

| Issue | Severity | Action |
|-------|---------|--------|
| n8n for file watcher trigger | LOW | FOR HUMAN REVIEW — easy win |
| n8n for notify step | LOW | FOR HUMAN REVIEW — easy win |
| Hardcoded paths in workflow steps | MEDIUM | Verify ingest.py config loader covers this |
| Branch auto-detection gap | MEDIUM | FOR HUMAN REVIEW — Ollama post-ingest classifier? |
| Cross-branch dedup missing | LOW | UNCONFIRMED requirement |
| Google Drive manual step | NONE | Leave manual |
| Claude usage in ingest | NONE — Claude not used | No issue |

**INGEST.md is not over-engineered. The core pipeline is clean. Main risks are path hardcoding in the spec examples and missing n8n triggers at edges.**
