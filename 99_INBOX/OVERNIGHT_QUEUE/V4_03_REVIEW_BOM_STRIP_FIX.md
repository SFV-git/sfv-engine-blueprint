---
STATUS: ACTIVE
DIRECTIVE_ID: REVIEW-20260701-BOM-STRIP-FIX-001
EXECUTOR: claude_code
---

This is a code review task, NOT a build task. Read C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\n8n_workflows\workflow1_queue_processor.json and find the "Read Task" Code node — it should have had BOM-stripping logic added earlier tonight (unsupervised codex run). Verify: is the fix actually present, is it syntactically valid JavaScript, does it correctly handle both BOM and non-BOM input without breaking normal parsing, and is the rest of the JSON file still valid (no corruption from the edit)? Write a verdict — CLEAN or NEEDS_FIXES with specifics — to a NEW file C:\SFV_BLUEPRINT\FOR_HUMAN_REVIEW\REVIEW_bom_strip_fix.md. This file is NOT live (it's a vault copy, not the running n8n DB) so this is a pure correctness check, no urgency. Do NOT modify the JSON file itself. Do not touch n8n, Docker, git push, or any live service.
