---
STATUS: ACTIVE
DIRECTIVE_ID: REVIEW-20260701-QUEUE-DASHBOARD-001
EXECUTOR: claude_code
---

This is a code review task, NOT a build task. Read C:\SFV_BLUEPRINT\99_INBOX\queue_dashboard.py (written earlier tonight by an unsupervised codex run). Check it for: bugs, unsafe file operations, path traversal risk, anything that could touch a file outside C:\SFV_BLUEPRINT, or anything that could touch n8n/Docker/git. Write a verdict — CLEAN or NEEDS_FIXES with specific line-level notes — to a NEW file C:\SFV_BLUEPRINT\FOR_HUMAN_REVIEW\REVIEW_queue_dashboard.md. Do NOT modify queue_dashboard.py itself, even if you find issues — flag only. Do not touch any other file. Do not touch n8n, Docker, git push, or any live service.
