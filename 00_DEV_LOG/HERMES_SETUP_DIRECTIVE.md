# HERMES SETUP DIRECTIVE
# Executed by: Claude Code (headless)
# Auth: --dangerously-skip-permissions
# Target: Engine Body
# Status: FOR HUMAN REVIEW — Will must ratify before CANON

## OBJECTIVE
Configure Hermes Desktop on Engine Body for SFV Engine development work.
Three changes: (1) enable correct toolsets, (2) add local Ollama, (3) add vault MCP server.

## TASK 1 — Enable toolsets in config.yaml
File: C:\Users\willa\AppData\Local\hermes\config.yaml

Remove these from disabled_toolsets (i.e. enable them):
- coding
- file
- terminal
- search
- memory
- skills
- vision

Keep disabled (not needed):
- browser, clarify, code_execution, computer_use, context_engine
- cronjob, delegation, discord, discord_admin, feishu_doc, feishu_drive
- homeassistant, image_gen, kanban, project, session_search
- spotify, todo, tts, video, video_gen, web, x_search, yuanbao

Also enable smart model routing:
smart_model_routing:
  enabled: true

Also enable memory:
memory:
  memory_enabled: true
  user_profile_enabled: true

## TASK 2 — Add local Ollama to .env
File: C:\Users\willa\AppData\Local\hermes\.env

Add these lines at the top of the file (after the first comment block):
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_API_KEY=ollama

## TASK 3 — Add vault MCP server
File: C:\Users\willa\AppData\Local\hermes\config.yaml

Add an mcp_servers section if it doesn't exist:

mcp_servers:
  - name: sfv-vault
    command: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-filesystem"
      - "C:\\SFV_BLUEPRINT"

## TASK 4 — Write completion log
File: C:\SFV_BLUEPRINT\00_DEV_LOG\HERMES_EVAL.md

Append a section:
## Setup Run [DATE]
- Toolsets enabled: coding, file, terminal, search, memory, skills, vision
- Local Ollama configured: http://localhost:11434/v1
- Vault MCP added: sfv-vault → C:\SFV_BLUEPRINT
- Smart model routing: enabled
- Status: FOR HUMAN REVIEW — Will to ratify

## CONSTRAINTS
- Do not touch ANTHROPIC_API_KEY or any existing keys in .env
- Do not change model.default (stays claude-sonnet-4-6)
- Do not modify any n8n or Postgres configs
- Blueprint Lock: log all changes, do not self-ratify

## CONNECTED FILES
- [[CURRENT_DIRECTIVE|Current Directive]]
- [[MASTER_CONTEXT|Master Context]]
- [[MODEL_ROUTING|Model Routing]]
- [[OLLAMA_SETUP|Ollama Setup]]
- [[SESSION_STATE|Session State]]
- [[DASHBOARD|Dashboard]]
- [[MODEL_LOCK|Model Lock]]
