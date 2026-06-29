---
STATUS: FOR HUMAN REVIEW
VERSION: v1
OWNER: WILL
CREATED: 2026-06-29
CREATED_BY: Claude Code (BUILD-20260629-HERMES-LOOP-001)
---

# HERMES SELF-CUING LOOP

The Hermes loop is the self-cuing execution spine for the SFV Engine. A
"thinking brain" (Claude / Antigravity) writes a directive to a single watched
file; a watcher detects the change locally at zero token cost, a router routes
the work to the correct executor, the result is dropped in `99_INBOX/OUTPUTS/`,
and the brain reads that result and writes the next directive. The watch step is
free; only the dispatch to a cloud executor spends.

This document describes the machine as built under
`C:\Users\willa\AppData\Local\hermes\sfv_loop\`. It is FOR HUMAN REVIEW —
nothing here is CANON.

---

## 1. ARCHITECTURE

```
        +-----------------------------------------------------------+
        |                         BRAIN                             |
        |        (Claude / Antigravity — the thinking layer)        |
        |   reasons, decides the next task, WRITES a directive      |
        +-----------------------------------------------------------+
                                   |
                                   |  writes frontmatter + body
                                   v
        +-----------------------------------------------------------+
        |            C:\SFV_BLUEPRINT\CURRENT_DIRECTIVE.md           |
        |        the single watched contract file (one at a time)   |
        +-----------------------------------------------------------+
                                   |
                                   |  OS-native FS change event (~98ms, 0 tokens)
                                   v
        +-----------------------------------------------------------+
        |                       watcher.py                          |
        |  watchfiles.watch() -> parse frontmatter                  |
        |  gate: STATUS == ACTIVE  AND  DIRECTIVE_ID unseen          |
        |  guards: processed_ids.txt (re-fire) + watcher.lock (1x)   |
        +-----------------------------------------------------------+
                                   |
                                   |  router.dispatch(path)
                                   v
        +-----------------------------------------------------------+
        |                        router.py                          |
        |  parse_directive() -> pick executor                       |
        +-----------------------------------------------------------+
              |            |              |                |
              v            v              v                v
         +--------+   +---------+   +-------------+   +-----------+
         | ollama |   | claude  |   | claude_code |   |   codex   |
         | qwen3  |   | -p json |   | --dsp flag  |   |  (STUB)   |
         | local  |   | cloud   |   | cloud/vault |   | no call   |
         +--------+   +---------+   +-------------+   +-----------+
              |            |              |                |
              +------------+------+-------+----------------+
                                  |
                                  |  writes {DIRECTIVE_ID}_RESULT.md
                                  v
        +-----------------------------------------------------------+
        |        C:\SFV_BLUEPRINT\99_INBOX\OUTPUTS\                  |
        |        + one row appended to 99_INBOX\DECISION_LOG.md      |
        +-----------------------------------------------------------+
                                  |
                                  |  brain reads the RESULT
                                  v
                              (back to BRAIN — write next directive)
```

The loop is closed by a human or brain reading `OUTPUTS/` and authoring the next
`CURRENT_DIRECTIVE.md`. There is no automated brain-side re-trigger yet (see
Known Limits).

---

## 2. THE DIRECTIVE CONTRACT

A directive is a markdown file with a `---`-delimited frontmatter block at the
top, followed by the body (the actual task/prompt). The router reads frontmatter
keys case-insensitively and uppercases them internally.

### Frontmatter fields the loop reads

| Field          | Required | Meaning                                                              |
|----------------|----------|---------------------------------------------------------------------|
| `STATUS`       | Yes      | Gate. Only `ACTIVE` fires a dispatch. Anything else is ignored.     |
| `DIRECTIVE_ID` | Yes      | Unique id. Used for the result filename, the log row, and re-fire guard. |
| `EXECUTOR`     | No       | Which engine runs the body. Defaults to `ollama` if absent/invalid. |

Other frontmatter fields (CREATED, CREATED_BY, PURPOSE, etc.) are allowed and
ignored by the loop — they are for humans.

### EXECUTOR values

| Value         | Routes to                                                                 | Cost          |
|---------------|---------------------------------------------------------------------------|---------------|
| `ollama`      | Local `qwen3:14b` via `http://127.0.0.1:11434/api/generate` (stream:false). `<think>...</think>` stripped from the response (WF1 parity). | Free (local)  |
| `claude`      | `claude -p --output-format json` with the body piped on STDIN; the `.result` field is captured. | Cloud, billed |
| `claude_code` | `claude -p --dangerously-skip-permissions` with the body on STDIN (headless multi-file vault work); raw stdout captured. | Cloud, billed |
| `codex`       | `codex exec` non-interactive, body on STDIN; final message via `-o`. **WRITE-ENABLED**: runs unsandboxed (Windows has no codex sandbox) with working root = the vault, so it reads across the vault and writes files (cross-ref guides, routine coding). **Trusted directives only.** Override root with `SFV_CODEX_WORKDIR`. | Cloud (ChatGPT sub) |

