---
STATUS: ACTIVE
DIRECTIVE_ID: REVIEW-20260701-MERGE-REVIEWER-001
EXECUTOR: claude_code
---

This is a code review task, NOT a build task. Read C:\SFV_BLUEPRINT\99_INBOX\merge_reviewer.py (written earlier tonight by an unsupervised codex run). Check it for: bugs, unsafe file operations, path traversal risk, whether it could accidentally modify a scanned file instead of only reading it, or anything that could touch n8n/Docker/git. Write a verdict — CLEAN or NEEDS_FIXES with specific line-level notes — to a NEW file C:\SFV_BLUEPRINT\FOR_HUMAN_REVIEW\REVIEW_merge_reviewer.md. Do NOT modify merge_reviewer.py itself, even if you find issues — flag only. Do not touch any other file. Do not touch n8n, Docker, git push, or any live service.
