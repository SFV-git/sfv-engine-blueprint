---
STATUS: ACTIVE
DIRECTIVE_ID: REVAMP-20260701-TOOLSTATUS-001
EXECUTOR: ollama
---

You are refreshing 06_TOOLS/TOOL_STATUS.md for SFV Engine. It is stale (v0.1.0, last touched 05-24) and
missing tools that are now live. Produce an updated tool-status table.

Current known tool states (as of 2026-07-01):
- Ollama: ACTIVE (qwen3:14b, qwen2.5-coder:7b, minicpm-v:8b, devstral-small-2 all pulled)
- n8n: ACTIVE (health 200, SQLite backend, Postgres migration pending)
- Hermes loop + gateway: ACTIVE (Scheduled Tasks SFV_HermesLoopWatcher + SFV_HermesGateway, Telegram connected)
- Aider: INSTALLED (isolated venv C:\SFV_TOOLS\aider-venv, paired with devstral-small-2, testing phase)
- Perplexity Pro: ACTIVE (manual research intake)
- Tavily: CONFIGURED but API key rotation PENDING (plaintext exposure flag)
- Desktop Commander MCP: ACTIVE (primary vault filesystem access)
- Obsidian / Git / Syncthing: ACTIVE (vault UI / version control / cross-node sync)
- Tailscale: ACTIVE (remote access)
- Bitwarden: PARTIAL (keys not yet migrated in)
- Docker: INSTALLED, not yet hosting services
- Antigravity / Gemini 2.5 Pro: ACTIVE (system audit / final reviewer)
- R&D Terminal Ollama: DOWN (not reinstalled after Win11 upgrade)

Write a clean status table: Tool | Status | Purpose | Notes/Blockers. Group by category (AI models,
automation, infrastructure, security). Mark anything uncertain [UNCONFIRMED]. Output only finished markdown.
