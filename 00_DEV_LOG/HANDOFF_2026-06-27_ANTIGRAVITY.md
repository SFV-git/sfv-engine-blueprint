---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
CREATED_BY: Antigravity — 2026-06-27 session
PURPOSE: Ground-truth state + Hermes architecture decisions for next Claude Code session.
READ BEFORE TOUCHING ANYTHING.
---

# SESSION HANDOFF — 2026-06-27 (Antigravity Session)

## WHAT WAS COMPLETED THIS SESSION

### Architecture decisions finalized (FOR WILL'S RATIFICATION)
This session completed the AI stack analysis that Claude Chat identified as the gap in the
2026-06-27 HANDOFF. Three new vault documents were written:

1. **`01_CANON_RULES/DIRECTIVE_TEMPLATE.md`** — CANON-candidate
   The missing schema for CURRENT_DIRECTIVE.md. Defines all fields Will needs to write
   to drive an autonomous build session. Includes full worked example.

2. **`05_AI_LAYER/HERMES_INTEGRATION.md`** — FOR HUMAN REVIEW
   Complete Hermes Agent integration spec. Includes:
   - Eval directive for Claude Code (copy-paste ready)
   - 7 success criteria for the eval (pass/fail/partial for each)
   - Adoption decision rules (what pass rate = adopt vs reject)
   - Hermes configuration spec for Engine Body
   - Separate Hermes config for R&D Terminal
   - Rollback procedure for autonomous sessions
   - Implementation order (8 steps from eval to stable)

3. **`05_AI_LAYER/HERMES_SKILLS_SEED.md`** — FOR HUMAN REVIEW
   10 pre-seeded Hermes skills derived entirely from existing vault docs.
   Import at adoption time. Gives Hermes SFV-specific knowledge from day one.
   Skips the cold-start period. Claude Code imports during integration session.

