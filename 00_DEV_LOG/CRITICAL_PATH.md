---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-06-10
CREATED_BY: Claude Fable 5 (Session Maple, Prompt B)
---

# CRITICAL PATH — TO MILESTONE M1

**M1 = PostgreSQL-backed n8n + workflow3 RESEARCH route live + SESSION_STATE matching
runtime.** First demo is history (queue processor validated 06-03); M1 is the next state
worth declaring. Standing order applies: no deadlines, correctness first — this is an
ORDER, not a schedule.

Legend: ⬛ Will-only · 🔷 Will + Claude Code on Engine Body · 🔶 Fable/Chat (doable tonight,
no Engine Body) · ⏱ rough Will-time.

---

## STEP 0 — DECISION GATE ⬛ ⏱ 15–30 min total
1. **Ratify or revert PROPOSAL 008.** Everything from 06-09 (COMPRESSED_CONTEXT v0.3,
   IP fixes, LEGACY marks, UNCONFIRMED reconciliation) hangs on this. Git diff shows all.
2. **Answer A1–A6** (QUESTIONS_FOR_WILL): A1 five-of-six ratification + N8N_MCP tag
   decision (matrix C12) · A2 approve schedule · A3 Bitwarden confirm · A4 defer-note
   until R&D rebuild · A5 yes/no Scheduled Task · A6 authorize runtime verification.
3. Optional same sitting: Q15–25 sweep — Q17 (Node-B fallback = 14b) and Q24 (Syncthing
   versioning) are the two that unblock other steps.

## STEP 1 — FIVE-MINUTE FIXES 🔷 ⏱ ~20 min
4. **S1: rotate Tavily key** → update n8n_env.ps1 → restart n8n → "KEY ROTATED" row in
   DECISIONS.md → add snapshot exclusions (`n8n_env.ps1`, `.claude*/settings.local.json`).
5. **S2/A3: enter/confirm all keys in Bitwarden** (the NEW Tavily key).
6. **D1/A2: schedule backup_n8n.ps1** — Task Scheduler, daily 03:00, run-when-not-logged-in.
7. **A5: watchdog → Scheduled Task** (if approved).
8. **W6: clear 4 stale PENDING tasks** in LEGACY TASK_QUEUE.md.
9. **W7: run the OUTPUTS_RETENTION 13-file cleanup** (if approved).

## STEP 2 — RUNTIME VERIFICATION + WRITE-BACK 🔷 ⏱ ~20 min
10. **A6/C4:** n8n UI → record actual workflow IDs + active states.
11. **C3/W2:** open live workflow1 → confirm think-strip + Phase-1 validation present
    (if absent: re-import vault JSON — after step 13's hygiene fix, ideally).
12. **GitHub remote check:** `git remote -v` + last push (DR assumes GitHub is the off-site).
13. **Write SESSION_STATE back to runtime truth** — closes the discipline gap by example;
    add session-end checklist enforcement note.

## STEP 3 — JSON/LAUNCHER HYGIENE 🔷 ⏱ ~30 min
14. **W1:** re-save workflow1 + workflow4 JSONs UTF-8 no-BOM, fix mojibake names. (Fable
    can emit cleaned files next session as a proposal; Will imports via UI.)
15. **W3:** add `client_facing → force ESCALATE` check to workflow1 Write+Log
    (spec exists in JOB_ENVELOPE_SPEC + Blueprint §3; ~3 lines).
16. **C14/W5:** start_n8n.ps1 dot-sources n8n_env.ps1; single ALLOW_BUILTIN; nodes read
    `$env.VAULT_PATH` with hardcode as fallback. Re-import, re-run TEST_CLASSIFY_002 +
    TEST_CODE_004 as regression proof.

## STEP 4 — POSTGRESQL MIGRATION ⬛🔷 ⏱ ~1–2 h supervised
17. Per POSTGRES_MIGRATION.md exactly: backup .n8n → native install (Option A, matches
    CANON C:\ allocation) → create db/user → env vars (+ template) → start → validate
    table incl. the 3-simultaneous-drops concurrency check → rollback path armed.
    Promote doc to CANON on success. **Gates: Redis, n8n-MCP, Phase-1 concurrency.**

## STEP 5 — DOCKER ⬛ ⏱ install + restart, end of a session
18. Per DOCKER_INSTALL_CHECKLIST (CANON). Post-install reference updates per its table.
    **Unlocks: Open WebUI, n8n-MCP, Redis, Qdrant — none required for M1 except none;
    Docker itself is on the path only because Will wants it stable before workflow3-era
    expansion.** (workflow3 needs only Tavily — no Docker dependency. Docker can slide
    after step 19 if a session runs short.)

## STEP 6 — WORKFLOW3 BUILD 🔷 ⏱ ~1 session
19. Per RESEARCH_ROUTE_SPEC (D3=C2 confirmed): dedicated handler, `auto_research` branch →
    Tavily → OUTPUTS, else → HANDOFF. Promote JOB_ENVELOPE_SPEC first (🔶 doable tonight)
    so the schema is locked. Acceptance = **Theory Run Scenario C** executed for real:
    drop a RESEARCH envelope, watch the full path, log to DECISION_LOG.

## PARALLEL TRACK A — R&D TERMINAL (any time after Step 0) ⬛🔷
20. **C8 fix first:** patch TWO_TERMINAL plan B2 to the CANON roster (qwen3:8b + qwen3:14b,
    no coder, NUM_PARALLEL=1, KEEP_ALIVE=2m). Then the install sequence: Ollama → Syncthing
    (Device ID in MYTHOS_FORWARD_PROMPT; fsWatcherDelayS=1) → Claude Code (.claude-rnd/) →
    windows_exporter. Then **A4** (Whisper port) and **FAILOVER wiring** into workflow1 →
    validated by **Theory Run Scenario B**.

## PARALLEL TRACK B — BLUEPRINT DEBT (🔶 Fable tonight, zero Engine Body)
21. **W4: EVENTS_ZENFOLIO_DELIVERY.md** — formalize the locked QR system + its open
    verification items. Biggest documentation hole in the vault; pure writing.
22. **Theory Runs protocol doc** (08_TESTS) — absorb PAPER_TRIAL_RUNS' role (C15).
23. **Mechanical-fix pass spec** (C1, C6, C7, C9, C13 + decision-ledger D3 proposal) —
    written as PROPOSAL-009 for Will's one-shot ratify, applied after P008 settles.
24. **JOB_ENVELOPE_SPEC promotion note** + EXPORT.md upgrade with the battle-tested
    Lightroom recipe (audit §3 implied-systems).

## MILESTONE M1 DECLARED WHEN
n8n on PostgreSQL ✓ · workflow3 processes a real RESEARCH task end-to-end ✓ · Theory Runs
B + C executed with findings logged ✓ · SESSION_STATE + DASHBOARD match runtime ✓ ·
backups scheduled and Bitwarden confirmed ✓. Then P2 opens: Redis decision window
(7-day Postgres stability rule), Qdrant, monitoring, MEDIA, UGC app build.

## CONNECTED FILES
- [[POSTGRES_MIGRATION|PostgreSQL Migration]]
- [[SESSION_STATE|SESSION_STATE]]
- [[RESEARCH_ROUTE_SPEC|Research Route Specification]]
- [[PROPOSALS|Proposals]]
- [[N8N_MCP|n8n MCP]]
- [[TOOL_STATUS|Tool Status]]
