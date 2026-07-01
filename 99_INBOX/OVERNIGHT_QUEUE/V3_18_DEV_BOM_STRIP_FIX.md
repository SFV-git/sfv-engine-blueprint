---
STATUS: ACTIVE
DIRECTIVE_ID: DEV-20260701-BOM-STRIP-FIX-001
EXECUTOR: codex
---

Read C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\n8n_workflows\workflow1_queue_processor.json (a vault copy of an n8n workflow, NOT the live n8n database). Find the "Read Task" Code node. It currently does not strip a UTF-8 BOM before JSON.parse, which is a known bug (files written with a BOM cause silent task drops — flagged in 00_DEV_LOG/HANDOFF_2026-06-27.md). Add BOM-stripping logic (e.g. content.replace(/^\uFEFF/, '') before JSON.parse) to that node's code in the JSON file. Save the file. Do NOT touch the live n8n instance, do NOT restart n8n, do NOT re-import anything. This is a file-only fix for Will to review and manually re-import later. Append one line to C:\SFV_BLUEPRINT\CHANGELOG.md under the "## 2026-07-01 — Overnight merge batch" heading noting this fix and that it is NOT yet live. Do not touch any other file, n8n, Docker, or git push.
