---
STATUS: CANON
VERSION: v0.3.0
OWNER: WILL
LAST_UPDATED: 2026-06-09
---

# SFV ENGINE — COMPRESSED CONTEXT
Use this file for cheap model calls. Never re-explain from scratch.

SFV = Will's photo/video/content brand. Sole owner. No equity sharing.
Engine = intelligent file management + light automation on Engine Body (Ryzen 9 9900X / RTX 5080 / 32GB RAM, 64GB upgrade planned / Win11).
R&D Terminal = RTX 3060 / 16GB / 24/7 Sentinel node / never touches production. Post-Win11 rebuild: Ollama, Syncthing, Claude Code, windows_exporter pending reinstall.
Vault = C:\SFV_BLUEPRINT (Obsidian + Git, Syncthing sync A↔B).
Network: ICS direct ethernet — Engine Body 192.168.137.1, R&D Terminal 192.168.137.246. Tailscale for remote.

BRANCHES (9): MYTHOLOGY | SFV_LIVE | SFV_EVENTS | SFV_ATHLETICS | SFV_STUDIO | SFV_UGC | SFV_ARCHIVE | SFV_WORLD | SFV_404
MONEY: SFV_UGC (retainers) + SFV_EVENTS (on-site portraits)
GROWTH ACCOUNTS: SFV_STUDIO + SFV_UGC only

ENGINE LEVELS: 1=store only | 2=organize | 3=rough edit | 4=full edit | 5=runs account | 6=adds ads | +.5=schedules
abbass=1 | LIVE=3.5 | EVENTS=5-6.5 | ATHLETICS=3.5 | STUDIO=5.5 | UGC=6.5 | ARCHIVE=3.5 | WORLD=2.5 | 404=2.5

LEADS: Brandon Bellotti (first UGC client candidate) | ProEdge/Will Wilver (warm)

PATHS: Vault = C:\SFV_BLUEPRINT | Active storage = D:\SFV_ACTIVE (Seagate One Touch 5TB) | Field ingest = E:\ (SanDisk Extreme 1TB)
All scripts use env vars from ENVIRONMENT_CONFIG.md — never hardcode paths.

TOOLS ACTIVE: Claude Chat | Claude Code (--dangerously-skip-permissions, launched from C:\SFV_BLUEPRINT) | Antigravity 2.0 (Gemini Flash, free preview) | n8n v2.22.5 @ localhost:5678 | Ollama (Engine Body: qwen3:14b default, qwen2.5-coder:7b CODE, minicpm-v:8b VISION) | Tavily API (in n8n) | Perplexity Pro (manual) | Syncthing | Tailscale | Python | Git | Obsidian | Lightroom Classic | Premiere Pro | Pixieset | Zenfolio (events)
TOOLS FREE CLOUD: Google AI Studio (Gemini Pro, 1M context — full-vault audits) | NotebookLM
TOOLS PENDING: Docker (approved, install needs restart) | PostgreSQL (mandatory before Redis/scaling) | Open WebUI | Qdrant | Redis | Supabase

LIVE AUTOMATION: workflow1 queue processor (QUEUE\*.json → Ollama route by task_type → OUTPUTS/HANDOFFS) | workflow2 pre-warm cron 5min | workflow4 output monitor | watchdog.ps1 (n8n+Ollama health, 5min) | vault_watcher.py
CONFIDENCE: default HIGH, escalate only on doubt keywords — CONFIDENCE_LOGIC.md (CANON)

TOOL ROLES:
- Claude Chat = planning, decisions, blueprint sessions
- Claude Code = vault file writes, scripts, autonomous execution (separate sessions per node via CLAUDE_CONFIG_DIR)
- Antigravity 2.0 = agentic orchestrator — parallel agents, scheduled tasks. Default model MUST be Gemini Flash, not Claude.
- Ollama = batch local inference via n8n QUEUE (free)
- Tavily = automated web search inside n8n | Perplexity = manual research intake
- Google AI Studio (1M context) = full-vault audits and massive context reads
- Opus = only when Will explicitly requests it

RULES: No invention. Label UNCONFIRMED/INFERENCE/FOR HUMAN REVIEW. Will is final authority.
BLUEPRINT LOCK: No dev work until planning is complete and Will approves build order. Long-term correctness > deadlines.
LOCKED: 9 branches | vault path | naming conventions (SFV_STUDIO format, underscore caps) | storage layout | model routing above
ANTIGRAVITY OUTPUTS ≠ WILL'S APPROVAL: explicit confirmation required before CANON promotion.

## CONNECTED FILES
- [[BRANCH_OUTPUTS|Branch Outputs]]
- [[ANTIGRAVITY_SETUP_GUIDE|Antigravity Setup Guide]]
- [[ENVIRONMENT_CONFIG|Environment Configuration]]
- [[RULES|Canon Rules]]
- [[SESSION_STATE|Session State]]
- [[JOB_ENVELOPE_SPEC|Job Envelope Spec]]
- [[CONFIDENCE_LOGIC|Confidence Logic]]
- [[OLLAMA_SETUP|Ollama Setup]]
