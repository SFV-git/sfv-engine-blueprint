---
STATUS: ACTIVE
DIRECTIVE_ID: PLAN-20260701-COST-CEILING-001
EXECUTOR: ollama
---

Draft a refined "Cost Ceiling Policy" for a solo creative studio's AI automation stack that mixes free local Ollama, a Claude subscription (Claude Code CLI), and a ChatGPT subscription (Codex CLI) — no per-token API billing on those two, but there may occasionally be direct Anthropic/OpenAI API calls that ARE metered. Propose: a simple monthly soft-cap in dollars for any metered API usage, an alert-only (not auto-shutoff) policy, and a simple log format (date, task, executor, estimated cost) for tracking spend. Output only the finished markdown section, no preamble.
