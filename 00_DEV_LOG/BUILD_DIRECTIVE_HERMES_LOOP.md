---
STATUS: ACTIVE
DIRECTIVE_ID: BUILD-20260629-HERMES-LOOP-001
CREATED: 2026-06-29
CREATED_BY: Will (via Claude Chat / Opus 4.8 — the thinking brain)
EXECUTOR: Claude Code (headless, --dangerously-skip-permissions)
PURPOSE: Build the Hermes-spine self-cuing execution loop. The thinking brain (Claude / Antigravity)
         writes a directive; Hermes detects it in <1s at zero tokens; a router dispatches the work to
         the correct executor (Ollama foreman / claude CLI / codex); output lands in OUTPUTS; the brain
         reads it and writes the next directive. This directive builds that machine. It does NOT run it.
---

# BUILD DIRECTIVE — HERMES SELF-CUING LOOP (v1)

> You are Claude Code, the primary code agent for SFV Engine, running headless on the Engine Body.
> This is an "ultra goal": execute every phase below top-to-bottom. Each phase has a VERIFY gate —
> do not advance until the gate passes. If a gate fails twice, STOP, write a HANDOFF, and ping nothing
> (Will is reviewing live). Honor Blueprint Lock: nothing here promotes to CANON; all new docs are
> FOR HUMAN REVIEW. You are building infrastructure, not making architectural decisions.

## ARCHITECTURE (locked by Will — do not redesign)
- SPINE: Hermes. The loop lives as Python under the Hermes install, run by the existing keepalive daemon.
- BRAIN: claude CLI (now subscription-authed) for hard reasoning; Antigravity for sparing review.
- FOREMAN / HANDS: Ollama qwen3:14b (local, free) does file-writing and routine generation.
- BULK CODE: codex CLI (EXECUTOR: codex) — STUB ONLY this build; codex not yet installed.
- COMPLEX CODE: claude CLI in headless mode (EXECUTOR: claude_code).
- TRIGGER: a watchfiles watcher on C:\SFV_BLUEPRINT\CURRENT_DIRECTIVE.md (proven 98ms in HERMES_EVAL C5).
- CONTRACT: the directive file format already in use (see CURRENT_DIRECTIVE.md on disk) is the spec.

## ABSOLUTE CONSTRAINTS
- DO NOT touch n8n workflows or any live running service (WF1/WF2/WF4, Postgres, Ollama daemon config).
- DO NOT promote anything to CANON.
- DO NOT delete any existing vault file.
- DO NOT modify the running Hermes gateway process or its config.yaml model block.
- DO NOT route anything to the paid OpenAI/codex path in any test (codex stays a stub).
- DO NOT spend more than $2.00 of claude usage across all tests in this build.
- All new Python lives under: C:\Users\willa\AppData\Local\hermes\sfv_loop\  (create it; it is yours).
- All new blueprint docs go to: C:\SFV_BLUEPRINT\05_AI_LAYER\  as STATUS: FOR HUMAN REVIEW.

## MAX_TURNS: 120
## MAX_BUDGET_USD: 2.00

---

## CONTEXT TO READ FIRST (in order)
1. C:\SFV_BLUEPRINT\SESSION_STATE.md  (latest session blocks)
2. C:\SFV_BLUEPRINT\00_DEV_LOG\HERMES_EVAL.md  (esp. C3, C5, C7 — the proven primitives you are productionizing)
3. C:\SFV_BLUEPRINT\CURRENT_DIRECTIVE.md  (the directive format = your contract)
4. C:\Users\willa\AppData\Local\hermes\config.yaml  (confirm Ollama model block, mcp_servers.sfv-vault)
5. C:\Users\willa\AppData\Local\hermes\hermes_keepalive.cmd  (how the daemon is kept alive — you will add to this)

---

