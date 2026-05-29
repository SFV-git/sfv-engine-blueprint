---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# COST AND MODEL ROUTING GUIDE

## PRINCIPLE
Every task goes to the cheapest model that can handle it.
Claude API = last resort, not default.

---

## MODEL TIERS

| Model | Cost | Use for |
|-------|------|---------|
| Ollama/Qwen3 (local) | FREE | tagging, sorting, blur detection, transcription prep, summaries, research |
| Claude Haiku | ~$0.25/MTok | simple file ops, templating, basic formatting, renaming |
| Claude Sonnet | ~$3/MTok | blueprint work, build sessions, workflow design, QC audit |
| Claude Opus | ~$15/MTok | complex architecture decisions only, use sparingly |

## TASK ROUTING

### Always local (R&D terminal, Ollama):
- Blur/exposure detection
- Duplicate grouping
- Metadata tagging
- Whisper transcription
- Trend research
- Rough summaries
- Blueprint audits

### Claude Haiku:
- Simple file creation
- Template population
- Basic rename operations
- Log formatting

### Claude Sonnet (default for Claude Code):
- All build sessions
- Blueprint writing
- Workflow design
- QC audit layer
- Client brief generation

### Claude Opus (explicit request only):
- Major architecture decisions
- System redesign
- Complex cross-module reasoning

---

## SESSION COST MANAGEMENT

### Claude.ai (planning sessions)
- Project instruction reads vault → no re-explaining
- Reference COMPRESSED_CONTEXT.md not full vault
- Batch all questions in one message
- Direct file edits instead of chat explanations
- Max one planning session per feature

### Claude Code (build sessions)
- API key mode + $25 spend cap
- Sonnet only (never Opus by default)
- One module per session
- /compact when context gets long
- /clear between unrelated modules
- Commit after each module → fresh session

### Overnight runs
- API key mode
- Sonnet for all document generation
- Haiku for simple file creation tasks
- Set spend cap before sleeping
- Parallel instances for independent modules only

---

## CONTEXT COMPRESSION RULES

Never feed raw unstructured context to any model.
Always:
1. Local model summarizes raw input first
2. Structured output passed to Claude
3. Claude receives condensed high-value context only

Example:
BAD:  "Here are 400 photos from the shoot, analyze them"
GOOD: "18 selects from LIVE_20250606_SHAMAR. Sequence for carousel."

## CONNECTED FILES
- [[MODEL_ROUTING|Model Routing]]
- [[CLAUDE_API|Claude API]]
- [[LOCAL_MODELS|Local Models]]
- [[QUALITY_CONTROL|Quality Control]]
- [[AI_USE_CASE_PROFILE|AI Use Case Profile]]
- [[INTEGRATIONS|Integrations]]