4. **Antigravity AI Stack Analysis artifact** (Antigravity's artifact store)
   Full analysis: current stack gaps, Hermes placement, per-stage stack diagrams,
   9 gaps identified. Referenced in this handoff but not in the vault.

---

## DECISIONS MADE BY ANTIGRAVITY (FOR WILL'S RATIFICATION — Blueprint Lock rule applies)

### DECISION A1 — Adopt Hermes (eval-first)
**Recommendation:** ADOPT Hermes Agent as the persistent daemon + loop driver.
**Rationale:** Fills the exact missing piece. Custom orchestrator (Option B) gets you the
same functionality in one session but stays flat forever. Hermes compounds.
**Condition:** Run the eval directive first. If Criterion 2 (daemon persistence) or
Criterion 3 (Anthropic API) FAIL: fall back to Option B immediately.
**Will decides: ADOPT / REJECT / DEFER**

### DECISION A2 — CURRENT_DIRECTIVE.md as the canonical loop entry point
**Recommendation:** CURRENT_DIRECTIVE.md (schema in DIRECTIVE_TEMPLATE.md) is the
single file Will writes to drive autonomous sessions. Hermes watches it. Claude Code reads it.
All the rules (scope bounds, human gate triggers, max turns, max budget) live in it.
**Will decides: RATIFY / MODIFY / REJECT**

### DECISION A3 — CANON locked during autonomous sessions (Rule 13)
**Recommendation:** Add Rule 13 to CANON_RULES: "Autonomous sessions write DRAFT only.
Will promotes to CANON manually." This is already implicit in the system but needs to be
explicit and enforced in the Hermes directive loop.
**Will decides: RATIFY / MODIFY**

---

## GAPS IDENTIFIED (from AI Stack Analysis — 9 total, top 5 most urgent)

| Gap | Risk | Effort | Status |
|-----|------|--------|--------|
| No DIRECTIVE_TEMPLATE schema | Loop can't run reliably | 1 hour | **DONE — file written** |
| WF4 process.env bug | Output monitoring blind | 5 min (Claude Code) | Open — next session |
| qwen3 thinking-block strip | False escalations at volume | 30 min (Claude Code) | Open — next session |
| No Hermes eval success criteria | Eval returns ambiguous result | 15 min | **DONE — in HERMES_INTEGRATION.md** |
| No rollback policy | Overnight sessions unsafe | 1 hour | **DONE — in HERMES_INTEGRATION.md** |
| No skill seeding plan | Cold-start wastes 40% efficiency | 2-4 hours | **DONE — HERMES_SKILLS_SEED.md** |
| R&D Terminal Ollama offline | No fallback, no Sentinel Role 3 | 1 session | Open |
| Budget-awareness gate | Runaway spend during autonomous | 30 min | Open — post-Hermes |
| Checkpoint/state recovery | Loop hangs on crash | 2 hours | Open — post-Hermes |

---

## NEXT SESSION PRIORITY ORDER

**Claude Code on Engine Body:**

1. **Will ratifies A1/A2/A3 above** (5-10 min, Blueprint Lock rule — must happen before anything)
2. **Fix WF4 process.env bug** — 5 minute Claude Code fix, re-import, verify no errors
3. **Fix qwen3 thinking-block strip in WF1** — add `<think>...</think>` strip before LOW_WORDS check
4. **Hermes eval directive** — copy from `HERMES_INTEGRATION.md §EVAL DIRECTIVE FOR CLAUDE CODE`
   Run it. Claude Code writes `00_DEV_LOG/HERMES_EVAL.md`. Will reviews.
5. **If eval passes: Hermes integration session** — configure, seed skills, test first directive
6. **n8n API key** — mint via UI (Settings → API → Create). Still not done from last session.
7. **Update backup_n8n.ps1 to pg_dump** (carried from 06-26)
8. **Git push** (Will pushes — multiple unpushed commits)

**Claude Chat / Antigravity (next time):**
- Review HERMES_EVAL.md after Claude Code writes it
- Final review pass after Hermes integration session

---

## CURRENT INFRASTRUCTURE STATE (end of 2026-06-27 Antigravity session)

*(Unchanged from HANDOFF_2026-06-27.md — no build work done this session, architecture only)*

- n8n: PostgreSQL 18, health 200, WF1+WF2+WF4 active+published
- Queue: WORKING end-to-end (TEST-002 confirmed)
- Ollama: running, qwen3:14b + qwen2.5-coder:7b + minicpm-v:8b
- WF4: active but errors on process.env (non-blocking for WF1)
- Scheduled tasks: SFV_n8n_Backup (03:00 daily) + SFV_Watchdog (at startup) — both Ready
- Git: multiple commits unpushed. Will pushes.
- Bitwarden: Postgres passwords NOT yet entered (A3 still open)
- Docker: not installed
- workflow3: not built
- R&D Terminal Ollama: needs reinstall (post-Win11 rebuild)
- Hermes: not yet installed (pending eval)

---

## NEW FILES IN VAULT (this session)

| File | Status | Purpose |
|------|--------|---------|
| `01_CANON_RULES/DIRECTIVE_TEMPLATE.md` | FOR HUMAN REVIEW | CURRENT_DIRECTIVE schema |
| `05_AI_LAYER/HERMES_INTEGRATION.md` | FOR HUMAN REVIEW | Hermes eval + integration spec |
| `05_AI_LAYER/HERMES_SKILLS_SEED.md` | FOR HUMAN REVIEW | 10 pre-seeded Hermes skills |

All three are FOR HUMAN REVIEW. Promote to CANON only after Will ratifies.
DIRECTIVE_TEMPLATE.md should go in `01_CANON_RULES/` because it is a process rule, not an AI layer doc.

---

## KEY REFERENCES

- Hermes Agent repo: https://github.com/NousResearch/hermes-agent
- Hermes self-evolution repo: https://github.com/NousResearch/hermes-agent-self-evolution
- Claude Code headless docs: https://code.claude.com/docs/en/headless
- `HERMES_INTEGRATION.md` — full spec, eval directive, config, rollback
- `DIRECTIVE_TEMPLATE.md` — the schema for CURRENT_DIRECTIVE.md
- `HERMES_SKILLS_SEED.md` — 10 skills to import at adoption time
- `HANDOFF_2026-06-27.md` — previous session handoff (architecture decision context)

## CONNECTED FILES
- [[DIRECTIVE_TEMPLATE|Directive Template]]
- [[HERMES_INTEGRATION|Hermes Integration]]
- [[HERMES_SKILLS_SEED|Hermes Skills Seed]]