## PHASE 0 — PREFLIGHT (verify the ground is what the plan assumes)
0.1 Confirm Ollama answers: POST http://127.0.0.1:11434/api/generate {model:qwen3:14b, prompt:"say PREFLIGHT_OK", stream:false}. Expect PREFLIGHT_OK in response.
0.2 Confirm claude CLI is subscription-authed: run `claude -p "reply AUTH_OK"` and capture output. If it errors about API credits or asks for a key, STOP — auth is not fixed, write HANDOFF, halt.
0.3 Confirm Python in the Hermes telegram venv can import watchfiles:
    C:\Users\willa\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -c "import watchfiles; print('WATCHFILES_OK')"
    If missing, it is also in app\.venv — find which venv has it and USE THAT PYTHON for the watcher.
VERIFY 0: all three print their OK token. Record which python.exe has watchfiles. Do not proceed otherwise.

## PHASE 1 — THE ROUTER (the dispatch core, pure function, testable alone)
Create C:\Users\willa\AppData\Local\hermes\sfv_loop\router.py
It must:
1.1 Parse a directive markdown file: extract the YAML-ish frontmatter (STATUS, DIRECTIVE_ID, EXECUTOR)
    and the body. EXECUTOR may be one of: ollama | claude | claude_code | codex. Default = ollama.
1.2 Expose dispatch(directive_path) -> writes a result file to
    C:\SFV_BLUEPRINT\99_INBOX\OUTPUTS\{DIRECTIVE_ID}_RESULT.md and returns a status dict.
1.3 EXECUTOR routing:
    - ollama: POST the directive body as prompt to http://127.0.0.1:11434/api/generate (qwen3:14b, stream:false).
      Strip any <think>...</think> block from the response before writing (WF1 does this — match it).
    - claude: run `claude -p "<body>" --output-format json`, capture .result field.
    - claude_code: run `claude -p "<body>" --dangerously-skip-permissions` (for multi-file vault work).
    - codex: STUB — write a result file saying "CODEX STUB — not yet installed. Body was: ..." and return
      status=stubbed. Do NOT call any OpenAI endpoint.
1.4 Every dispatch appends one line to C:\SFV_BLUEPRINT\99_INBOX\DECISION_LOG.md:
    timestamp | DIRECTIVE_ID | executor | status | output_path  (match existing DECISION_LOG format if present).
1.5 BOM-safe: read directive as utf-8-sig; write outputs as utf-8 no-BOM (SESSION_STATE flags BOM breakage).
1.6 NEVER call the codex/OpenAI path. NEVER touch n8n. Idempotent: same directive twice = overwrite same RESULT file.
VERIFY 1: run `python router.py --selftest` which you implement to:
    (a) write a throwaway directive with EXECUTOR: ollama and body "Reply with exactly ROUTER_OLLAMA_OK",
        dispatch it, confirm RESULT file contains ROUTER_OLLAMA_OK.
    (b) dispatch a directive with EXECUTOR: codex, confirm status=stubbed and NO network call to openai.
    Print SELFTEST_PASS only if both hold. Gate on SELFTEST_PASS.

## PHASE 2 — THE WATCHER (the zero-token trigger)
Create C:\Users\willa\AppData\Local\hermes\sfv_loop\watcher.py
2.1 Use watchfiles.watch() on C:\SFV_BLUEPRINT\CURRENT_DIRECTIVE.md (the file proven at 98ms in C5).
2.2 On change: read the file. If frontmatter STATUS == ACTIVE and DIRECTIVE_ID has not already been
    processed (track processed IDs in sfv_loop\processed_ids.txt), call router.dispatch(path).
    If STATUS != ACTIVE, ignore (this prevents re-firing on drafts).
2.3 After successful dispatch, append the DIRECTIVE_ID to processed_ids.txt so the same directive
    never double-fires (SESSION_STATE flags stranded/duplicate jobs as a known failure class — prevent it).
2.4 Zero tokens for the watch itself (pure local FS event + local file read). Only dispatch spends.
2.5 Log watcher lifecycle to sfv_loop\watcher.log (started, change detected, dispatched, ignored-draft).
2.6 Wrap dispatch in try/except — a bad directive must log an error and keep the watcher alive, never crash it.
VERIFY 2: start watcher.py in the background. Programmatically write a test directive to CURRENT_DIRECTIVE.md
    with STATUS: ACTIVE, DIRECTIVE_ID: TEST-WATCH-001, EXECUTOR: ollama, body "Reply WATCHER_OK".
    Within 10s, confirm OUTPUTS\TEST-WATCH-001_RESULT.md exists and contains WATCHER_OK. Then write the SAME
    directive again unchanged — confirm it does NOT re-dispatch (processed_ids guard). Gate on both.

