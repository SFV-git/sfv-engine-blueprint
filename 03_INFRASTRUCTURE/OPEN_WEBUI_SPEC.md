---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE
---

# OPEN WEBUI DEPLOYMENT SPEC

> Unified OpenAI-compatible inference endpoint on Node A.
> Sits between n8n and Ollama — n8n calls one URL for all model inference.

---

## WHAT IT DOES

Open WebUI provides:
1. A browser-based chat UI for interacting with local Ollama models
2. An OpenAI-compatible REST API (`/v1/chat/completions`) that n8n can call
3. A single endpoint that routes to any model without per-model URL changes in n8n

**In the SFV stack:** Open WebUI becomes the stable API surface for n8n → Ollama calls. Instead of n8n calling `http://127.0.0.1:11434/api/generate` directly, n8n calls `http://127.0.0.1:3000/v1/chat/completions`. Open WebUI handles model routing and Ollama communication.

---

## PREREQUISITES

- Docker installed on Engine Body (DOCKER_INSTALL_CHECKLIST.md)
- Ollama running on Engine Body (`http://127.0.0.1:11434`)

---

## DEPLOYMENT

```bash
docker run -d \
  --name open-webui \
  --network host \
  -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

**Port:** 3000 (localhost only — do not expose to LAN)
**Data volume:** `open-webui` Docker volume (persists settings, history, users)

---

## AUTH MODEL

Open WebUI has built-in user auth. For the SFV stack:

| Access type | Config |
|---|---|
| Will (direct browser access) | Admin account — create on first launch |
| n8n (API calls) | Disable auth for API key OR create a service API key |
| External (LAN / Tailscale) | **Blocked by default** — port 3000 bound to localhost only |

**First launch:** Open WebUI asks to create an admin account. Use a real password, not a placeholder.

**n8n API access:** Open WebUI supports API key auth for OpenAI-compatible endpoints. Generate a key in Open WebUI admin settings and add to `n8n_env.ps1` as `OPENWEBUI_API_KEY`.

---

## ROUTING RULES — WHAT GOES THROUGH OPEN WEBUI vs DIRECT OLLAMA

| Path | Use |
|---|---|
| Open WebUI (`/v1/chat/completions`) | n8n workflow calls, structured multi-turn conversations, browser-based testing |
| Direct Ollama (`/api/generate`) | Legacy paths, streaming responses, raw generate calls |
| Direct Ollama (`/api/embeddings`) | Embedding generation (Open WebUI may not expose this) |

**[FOR HUMAN REVIEW]:** Migrate n8n workflow1 Ollama calls to Open WebUI endpoint after confirming stability? Keeps a single OpenAI-compatible interface. Direct Ollama calls remain for embeddings and any raw generate needs.

---

## n8n WORKFLOW MIGRATION (workflow1)

Current workflow1 "Call Ollama" node calls:
```
POST http://127.0.0.1:11434/api/generate
Body: { model, prompt, stream: false, keep_alive: '10m' }
```

**[FOR HUMAN REVIEW]:** If migration is approved, the new node call would be:
```
POST http://127.0.0.1:3000/v1/chat/completions
Headers: Authorization: Bearer [OPENWEBUI_API_KEY]
Body: {
  model: "qwen3:14b",  (or specialist model name)
  messages: [{ role: "user", content: "[prompt]" }],
  stream: false
}
Response: .choices[0].message.content
```

**[FOR HUMAN REVIEW]:** Migrate workflow1 to Open WebUI endpoint in Phase 1 after Docker install, or keep direct Ollama calls? Recommend: migrate — more stable long-term and enables model switching from UI.

---

## BROWSER ACCESS

Once running, Open WebUI is at: `http://localhost:3000`

Use for:
- Testing model responses before committing to a prompt in workflow1
- Comparing qwen3:14b vs qwen2.5-coder:7b on the same task
- Ad-hoc queries without going through the n8n queue

---

## CONNECTED FILES
- [[AI_STACK_ARCHITECTURE_BLUEPRINT|AI Stack Architecture §1]]
- [[DOCKER_INSTALL_CHECKLIST|Docker Install Checklist]]
- [[LOCAL_MODELS|Local Models]]
- [[SECRETS_POLICY|Secrets Policy]]
- [[N8N_MCP_SPEC|n8n-MCP Spec]]
- [[workflow1_queue_processor|Workflow 1 JSON]]
