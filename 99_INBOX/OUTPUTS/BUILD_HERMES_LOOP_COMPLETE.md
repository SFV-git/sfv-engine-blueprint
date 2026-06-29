---
STATUS: FOR HUMAN REVIEW
DIRECTIVE_ID: BUILD-20260629-HERMES-LOOP-001
CREATED: 2026-06-29
CREATED_BY: Claude Code (headless)
---

# BUILD COMPLETE — HERMES SELF-CUING LOOP

All six phases executed top-to-bottom. Every VERIFY gate passed before the next
phase began. Nothing promoted to CANON; no n8n / live service touched; no vault
file deleted. Claude spend ≈ $0.20 (cap $2.00).

## WHAT WAS BUILT
A zero-token self-cuing dispatch loop on the Hermes stack:
`brain → CURRENT_DIRECTIVE.md → watcher.py → router.py → executor → OUTPUTS → brain`.

Files (under `C:\Users\willa\AppData\Local\hermes\sfv_loop\`): `router.py`,
`watcher.py`, `watcher_keepalive.cmd`, plus runtime state (`processed_ids.txt`,
`watcher.log`, `watcher.lock`). One line added to `hermes_keepalive.cmd` to start
the watcher beside the gateway. Blueprint: `05_AI_LAYER/HERMES_LOOP.md` (FHR).
Handoff: `00_DEV_LOG/HANDOFF_2026-06-29_HERMES_LOOP.md`.

## VERIFY RESULTS
| Gate | Result | Evidence |
|------|--------|----------|
| VERIFY 0 — preflight | PASS | `PREFLIGHT_OK` / `AUTH_OK` / `WATCHFILES_OK` (both venvs) |
| VERIFY 1 — router selftest | PASS | `SELFTEST_PASS` (ollama echo + codex stub, no OpenAI) |
| VERIFY 2 — watcher detect + re-fire guard | PASS | sub-second detect; identical re-write "already processed", no re-dispatch |
| VERIFY 3 — kill → auto-restart, single-instance | PASS | relaunched ~5s, new lock PID, one logical watcher |
| VERIFY 4 — end-to-end claude + ollama | PASS | both RESULT files + DECISION_LOG rows; 3-line haiku; spend ≈ $0.20 |

## SUCCESS CRITERIA (from the directive)
- [x] `router.py` exists, `--selftest` prints `SELFTEST_PASS`
- [x] `watcher.py` exists, detects change <10s, guards against re-fire
- [x] keepalive relaunches watcher; single-instance enforced
- [x] End-to-end: claude-executor AND ollama-executor directives both produced RESULT files
- [x] `DECISION_LOG.md` has correct rows for all test dispatches
- [x] `HERMES_LOOP.md` written FOR HUMAN REVIEW; HANDOFF appended
- [x] No n8n/live-service touched; nothing promoted to CANON; claude spend < $2.00

## HONEST ASSESSMENT — SOLID vs FRAGILE
**Solid:**
- The trigger → dispatch → result → log path is clean and proven end-to-end for
  ollama (free) and claude (billed). BOM-safe I/O; idempotent RESULT overwrite.
- Re-fire guard (`processed_ids.txt`) and single-instance lock (atomic O_EXCL +
  stale reclaim) both verified, including the kill/restart case.
- codex is provably inert (stub, no network). claude calls are injection-safe
  (shell-less, body on STDIN). Three independent reviews found no remaining holes.

**Fragile / watch-outs:**
- Reboot persistence is indirect: the watcher rides on the gateway keepalive. A
  full reboot needs the gateway keepalive to auto-start (Scheduled Task not yet
  registered — elevation required, Will-only).
- One active directive at a time — no queue. A long dispatch blocks the watch
  loop (changes during it are buffered, not lost, but serialized).
- No completion notification wired in (no Telegram ping on result).
- PID accounting is non-obvious due to the uv-venv launcher→interpreter pair.

## SINGLE MOST IMPORTANT NEXT STEP
Decide reboot-persistence (register the gateway keepalive as an elevated
Scheduled Task vs accept Startup-folder/keepalive-only), then ratify promoting
`05_AI_LAYER/HERMES_LOOP.md` + the `sfv_loop/` machine out of FOR HUMAN REVIEW.

## CURRENT STATE
The watcher is running and idle (`CURRENT_DIRECTIVE.md` = STATUS: IDLE). To drive
the loop, write an ACTIVE directive per `05_AI_LAYER/HERMES_LOOP.md` §4. To stand
it down, stop `watcher_keepalive.cmd` + `watcher.py` (see HANDOFF).

## ADDENDUM (same session — Will directing live)
- **Reboot persistence now RESOLVED** (supersedes the "not yet registered" note
  above): the watcher auto-starts via the `SFV_HermesLoopWatcher` logon Scheduled
  Task (independent of the gateway). Proven by cold-start +
  `persistence_selftest.py` → `PERSISTENCE_SELFTEST_PASS`. After a real reboot,
  run `python sfv_loop\persistence_selftest.py`.
- **Codex** is installed (`codex-cli 0.142.4`) but not logged in. Per Will: he
  runs `codex login`, then the router stub is replaced with a real `codex exec`
  executor and tested. See HERMES_LOOP.md §8.
