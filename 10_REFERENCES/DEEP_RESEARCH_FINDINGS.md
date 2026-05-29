---
STATUS: RESEARCH
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# DEEP RESEARCH FINDINGS

Research-backed lessons that informed the SFV Engine architecture.
RESEARCH status — reference only, not built from directly.

---

## KEY LESSONS

### Lesson 01 — Workflow First, AI Second
Strong systems are workflow-first, not AI-first.
AI is added to a working workflow, not used to build one.

### Lesson 02 — Naming and Metadata Early
File naming and metadata consistency must be established at the start.
Retroactive renaming is expensive and error-prone.

### Lesson 03 — Context Compression
Claude context should be controlled through project files and briefing files.
Never re-explain the whole system every session.

### Lesson 04 — n8n Spaghetti Risk
n8n-style workflow tools become unmaintainable without modular design.
Every workflow block must be isolated and reusable.

### Lesson 05 — AI Clipping Without Human Review
AI clipping tools become generic without human review.
Clip selection must always have a human approval gate.

### Lesson 06 — Storage Friction
Storage should reduce friction, not become its own project.
Build minimal viable storage structure first.

### Lesson 07 — R&D and Production Separation
R&D and production must be on separate nodes.
Testing on production causes instability.

### Lesson 08 — Blueprint as Asset
The blueprint itself is an asset.
A well-designed blueprint reduces implementation errors significantly.

### Lesson 09 — Model Routing
Routing tasks to the right model saves significant cost.
Local models for 80% of tasks, premium API for 20%.

### Lesson 10 — Parallel Agent Costs
Multiple Claude Code agents running simultaneously use quota N times faster.
Use API key mode with spend cap for parallel overnight sessions.

## CONNECTED FILES
- [[COMPRESSED_CONTEXT|Compressed Context]]
- [[12_DATABANKS/RESEARCH_BANKS|Research Banks]]
