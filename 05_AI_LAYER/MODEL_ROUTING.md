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

| Task | Model | Location |
|------|-------|---------|
| Blur detection | Local (Qwen/Llama) | R&D terminal |
| Duplicate detection | Python script | Engine |
| Metadata tagging | Local model | R&D terminal |
| Caption drafts | Claude API | Cloud |
| Script matching | Whisper + local | R&D terminal |
| Take ranking | Local model | R&D terminal |
| QC audit | Local model + Claude | R&D → Engine |
| Creative strategy | Claude API | Cloud |
| Complex reasoning | Claude API | Cloud |
| Transcription | Whisper (local) | R&D terminal |
| Trend research | Local model | R&D terminal |

## COST PRINCIPLE
Claude API = reserved for strategy, art direction, final decisions.
Local models = handle 80% of repetitive tasks.
This is the primary method for minimizing API costs and usage limits.