## PHASE 3 — PERSISTENCE (survive alongside the gateway)
3.1 Add a launch line for watcher.py to the keep-alive wrapper hermes_keepalive.cmd so it starts with the
    gateway and relaunches if it dies. Use the watchfiles-capable python.exe found in Phase 0.
    DO NOT alter the existing gateway launch line — ADD a new background start for the watcher.
3.2 Make watcher startup idempotent (if already running, don't spawn a second — check via a lockfile
    sfv_loop\watcher.lock containing the PID).
VERIFY 3: kill watcher.py; confirm keepalive relaunches it within ~10s; confirm only ONE watcher runs
    (no duplicate from the lockfile guard). Gate on single-instance auto-restart.

## PHASE 4 — END-TO-END LOOP PROOF (the whole thing, once)
4.1 Simulate the real loop: write a directive with EXECUTOR: claude (the brain), body asking it to
    "Write a 3-line haiku about a silver fish and output only the haiku." Confirm RESULT file appears,
    contains 3 lines, and DECISION_LOG logged it. (This is the ONE claude-spend test; keep it tiny.)
4.2 Write a directive with EXECUTOR: ollama, body "List 5 SFV content branches from memory or reply
    UNKNOWN." Confirm RESULT lands (foreman path, zero cost).
4.3 Confirm DECISION_LOG.md now has rows for both, with correct executor + output_path.
VERIFY 4: both RESULT files exist, DECISION_LOG has both rows, total claude spend < $2.00. Gate on all.

## PHASE 5 — DOCUMENT (FOR HUMAN REVIEW, for Will)
Write C:\SFV_BLUEPRINT\05_AI_LAYER\HERMES_LOOP.md  (STATUS: FOR HUMAN REVIEW) containing:
- Architecture diagram (text) of the loop: brain -> CURRENT_DIRECTIVE.md -> watcher -> router -> executor -> OUTPUTS -> brain.
- The directive contract (frontmatter fields, EXECUTOR values, STATUS gating).
- File inventory: every file you created under sfv_loop\ and what it does.
- How to drive it: exactly what a brain (Claude/Antigravity) writes to CURRENT_DIRECTIVE.md to cue a task.
- Known limits / not-yet-done: codex stub, no multi-directive queue yet (one active directive at a time),
  no Telegram notify wired into the loop yet, reboot-persistence still depends on keepalive (not a Task).
- A "NEXT STEPS for Will to ratify" section.
Also append a short SESSION block to C:\SFV_BLUEPRINT\00_DEV_LOG\HANDOFF_2026-06-29_HERMES_LOOP.md
summarizing what was built, every VERIFY result, and anything that felt rough.

## SUCCESS CRITERIA (all must hold)
- [ ] router.py exists, --selftest prints SELFTEST_PASS
- [ ] watcher.py exists, detects directive change <10s, guards against re-fire
- [ ] keepalive relaunches watcher; single-instance enforced
- [ ] End-to-end: claude-executor directive AND ollama-executor directive both produced RESULT files
- [ ] DECISION_LOG.md has correct rows for all test dispatches
- [ ] HERMES_LOOP.md written FOR HUMAN REVIEW; HANDOFF appended
- [ ] No n8n/live-service touched; nothing promoted to CANON; claude spend < $2.00

## HUMAN_GATE_TRIGGERS (STOP, write HANDOFF, halt)
- claude auth is not subscription (Phase 0.2 fails)
- Any VERIFY gate fails twice
- You would need to touch n8n or a live service to proceed
- claude spend approaches $1.50
- watchfiles import fails in BOTH venvs

## COMPLETION
When all phases pass, write C:\SFV_BLUEPRINT\99_INBOX\OUTPUTS\BUILD_HERMES_LOOP_COMPLETE.md:
what was built, every VERIFY result (pass/fail), files created, claude spend total, honest assessment
of where the loop is solid vs fragile, and the single most important next step. Do not promote to CANON.
