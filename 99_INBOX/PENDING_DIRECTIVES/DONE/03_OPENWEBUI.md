---
STATUS: ACTIVE
DIRECTIVE_ID: REVAMP-20260701-OPENWEBUI-001
EXECUTOR: ollama
---

You are revising 03_INFRASTRUCTURE/OPEN_WEBUI_SPEC.md for SFV Engine. Scored 3/5: on track, needs
specifics. Context: Open WebUI is a self-hosted web front-end for local LLMs. SFV runs Ollama on
Engine Body (RTX 5080) with qwen3:14b, qwen2.5-coder:7b, minicpm-v:8b, devstral-small-2. Docker installed.
Open question in the vault: migrate n8n's workflow1 model calls to route through Open WebUI after Docker,
or keep calling Ollama directly.

Write a complete spec covering: (1) purpose — why Open WebUI in this stack (unified chat UI over local
models, prompt testing, model comparison), (2) deployment via Docker with a persistent volume, pointed
at the existing Ollama endpoint (host.docker.internal:11434), (3) which SFV use cases it serves
(manual prompt testing, model eval) vs which stay on direct Ollama API (n8n automation calls),
(4) the decision framework for the open question above with a clear recommendation and reasoning,
(5) access/security note (localhost-only vs Tailscale exposure).

Mark uncertain items [UNCONFIRMED]. Output only finished markdown.
