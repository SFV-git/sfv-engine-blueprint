---
STATUS: ACTIVE
DIRECTIVE_ID: REVIEW-20260701-UGC-SCAFFOLD-001
EXECUTOR: claude_code
---

This is a code review task, NOT a build task. Read everything under C:\SFV_BLUEPRINT\99_INBOX\PROTOTYPES\ugc_pre_production\ (written earlier tonight by an unsupervised codex run — an HTML/JS client intake form prototype). Check it for: XSS/injection risk if this were ever exposed publicly, whether it correctly matches the field list in 04_WORKFLOWS/UGC_PRE_PRODUCTION.md, obvious bugs, and general code quality. Write a verdict — CLEAN or NEEDS_FIXES with specifics — to a NEW file C:\SFV_BLUEPRINT\FOR_HUMAN_REVIEW\REVIEW_ugc_scaffold.md. Do NOT modify anything inside the prototype folder. Do not touch any other file. Do not touch n8n, Docker, git push, or any live service.
