---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# MODEL ROUTING

## PURPOSE
Route tasks to the right model at the right cost.
Claude API only gets high-value tasks.
Local models handle everything else.

## ROUTING LOGIC

```
Task arrives
→ n8n router evaluates complexity [FUTURE — n8n not built yet]
→ simple/repetitive → local model (R&D terminal)
→ complex/creative → Claude API
→ result returned → Engine continues workflow
```

## TASK ROUTING TABLE

| Task | Tool | Location | Cost |
|------|------|----------|------|
| Blur detection | Ollama qwen3:14b | R&D terminal | Free |
| Duplicate detection | Python script | Engine | Free |
| Metadata tagging | Ollama qwen3:14b | R&D terminal | Free |
| Caption drafts (bulk) | Ollama qwen3:14b | R&D terminal | Free |
| Caption drafts (final polish) | Claude Sonnet | Cloud | $$  |
| Script matching | Whisper + Ollama | R&D terminal | Free |
| Take ranking | Ollama qwen3:14b | R&D terminal | Free |
| QC audit | Ollama → Claude review | R&D → Engine | Free → $$ |
| Blueprint planning | Claude Chat Sonnet | Cloud | $$ |
| Vault file editing | Claude Code Sonnet | Cloud | $$ |
| Desktop file routing | Claude Cowork | Engine | $$ |
| Vault local execution | Antigravity | Engine (local) | Free |
| Git audit | Antigravity | Engine (local) | Free |
| Massive-context reads | Google AI Studio Gemini 2.5 Pro | Cloud | Free |
| Research synthesis | NotebookLM | Cloud | Free |
| Creative strategy | Claude Sonnet | Cloud | $$ |
| Hard decisions | Claude Opus | Cloud | $$$$ |
| Transcription | Whisper (local) | R&D terminal | Free |
| Trend research | Ollama qwen3:14b | R&D terminal | Free |

## COST PRINCIPLE
Claude API = reserved for strategy, art direction, final decisions.
Local models = handle 80% of repetitive tasks.
This is the primary method for minimizing API costs and usage limits.
