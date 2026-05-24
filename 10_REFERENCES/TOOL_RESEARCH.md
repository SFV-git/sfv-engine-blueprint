---
STATUS: RESEARCH
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# TOOL RESEARCH

Research notes on tools considered for SFV Engine.
See TOOL_STATUS.md for current decisions.

---

## OPENCLAW
Open source autonomous AI agent. 250,000+ GitHub stars.
Runs locally. 100+ built-in skills. File system access.
Model agnostic — bring your own API key.
Continuous multi-step workflows without checking in at every step.

Potential role: R&D terminal autonomous agent layer.
Handles: routine file operations, research, proposal generation.
Risk: still experimental ecosystem. Moltbook data breach Jan 2026.
Status: RESEARCHING — FOR HUMAN REVIEW

## SUPABASE
Open source Firebase alternative. Postgres + auth + storage.
Free tier handles significant scale.
Best option for CLIENT_ID, EVENT_ID, PERSON_ID system.
Status: APPROVED for future database layer.

## VERCEL
Deployment platform for dashboard.
Free tier, zero infrastructure management.
Pairs naturally with Supabase.
Status: FUTURE

## APIFY
Web scraping and automation platform.
Use case: trend research, competitor content analysis for UGC clients.
Status: RESEARCHING

## CAPTIONS APP
AI captions for video content. Cloud-based, per-use cost.
Relevant for UGC reel pipeline.
Alternative: local Whisper (free, R&D terminal).
Decision pending: cost vs convenience tradeoff.
Status: RESEARCHING

## OLLAMA
Local model runner. Free. Runs Qwen, Llama, DeepSeek locally.
RTX 3060 on R&D terminal handles 7B-13B models well.
Primary cost-reduction tool for AI tasks.
Status: APPROVED
