---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# USAGE OPTIMIZATION MASTER GUIDE

## PRIORITY ORDER
1. Ollama (free, install now)
2. Session discipline (free, do now)
3. Claude Code for building (free, already installed)
4. Max plan upgrade (when revenue justifies)

---

## OLLAMA SETUP
```
winget install Ollama.Ollama
ollama pull qwen3
ollama pull llama3.1
```
Interface: http://localhost:11434
Use for everything that doesn't need Claude's reasoning.

## TASK ROUTING — QUICK REFERENCE
| Task | Use |
|------|-----|
| Tagging, sorting, summaries | Ollama/Qwen3 |
| Transcription | Whisper (local) |
| File creation, renaming | Claude Code |
| Blueprint decisions | Claude Chat |
| Complex reasoning | Claude Chat |
| Research | Ollama first, Claude if needed |

## SESSION DISCIPLINE
- One topic per session
- Batch all questions in one message
- Switch to Code tab for file work
- End session when done, don't linger
- Max 1 planning session per feature

## CLAUDE CODE EFFICIENCY
- Always start: Read CLAUDE.md and COMPRESSED_CONTEXT.md
- One module per session
- Autonomous multi-step = fewer messages = less usage
- Point at C:\SFV_BLUEPRINT every session

## 3 ADDITIONAL OPTIMIZATIONS

### OPT 04 — TIERED ESCALATION
Ollama tries every task first.
Only escalate to Claude if Ollama outputs UNSURE or ERROR.
Result: Claude only sees genuinely hard problems.
Saves 60-80% of Claude calls on routine tasks.

### OPT 05 — TEMPLATE-BASED RESPONSES
Never ask Claude for free-form answers on structured tasks.
Always give a template to fill in.
BAD:  "Write a caption for this photo"
GOOD: "Fill this template: [SFV LIVE|##] [one line description] [mood word]"
Result: 50-70% fewer tokens per response.

### OPT 06 — SMART CONNECTIONS (Obsidian plugin)
Install: Smart Connections (community plugin)
What it does: creates local semantic embeddings of all vault notes.
Result: search vault semantically without feeding Claude full file contents.
Instead of pasting a whole file → ask Smart Connections → paste only relevant snippet.
Saves tokens on every session that involves vault lookup.

## CONNECTED FILES
- [[OLLAMA_SETUP|Ollama Setup Guide]]
- [[COMPRESSED_CONTEXT|Compressed Context]]
- [[CLAUDE_CODE_SESSION_2026-05-29|Claude Code Session 2026-05-29]]
- [[CLAUDE|Claude]]
- [[LOCAL_MODELS|Local Models]]