Any unrecognised `EXECUTOR` value is normalised to `ollama` by
`parse_directive()`. The directive body is passed to claude on STDIN (never as a
shell argument), so arbitrary directive text cannot be misparsed or injected as
a command.

### STATUS gating

- `STATUS: ACTIVE` → the watcher dispatches (once).
- Any other STATUS (e.g. `DRAFT`, `IDLE`, `FOR HUMAN REVIEW`, empty) → logged and
  ignored. This is deliberate so brains can stage drafts in the file without
  firing them.
- The re-fire guard is independent of STATUS: even an ACTIVE directive whose
  `DIRECTIVE_ID` is already in `processed_ids.txt` will not run again. To re-run,
  use a new `DIRECTIVE_ID`.

---

## 3. FILE INVENTORY

All under `C:\Users\willa\AppData\Local\hermes\sfv_loop\`.

| File                   | Role |
|------------------------|------|
| `router.py`            | The dispatch core. Pure, testable. `parse_directive()` extracts STATUS / DIRECTIVE_ID / EXECUTOR + body (BOM-safe via `utf-8-sig`). `dispatch()` routes the body to the chosen executor, writes `99_INBOX\OUTPUTS\{DIRECTIVE_ID}_RESULT.md` as UTF-8 no-BOM, appends a row to `DECISION_LOG.md`, and returns a status dict. Errors are caught and written into the RESULT (`status=error`) — dispatch never raises to its caller. CLI: `--selftest` (VERIFY 1 gate; prints `SELFTEST_PASS`/`SELFTEST_FAIL`) and `--dispatch <path>`. |
| `watcher.py`           | The zero-token trigger. `watchfiles.watch()` on `CURRENT_DIRECTIVE.md`. On each change it parses the file and dispatches only when `STATUS == ACTIVE` and the `DIRECTIVE_ID` is unseen. Marks the id in-memory immediately (so duplicate FS events for one write don't double-fire), then persists it after dispatch. Dispatch is wrapped in try/except so a bad directive logs and the watcher survives. Holds a single-instance lock (atomic `O_CREAT\|O_EXCL`, with stale-PID reclaim) and writes lifecycle lines to `watcher.log`. |
| `watcher_keepalive.cmd`| A 5-second relaunch loop that runs `watcher.py` with the `hermes-agent\venv` python (the watchfiles-capable interpreter). If the watcher dies it is relaunched within ~5s. Launched at logon by the Scheduled Task (see §5). |
| `watcher_launch.vbs`   | Hidden launcher: starts `watcher_keepalive.cmd` with no visible console window. The Scheduled Task runs this. |
| `sfv_watcher_task.xml` | Task Scheduler definition for `SFV_HermesLoopWatcher` (logon trigger → `watcher_launch.vbs`, RestartOnFailure). Register it elevated (see §5). |
| `persistence_selftest.py` | The reboot self-test: confirms a watcher is alive (live lock PID) and the loop still dispatches (writes an ACTIVE directive, waits for the RESULT). Prints `PERSISTENCE_SELFTEST_PASS`. Run after a reboot. |
| `processed_ids.txt`    | Append-only ledger of `DIRECTIVE_ID`s already dispatched, one per line. Loaded on startup into a set; this is the re-fire guard that survives restarts and crashes. |
| `watcher.log`          | Plain-text lifecycle log (`[timestamp] message`): started, change detected, dispatched, ignored-draft, errors. Logging failures are swallowed so logging can never crash the watcher. |
| `watcher.lock`         | Single-instance lockfile containing the owning watcher's PID. On startup the watcher atomically creates it; if a live process owns it, the new instance exits quietly; a stale lock (dead PID) is reclaimed. Removed on clean exit via `atexit`. |

Incidental artifacts also present in the directory (not part of the contract):
`__pycache__/` (Python bytecode cache), `_selftest/` (throwaway directives the
`--selftest` run generates), and `CURRENT_DIRECTIVE.bak.md` (a backup of the
directive file as it was before this build's tests).

---

## 4. HOW TO DRIVE IT

To cue a task, a brain writes a directive to
`C:\SFV_BLUEPRINT\CURRENT_DIRECTIVE.md` with `STATUS: ACTIVE`, a fresh
`DIRECTIVE_ID`, the desired `EXECUTOR`, and the task as the body. The watcher
picks it up within ~1s. Write the file as UTF-8 (a BOM is tolerated).

Concrete example — route a summary task to the free local foreman:

```markdown
---
STATUS: ACTIVE
DIRECTIVE_ID: TASK-20260629-SUMMARY-001
EXECUTOR: ollama
---

