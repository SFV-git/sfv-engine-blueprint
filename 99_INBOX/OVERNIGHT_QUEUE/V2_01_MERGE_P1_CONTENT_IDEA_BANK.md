---
STATUS: ACTIVE
DIRECTIVE_ID: MERGE-20260701-P1-CONTENT-IDEA-BANK-001
EXECUTOR: codex
---

Read C:\SFV_BLUEPRINT\99_INBOX\OUTPUTS\BLUEPRINT-LOOP-20260630-192506-P1-CONTENT-IDEA-BANK-001_RESULT.md — skip the executor/status header above the first "---" fence, take everything after it as DRAFT_CONTENT.

Read C:\SFV_BLUEPRINT\05_AI_LAYER\CONTENT_IDEA_BANK.md.

If that file's frontmatter STATUS is CANON: do NOT edit it. Instead write DRAFT_CONTENT to a new file C:\SFV_BLUEPRINT\FOR_HUMAN_REVIEW\content_idea_bank_overnight_draft.md with a one-line header noting it is unreviewed ollama output for Will, then stop.

Otherwise: append DRAFT_CONTENT to the end of the file under a new heading "## OVERNIGHT DRAFT — UNREVIEWED (codex merge 2026-07-01, directive MERGE-20260701-P1-CONTENT-IDEA-BANK-001)". Do not delete, reorder, or rewrite any existing content. Do not change the file's STATUS frontmatter field.

Then append exactly one new line to C:\SFV_BLUEPRINT\CHANGELOG.md under a "## 2026-07-01 — Overnight merge batch" heading (create the heading above older entries if it does not exist) stating which file was changed and this directive id.

Do not touch, create, or delete any other file. Do not touch n8n, Docker, git push, or any live service.
