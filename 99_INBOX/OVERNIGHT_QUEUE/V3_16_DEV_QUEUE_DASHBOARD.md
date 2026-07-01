---
STATUS: ACTIVE
DIRECTIVE_ID: DEV-20260701-QUEUE-DASHBOARD-001
EXECUTOR: codex
---

Write a new python script C:\SFV_BLUEPRINT\99_INBOX\queue_dashboard.py that reads C:\SFV_BLUEPRINT\99_INBOX\DECISION_LOG.md (a markdown table) and C:\SFV_BLUEPRINT\99_INBOX\OUTPUTS\ (result files), and generates a summary markdown file C:\SFV_BLUEPRINT\VAULT_DASHBOARD_DRAFT.md showing: total directives dispatched, count per executor (ollama/claude/claude_code/codex), count per status, and the 10 most recent dispatches. Run the script once to generate the output. Do not overwrite VAULT_DASHBOARD_DRAFT.md if the real DASHBOARD.md already exists — use the DRAFT filename exactly as given. Do not touch DASHBOARD.md itself. Do not touch n8n, Docker, git push, or any live service.
