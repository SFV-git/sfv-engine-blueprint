---
STATUS: ACTIVE
DIRECTIVE_ID: DEV-20260701-MERGE-REVIEWER-001
EXECUTOR: codex
---

Write a new python script C:\SFV_BLUEPRINT\99_INBOX\merge_reviewer.py that recursively searches all .md files under C:\SFV_BLUEPRINT\ (excluding .git, .obsidian, .smart-env) for the exact heading text "OVERNIGHT DRAFT — UNREVIEWED", and writes a list of every file + line number it appears in to C:\SFV_BLUEPRINT\99_INBOX\REVIEW_QUEUE.md, so Will can quickly find every unreviewed overnight merge in one place. Run the script once to generate the file. Do not modify any of the files being scanned. Do not touch n8n, Docker, git push, or any live service.
