---
STATUS: CANON
VERSION: v0.2.0
OWNER: WILL
LAST_UPDATED: 2026-05-25
---

# AI USE-CASE PROFILE

> Corrected hierarchy as of 2026-05-25. Previous versions understated Antigravity. Fixed.

---

## TIER 1 — SYSTEM-LEVEL (Antigravity)

### Antigravity 2.0
**Role: Top-tier system builder, codebase reviewer, orchestration and audit layer**

Antigravity is the highest-leverage tool in the Engine. NOT a helper. NOT a side tool.

Use for:
- Full codebase review and audit
- PowerShell and script execution directly on the machine
- Agentic orchestration — runs subagents, schedules tasks, triggers workflows
- System-level blueprint review — catches contradictions across all docs
- Final review pass before anything becomes canon
- Architectural decisions requiring web access + local execution + multi-step reasoning
- Coordinating tasks that would otherwise require Will to manually jump between 3 tools

Do NOT waste on:
- Simple summaries, routing decisions, file renaming, single-step lookups

**CONFIRMED CANON. Full rules: ANTIGRAVITY_RULES.md**

---

## TIER 2 — HIGH REASONING (Claude)

### Claude (Sonnet default / Opus on request)
**Role: Architecture, implementation design, blueprint writing, complex reasoning**

Use for:
- Blueprint doc creation and updates
- Workflow design and multi-step reasoning with ambiguous inputs
- Writing code that will enter canon
- Reviewing Ollama or n8n outputs before escalation

Do NOT use for:
- Tasks n8n, PowerShell, or Python can handle alone
- Simple classification, routing, or short-file summaries
- Anything Ollama can do at acceptable quality

---

## TIER 3 — RESEARCH LAYER (Perplexity)

### Perplexity
**Role: Primary research and current web intelligence layer**

Entry point for any question requiring current web knowledge. Feeds structured inputs INTO the Engine — does not replace Claude reasoning.

Use for:
- Current events, pricing, tool comparisons, best practices
- Research that feeds task queue, Obsidian notes, or agent handoff files
- Any question where the answer depends on post-training-cutoff data

Output flow:
```
Perplexity research → structured file in QUEUE or OUTPUTS → Claude or Antigravity review → canon if approved
```

Do NOT use for:
- Blueprint editing, code execution, local file access

---

## TIER 4 — AUTOMATION ROUTING (n8n)

### n8n
**Role: Automation routing and repeatable workflow execution**

If a workflow runs more than once with the same logic, it belongs in n8n.

Use for:
- File watcher triggers, ingest routing, posting schedules
- Webhook handling, moving files on trigger
- Calling Ollama or external APIs on schedule

Do NOT use for:
- One-off tasks, complex reasoning, judgment calls

---

## TIER 5 — LOCAL HELPER (Ollama)

### Ollama (local, free, always-on)
**Role: Cheap local helper — compression, classification, routing drafts, handoff generation**

Runs locally. Costs nothing per call. Default first attempt for any task not requiring web access or high reasoning.

Use for:
- Summarizing task files
- Classifying branch/tag from filename or metadata
- Compressing context before sending to Claude
- Reading queue files and writing draft outputs
- Generating handoff notes for Claude or Antigravity
- Logging status updates to OLLAMA_RESULTS.md

Do NOT use for:
- Final decisions, canon edits, web-dependent tasks, high-accuracy code generation

**First test (pending): Read one JSON task from queue → process → write markdown output → log status**

---

## ROUTING DECISION TREE

```
Will request arrives
  ↓ Can n8n / PowerShell / Python handle it alone?
    YES → use that. No AI.
  ↓ Does it require current web data?
    YES → Perplexity first. Output to queue.
  ↓ Is it local, cheap, classification or summary?
    YES → Ollama.
  ↓ Is it architecture, blueprint, or complex code?
    YES → Claude.
  ↓ Is it system audit, orchestration, or codebase review?
    YES → Antigravity.
```

---

## WHAT CHANGED FROM PREVIOUS VERSION
- Antigravity elevated to Tier 1. Was previously treated as peer to Claude. That was wrong.
- Ollama given a defined role. Was previously undefined.
- Perplexity formalized as structured research intake. Was previously ad hoc.
- Routing decision tree added.

## CONNECTED FILES
- [[05_AI_LAYER/COST_ROUTING|Cost Routing]]
- [[05_AI_LAYER/RATE_LIMITS|Rate Limits]]
- [[COMPRESSED_CONTEXT|Compressed Context]]
