---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# OLLAMA SETUP — SFV ENGINE

## WHAT IT IS
Local AI model runner. Runs on RTX 5080. Free forever. No API costs.
Handles 80% of low-value tasks. Claude only gets complex reasoning.

## LIMITATIONS
- Not as smart as Claude — no complex decisions
- No internet access — can't research live data
- No persistent memory — feed context every call
- Smaller context window — use COMPRESSED_CONTEXT only
- Can't edit files directly — needs Python wrapper
- Will hallucinate on specifics — always verify
- Slower on complex tasks, fast on simple ones

## MODEL
qwen3:14b — optimal for RTX 5080 (16GB VRAM)
Install: ollama pull qwen3:14b

## RUNNING
ollama serve → runs at http://localhost:11434
Keep this terminal tab open whenever using Ollama.

## TASK ROUTING
USE OLLAMA FOR:
- Summarizing content
- Tagging and categorizing files
- Research synthesis
- Caption drafts (rough)
- QC pre-checks
- Blueprint audits
- Script brainstorming
- Trend research summaries

NEVER USE OLLAMA FOR:
- Final creative decisions
- Canon changes to the vault
- Client deliverable approval
- Archive curation
- Anything requiring current internet data

## OBSIDIAN INTEGRATION
Plugin: Local GPT (community plugin)
Settings:
  Provider: Ollama
  Model: qwen3:14b
  Base URL: http://localhost:11434
Usage: highlight text → right click → Local GPT options

## PYTHON WRAPPER
See SCRIPTS/ollama_wrapper.py for calling Ollama from scripts.

## SYSTEM PROMPT (use every call)
You are a task assistant for SFV Engine, a photography production system.
Branches: MYTHOLOGY, LIVE, EVENTS, ATHLETICS, STUDIO, UGC, ARCHIVE, WORLD, 404
Revenue: UGC content retainers + EVENTS on-site portraits
Your role: handle specific low-value tasks only. Be structured. Never make creative decisions.
If unsure, say UNSURE — never guess.
Output exactly what is asked. No extra commentary.

## CONNECTED FILES
- [[QUALITY_CONTROL|Quality Control]]
- [[LOCAL_MODELS|Local Models]]
- [[MYTHOLOGY|Mythology]]
- [[ENGINE_COMMUNICATION_MODEL|Engine Communication Model]]
- [[MODEL_ROUTING|Model Routing]]