Summarise the following note in three bullet points, then output only the
bullets:

<paste the note text here>
```

What happens:
1. The watcher fires within ~1s, sees `STATUS: ACTIVE` and an unseen id.
2. `router.dispatch()` sends the body to qwen3:14b locally (zero cloud cost).
3. The result is written to
   `C:\SFV_BLUEPRINT\99_INBOX\OUTPUTS\TASK-20260629-SUMMARY-001_RESULT.md`.
4. A row is appended to `99_INBOX\DECISION_LOG.md`.
5. `TASK-20260629-SUMMARY-001` is appended to `processed_ids.txt`.

To send the same work to a cloud brain instead, change one line to
`EXECUTOR: claude` (single-prompt reasoning) or `EXECUTOR: claude_code`
(multi-file vault work). To stage a draft without firing, set any STATUS other
than `ACTIVE`. To re-run a task, change the `DIRECTIVE_ID` (re-using an id is
blocked by the re-fire guard).

Result files follow the pattern: a `# RESULT -- {DIRECTIVE_ID}` header, an
executor/status/timestamp block, a `---` fence, then the executor's output.

---

## 5. PERSISTENCE

The watcher has its own dedicated logon persistence, fully **independent of the
Hermes gateway** (the gateway's own autostart VBS is untouched — this avoids any
double-gateway conflict):

```
logon  ->  Scheduled Task "SFV_HermesLoopWatcher"  (LogonTrigger, RestartOnFailure)
       ->  watcher_launch.vbs       (hidden, no console window)
       ->  watcher_keepalive.cmd    (5s relaunch loop)
       ->  watcher.py               (single-instance via watcher.lock)
```

- If the watcher process dies, `watcher_keepalive.cmd` relaunches it within ~5s.
- The single-instance lockfile guarantees a second copy can never run.

Register / refresh the task from an **elevated** PowerShell:

```powershell
Register-ScheduledTask -Xml (Get-Content 'C:\Users\willa\AppData\Local\hermes\sfv_loop\sfv_watcher_task.xml' -Raw) -TaskName 'SFV_HermesLoopWatcher' -Force
```

Verified 2026-06-29 by cold-start: the watcher was killed and the lock cleared,
the task was triggered, the watcher auto-started, and `persistence_selftest.py`
dispatched a directive through the loop end-to-end (`PERSISTENCE_SELFTEST_PASS`).
After a real reboot, run `python sfv_loop\persistence_selftest.py` to re-confirm.

NOTE: this is a **logon** trigger (fires after Will logs in), which is the right
scope because the loop needs the user session (PATH, Ollama, the claude CLI). It
is not a pre-login SYSTEM boot task.

**Gateway persistence (2026-06-29):** the Hermes gateway was also moved onto a
logon Scheduled Task `SFV_HermesGateway` → `hermes_gateway_launch.vbs` (hidden) →
`hermes_keepalive.cmd` (which loops `hermes gateway run` with auto-restart). The
old Startup-folder `Hermes_Gateway.vbs` (which launched `gateway run` directly,
no auto-restart) was renamed to `.disabled` so there is exactly ONE gateway
launch path. This activates on the next logon/reboot; the currently-running
gateway was left untouched. To revert: rename the Startup VBS back and
`Unregister-ScheduledTask SFV_HermesGateway`.

---

## 6. END-TO-END VERIFICATION (2026-06-29)

All gates were run on the Engine Body during the build. Every gate passed before
the next phase began.

| Gate     | What was tested                                                        | Result |
|----------|------------------------------------------------------------------------|--------|
| VERIFY 0 | Preflight: Ollama qwen3:14b, claude CLI auth, watchfiles import        | PASS — `PREFLIGHT_OK`, `AUTH_OK`, `WATCHFILES_OK` (present in both venvs) |
| VERIFY 1 | `router.py --selftest` (ollama echo + codex stub, no OpenAI call)      | PASS — `SELFTEST_PASS` |
| VERIFY 2 | Watcher detects directive change + re-fire guard                       | PASS — detected sub-second; identical re-write logged "already processed", no re-dispatch |
| VERIFY 3 | Kill watcher → keepalive auto-restart, single-instance                 | PASS — restarted in ~5s with a new lock PID; exactly one watcher (uv venv launcher→interpreter = one logical instance) |
| VERIFY 4 | E2E: `claude` haiku directive + `ollama` branches directive            | PASS — both RESULT files landed via the live watcher; both DECISION_LOG rows correct; claude spend ≈ $0.20 total (well under the $2.00 cap) |
| PERSIST  | Cold-start: kill watcher + clear lock → trigger logon Scheduled Task   | PASS — watcher auto-started via the task; `persistence_selftest.py` dispatched a directive end-to-end → `PERSISTENCE_SELFTEST_PASS` |
| CODEX    | Wire real `codex exec` + E2E `EXECUTOR: codex` directive               | PASS — `--selftest` returned `ROUTER_CODEX_OK`; live loop dispatched `E2E-CODEX-001` → RESULT with `CODEX_LOOP_OK` |

