---
STATUS: FOR HUMAN REVIEW
OWNER: WILL
CREATED_BY: Claude Code (Blueprint Builder, Opus) — 2026-06-27
PURPOSE: Plain-language handoff for the NEXT CLAUDE CHAT session. Chat does planning/decisions, not
  subagents or file writes — this frames what Will should review/decide and what to hand to Claude Code next.
---

# HANDOFF → NEXT CLAUDE CHAT

## Where things stand (one paragraph)
Claude Code just finished **STEP 1** of the Blueprint Completeness Audit. The whole engine — both nodes,
all 9 branches, ingest→edit→deliver→archive, plus infra/AI — was walked and graded COVERED / THIN / MISSING.
The result is one file: **`08_TESTS/BLUEPRINT_COVERAGE_MAP.md`**. **STEP 2** (research the gaps + write the
Content Idea Bank spec) did NOT happen — the session hit the Anthropic limit before any research ran.

## The single thing to read first
`08_TESTS/BLUEPRINT_COVERAGE_MAP.md` — specifically **§6, the ranked MASTER GAP LIST (18 items)**. That's
the backlog. Everything below is about confirming that list and feeding it back to Claude Code.

## What the audit found (the short version)
- The **infrastructure / AI layer is fine on paper** — docs exist, they're just waiting on execution
  (Postgres, Docker, WF1 re-import, etc.). Not where the holes are.
- The **real missing pieces are the creative + business craft**, which nobody had blueprinted:
  - **No video-editing (Premiere Pro) workflow doc at all** — affects UGC, LIVE, ARCHIVE, ATHLETICS, etc.
  - **No Instagram scheduling workflow** for any of the 8 automated branches (Later vs Buffer still undecided).
  - **No Lightroom preset/catalog doc** — the Morning Walk / Shamar recipe lives only in your head + practice.
  - **The UGC money pipeline is half-missing**: lead intake, brief/contract, invoicing, client notification,
    and performance reporting have ZERO coverage. Only the pre-production app + ingest are solid.
  - **The Content Idea Bank (R&D Terminal "Role 5") doesn't exist yet** — this was the headline ask.

## Decisions only YOU can make (Chat should walk you through these)
These block STEP 2 docs — Claude Code can't invent them:
1. **UGC video editor:** Premiere Pro vs CapCut vs Aditor.ai? (Premiere is the only one currently in the stack.)
2. **Scheduling tool:** Later vs Buffer (vs other)?
3. **UGC business tools:** CRM/lead tracker, contract/proposal tool, payment/invoicing tool, client delivery
   platform (currently WeTransfer stop-gap).
4. **Gap priority order:** confirm §6's ranking matches your priorities before Code spends tokens writing docs.

## What to tell the next Claude Code session to do (STEP 2, in order)
1. Re-run the 2 research subagents (ingestion services + storage/retrieval tech) → write `10_REFERENCES/TOOL_RESEARCH.md`.
2. Write `05_AI_LAYER/CONTENT_IDEA_BANK.md` (R&D Terminal Role 5 — 6 stages: ingestion, scoring, storage,
   retrieval, feedback loop, node boundary). Respect: NO independent internet on R&D Terminal (routes via
   Engine Body ICS) + 12GB VRAM ceiling + Tavily key must be rotated first.
3. Add a Role 5 note to `RD_TERMINAL_ARCHITECTURE.md` (FHR edit, not a rewrite).
4. Work the rest of §6's ranked gaps, one FHR doc each.
Full detailed version: `00_DEV_LOG/HANDOFF_2026-06-27_BLUEPRINT_AUDIT.md`.

## Housekeeping / still-open from before (not touched this session)
PROPOSAL 008 ratify/revert · A1–A3 (Hermes adoption) · Tavily key rotation · n8n restart for the WF4 fix.
Nothing was committed to git this session — you push.

## Guardrails (still in force)
Everything produced is FOR HUMAN REVIEW. No CANON promotion, no building, no live n8n/Ollama/Postgres
changes. You ratify everything.

## CONNECTED FILES
- [[BLUEPRINT_COVERAGE_MAP|Blueprint Coverage Map]]
- [[HANDOFF_2026-06-27_BLUEPRINT_AUDIT|Detailed Code Handoff]]
- [[DIRECTIVE_BLUEPRINT_AUDIT_CONTENT_BANK|Directive]]
- [[RD_TERMINAL_ARCHITECTURE|R&D Terminal Architecture]]
- [[SESSION_STATE|Session State]]
