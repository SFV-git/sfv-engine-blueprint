---
STATUS: FOR HUMAN REVIEW
OWNER: WILL
CREATED: 2026-06-29
CREATED_BY: Claude Code (headless) — BUILD-20260629-HERMES-LOOP-001
---

# HANDOFF — HERMES SELF-CUING LOOP BUILD (2026-06-29)

## SESSION SUMMARY
Executed `00_DEV_LOG/BUILD_DIRECTIVE_HERMES_LOOP.md` (directive STATUS: ACTIVE,
authored by Will via Opus 4.8) top-to-bottom as an ultra-goal. Built the
Hermes-spine self-cuing execution loop: brain writes a directive →
`CURRENT_DIRECTIVE.md` → watcher detects (zero token) → router dispatches to the
right executor → result lands in `99_INBOX/OUTPUTS/` + `DECISION_LOG.md`. Built
the machine; left it idle. No CANON promoted. No n8n / live service touched.

All new Python lives under `C:\Users\willa\AppData\Local\hermes\sfv_loop\`; the
blueprint doc went to `05_AI_LAYER/HERMES_LOOP.md` as FOR HUMAN REVIEW.

## FILES CREATED / CHANGED
New (under `...\hermes\sfv_loop\`):
- `router.py` — dispatch core (parse, route, write RESULT, log, `--selftest`).
- `watcher.py` — watchfiles trigger; processed_ids re-fire guard; atomic lockfile.
- `watcher_keepalive.cmd` — 5s relaunch loop for the watcher.
- `processed_ids.txt`, `watcher.log`, `watcher.lock` — runtime state.
- `CURRENT_DIRECTIVE.bak.md` — backup of the directive file before tests.

Changed:
- `C:\Users\willa\AppData\Local\hermes\hermes_keepalive.cmd` — ADDED one line to
  start `watcher_keepalive.cmd` alongside the gateway. The gateway launch line was
  NOT touched.
- `05_AI_LAYER/HERMES_LOOP.md` (NEW, FHR) — full architecture + contract + inventory.
- `99_INBOX/DECISION_LOG.md` — dispatch rows appended by the router (selftest + E2E).
- `99_INBOX/OUTPUTS/` — RESULT files for selftest + the two E2E proofs.
- `CURRENT_DIRECTIVE.md` — left in STATUS: IDLE (loop live but quiet).

## VERIFY RESULTS (every gate honored; no phase advanced until its gate passed)
- **VERIFY 0 — PASS.** Ollama `qwen3:14b` → `PREFLIGHT_OK`; `claude -p` →
  `AUTH_OK` (subscription, no key error); `watchfiles` imports in BOTH venvs.
  Watcher uses `hermes-agent\venv\Scripts\python.exe`.
- **VERIFY 1 — PASS.** `router.py --selftest` printed `SELFTEST_PASS`: ollama
  echo returned the token; codex returned `status=stubbed` with no OpenAI call.
- **VERIFY 2 — PASS.** Watcher detected a written directive sub-second and the
  RESULT landed (`TEST-WATCH-001`); an identical re-write logged
  "already processed" with NO re-dispatch (RESULT timestamp unchanged).
- **VERIFY 3 — PASS.** Killed the live watcher; `watcher_keepalive.cmd`
  relaunched it in ~5s with a NEW lock PID; single-instance held (the two PIDs
  seen are the uv-venv launcher→interpreter pair = one logical watcher).
- **VERIFY 4 — PASS.** `EXECUTOR: claude` haiku directive produced a clean
  3-line RESULT in ~11s; `EXECUTOR: ollama` directive produced a RESULT in ~21s
  (model correctly returned `UNKNOWN`); both DECISION_LOG rows correct. Total
  claude spend ≈ $0.20 (cap $2.00).

## HARDENING (from 3 read-only review subagents)
- **Lockfile TOCTOU (HIGH)** → fixed: atomic `os.open(O_CREAT|O_EXCL)` with
  stale-PID reclaim, so two racing watchers cannot both acquire.
- **`shell=True` claude call (MED)** → fixed: `claude.exe` is native (not a .cmd
  shim), so calls are now shell-less and the directive body is piped on STDIN —
  no command-line/cmd.exe parse or injection surface.
- Re-ran `--selftest` after hardening: still `SELFTEST_PASS`.

## WHAT FELT ROUGH / NOTES FOR WILL
- **uv venv trampoline:** one `python watcher.py` shows as TWO PIDs (a launcher +
  the real cpython-3.11 interpreter). Single-instance is still correct, but PID
  counting must look at the lock holder / the interpreter, not raw process count.
- **Reboot persistence is not self-standing.** The watcher starts only when the
  gateway keepalive (re)launches. Editing `hermes_keepalive.cmd` does not affect
  an already-running keepalive. For true reboot-survival, register the gateway
  keepalive as a Scheduled Task (elevated, one-time) — same caveat HERMES_EVAL
  raised for the gateway itself.
- **The watcher is RUNNING right now** (started this session for testing, via
  `watcher_keepalive.cmd`, detached). It is idle because `CURRENT_DIRECTIVE.md`
  is STATUS: IDLE. To stop it until you ratify: kill the `watcher_keepalive.cmd`
  cmd process and the `watcher.py` python process (delete `watcher.lock` if
  stale). To drive it: write an ACTIVE directive per `05_AI_LAYER/HERMES_LOOP.md`.
- **Default executor is free local ollama** — an ACTIVE directive that forgets
  `EXECUTOR` will NOT spend cloud money; it routes to qwen3:14b.

## NEXT STEP (single most important)
Decide reboot-persistence (Scheduled Task vs keepalive-only) and whether to
promote `05_AI_LAYER/HERMES_LOOP.md` + the `sfv_loop/` machine out of FOR HUMAN
REVIEW. Everything else (codex install, queue model, Telegram notify, cost
guardrails) is enumerated in HERMES_LOOP.md §8.

## CONNECTED FILES
- [[HERMES_LOOP|Hermes Loop]]
- [[HERMES_EVAL|Hermes Agent Evaluation]]
- [[SESSION_STATE|Session State]]
- [[BUILD_DIRECTIVE_HERMES_LOOP|Build Directive — Hermes Loop]]