Artifacts from the proof runs:
`99_INBOX\OUTPUTS\E2E-CLAUDE-HAIKU-001_RESULT.md` (clean 3-line haiku),
`99_INBOX\OUTPUTS\E2E-OLLAMA-BRANCHES-001_RESULT.md`, and their two rows in
`DECISION_LOG.md`.

This build was also reviewed by three independent read-only review agents
(correctness, security/contract, and documentation). Their two actionable
findings — a TOCTOU race in the lockfile and a `shell=True` command-construction
surface — were both fixed before Phase 4 (atomic `O_EXCL` lock; shell-less claude
calls with the body passed on STDIN).

---

## 7. KNOWN LIMITS / NOT-YET-DONE

- **codex is WRITE-ENABLED and UNSANDBOXED (Will's call, 2026-06-29).**
  `EXECUTOR: codex` runs `codex exec --dangerously-bypass-approvals-and-sandbox
  --cd <vault>` — the only way codex can write on Windows (its seatbelt/landlock
  sandbox is macOS/Linux-only). So codex has full local read/write while a
  directive runs. **Risk:** a codex directive can modify anything reachable from
  the vault root (incl. CANON, `.git`, the loop's own code). Mitigations: only
  Will/the brain author directives; git tracks every change (auto-commit). Narrow
  the blast radius any time by setting `SFV_CODEX_WORKDIR` to a subfolder.
- **No multi-directive queue.** The loop watches exactly one file
  (`CURRENT_DIRECTIVE.md`) and handles one active directive at a time. There is
  no queue, no priority, no parallel dispatch. A new directive overwrites the
  watched file. While a `claude`/`ollama` dispatch is running, the watch loop is
  blocked; a change written during that window is processed when the dispatch
  returns (watchfiles buffers it), not dropped.
- **No Telegram notify wired into the loop.** Completion is observable only via
  the RESULT file, `DECISION_LOG.md`, and `watcher.log`. There is no push
  notification when a dispatch finishes, even though Hermes itself can send
  Telegram.
- **Reboot-persistence: RESOLVED (logon) for the watcher.** It auto-starts via
  the `SFV_HermesLoopWatcher` logon Scheduled Task (§5), independent of the
  gateway. This is a logon trigger (fires once Will logs in), not a pre-login
  SYSTEM boot task — which is correct, because the loop needs the user session
  (PATH, Ollama, the claude CLI).
- **The gateway is now on its own logon Task** (`SFV_HermesGateway`) with
  auto-restart via `hermes_keepalive.cmd`; the old Startup VBS was disabled.
  Takes effect next logon/reboot (see §5).

---

## 8. NEXT STEPS FOR WILL TO RATIFY

1. **Reboot-persistence: DONE** for BOTH the watcher (`SFV_HermesLoopWatcher`) and
   the gateway (`SFV_HermesGateway`) via logon Scheduled Tasks (§5). Verify after
   your next reboot: confirm the gateway/Telegram comes up and
   `python sfv_loop\persistence_selftest.py` → `PERSISTENCE_SELFTEST_PASS`.
2. **Codex: WRITE-ENABLED + tested.** `EXECUTOR: codex` writes into the vault
   (proven: `E2E-CODEX-WRITE-001` created a cross-reference file). It runs
   UNSANDBOXED — keep codex directives trusted and review `git` after codex runs.
3. **Decide on a queue / inbox model** if more than one directive at a time is
   ever needed (e.g. a `PENDING_DIRECTIVES/` folder the watcher drains), vs.
   keeping the deliberate one-at-a-time discipline.
4. **Wire a notify** (Telegram via Hermes) into `router.dispatch()` completion if
   push alerts are wanted when a result lands.
5. **Set cost guardrails** for the `claude` / `claude_code` paths (per-dispatch
   budget, an allow-list of which executors a directive may request) before the
   loop is left running unattended for long stretches. Today the safe default is
   that an unspecified `EXECUTOR` routes to free local ollama.
6. **Ratify whether this document and the `sfv_loop/` machine are promoted**
   beyond FOR HUMAN REVIEW.

## CONNECTED FILES
- [[HERMES_EVAL|Hermes Agent Evaluation]]
- [[SESSION_STATE|Session State]]
- [[DECISION_LOG|Decision Log]]
- [[MODEL_ROUTING|Model Routing]]
- [[COMPRESSED_CONTEXT|Compressed Context]]
