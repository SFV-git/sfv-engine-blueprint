---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE
---

# n8n-MCP INTEGRATION SPEC

> czlonkowski/n8n-mcp exposes n8n workflows as MCP (Model Context Protocol) tools.
> Enables Claude and Antigravity to trigger and query n8n directly via MCP calls,
> rather than file drops or webhook calls.

---

## WHAT IT DOES

n8n-MCP acts as a bridge: it runs as an MCP server that Claude Code or Antigravity connects to as an MCP client. This lets AI agents call n8n workflows as native tools — the same interface Claude Code uses for file reads, web search, etc.

**With n8n-MCP:**
- Claude Code can call: `trigger_workflow("workflow1_queue_processor", { task: {...} })`
- Antigravity can list available workflows and run them
- Results come back in-session — no polling required

---

## PREREQUISITES

- [ ] Docker installed on Engine Body (Gap 3 — DOCKER_INSTALL_CHECKLIST.md)
- [ ] n8n running with PostgreSQL (Gap 2 — POSTGRES_MIGRATION.md)
- [ ] n8n API key generated (Settings → API → Create API Key)

---

## DEPLOYMENT

```bash
docker run -d \
  --name n8n-mcp \
  --network host \
  -e N8N_API_URL=http://127.0.0.1:5678 \
  -e N8N_API_KEY=[N8N_API_KEY] \
  czlonkowski/n8n-mcp
```

**Notes:**
- `--network host` so the MCP server can reach n8n on localhost
- `N8N_API_KEY` must be added to `n8n_env.ps1` (gitignored) and to SECRETS_POLICY.md
- Container runs on `stdio` — MCP clients connect via stdio transport, not HTTP

[INFERENCE: czlonkowski/n8n-mcp uses stdio transport. Confirm from the repo README before deploying.]

---

## WORKFLOWS TO EXPOSE

Not all workflows should be MCP-accessible. Expose only what AI agents need to trigger:

| Workflow | Expose via MCP? | Reason |
|---|---|---|
| workflow1_queue_processor | YES — as dispatch tool | Agents can drop tasks directly |
| workflow2_model_prewarm | NO | Cron-only, no agent-trigger needed |
| workflow4_output_monitor | NO | Monitoring only, not an action |
| workflow3 (pending) | FOR HUMAN REVIEW | Depends on D3 decision |

**Principle:** Expose trigger surfaces only. Read-only monitoring workflows stay internal.

---

## WHICH AGENTS USE MCP

| Agent | MCP use case |
|---|---|
| Claude Code | Dispatch tasks to n8n within a Code session; read queue status |
| Antigravity | Trigger complex multi-step workflows without file writes |
| Claude Chat | [INFERENCE] — Claude.ai web does not support MCP. Cannot use this path. |

---

## AUTH MODEL

n8n-MCP authenticates to n8n via API key. Claude Code and Antigravity authenticate to n8n-MCP via MCP session (no separate auth — MCP assumes the connecting agent is trusted).

**Security boundary:** n8n-MCP runs on localhost only. It is not exposed to the LAN or Tailscale. Only processes on Engine Body can reach it.

---

## CLAUDE CODE MCP CONFIGURATION

To use n8n-MCP in Claude Code sessions, add to `claude_code_config.json` (or equivalent MCP config file):

```json
{
  "mcpServers": {
    "n8n": {
      "command": "docker",
      "args": ["exec", "-i", "n8n-mcp", "node", "dist/index.js"],
      "env": {}
    }
  }
}
```

[INFERENCE: Exact MCP config format depends on czlonkowski/n8n-mcp README. Confirm before writing config.]

---

## FALLBACK

If n8n-MCP container is down, agents fall back to file-drop method (ANTIGRAVITY_N8N_TRIGGER.md). The file-drop path is always available and is the baseline — MCP is an enhancement, not a dependency.

---

## CONNECTED FILES
- [[AI_STACK_ARCHITECTURE_BLUEPRINT|AI Stack Architecture §1]]
- [[DOCKER_INSTALL_CHECKLIST|Docker Install Checklist]]
- [[ANTIGRAVITY_N8N_TRIGGER|Antigravity → n8n Trigger]]
- [[SECRETS_POLICY|Secrets Policy]]
- [[POSTGRES_MIGRATION|PostgreSQL Migration]]
