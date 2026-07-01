---
STATUS: ACTIVE
DIRECTIVE_ID: DEV-20260701-GIT-DIFF-SUMMARY-001
EXECUTOR: codex
---

Write a new python script C:\SFV_BLUEPRINT\99_INBOX\git_diff_summary.py that runs `git status` and `git diff --stat` (read-only git commands only — do NOT commit, push, or stage anything) inside C:\SFV_BLUEPRINT, and writes a plain-English summary of what changed tonight to C:\SFV_BLUEPRINT\99_INBOX\TONIGHT_CHANGES_SUMMARY.md (list of modified/new files, grouped by top-level folder, with a one-line total). Run the script once to generate the file. Do not run git add, git commit, or git push under any circumstance. Do not touch n8n, Docker, or any live service.
