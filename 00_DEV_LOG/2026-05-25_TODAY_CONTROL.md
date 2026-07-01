---
STATUS: ACTIVE
DATE: 2026-05-25
OWNER: WILL
---

# TODAY CONTROL — 2026-05-25

## SESSION OBJECTIVE
Build the Engine communication layer and fix the AI stack hierarchy before touching ingest.

---

## PRIORITY ORDER

1. AI use-case profile correction — Antigravity understated, fix hierarchy
2. Engine communication model — task queue, output folder, handoff notes, decision log
3. Perplexity integration — structured research layer feeding blueprint + Obsidian + agent queue
4. Ollama repair — define role first, then fix; first test = read task → process → write output
5. Ingest waste audit — n8n-first logic, flag Claude overuse, flag hardcoded paths
6. Token optimization routing — cheapest capable layer gets the task, not default Claude

---

## TODAY'S BUILD TARGETS

| File | Action | Status |
|------|--------|--------|
| 02_AI_STACK/AI_USE_CASE_PROFILE.md | Create/update — corrected hierarchy | IN PROGRESS |
| 03_INFRASTRUCTURE/ENGINE_COMMUNICATION_MODEL.md | Create — full communication model | IN PROGRESS |
| SFV_OS/ENGINE/QUEUE/20260525-001_PERPLEXITY_N8N_INGEST_RESEARCH.json | Create — first Perplexity task file | IN PROGRESS |
| 04_WORKFLOWS/INGEST.md | Audit only — flag waste, no rewrite | IN PROGRESS |
| 99_INBOX/ollama_task_loop_test.py | Design first Ollama queue test | IN PROGRESS |

---

## WHAT IS NOT HAPPENING TODAY
- No ingest rewrite
- No rushed demo for May 28 at cost of architecture
- No blind Ollama fixes without defined role
- No canon changes without Will approval

---

## RULE REMINDER
Will request → task queue → cheapest capable layer → output file → review if needed → canon only after approval

## CONNECTED FILES
- [[RESEARCH_ROUTE_SPEC|Research Route Spec]]
- [[OLLAMA_SETUP|Ollama Setup]]
- [[COST_ROUTING|Cost Routing]]
- [[MODEL_ROUTING|Model Routing]]
- [[TRAINING_DATA_AUTOMATION|Training Data Automation]]
- [[PROMPT_VERSIONING|Prompt Versioning]]
