---
STATUS: FOR HUMAN REVIEW
AUDIENCE: Claude Chat (the thinking brain) — and Will
CREATED: 2026-06-29
CREATED_BY: Claude Code (headless) — BUILD-20260629-HERMES-LOOP-001
---

# HANDOFF → CLAUDE CHAT — the Hermes self-cuing loop is LIVE

You are the **brain**. As of 2026-06-29 there is a working machine that lets you
hand work to executors by writing one file. This handoff tells you what exists and
exactly how to drive it. Nothing here is CANON yet — it is FOR HUMAN REVIEW.

---

## TL;DR
- A **directive watcher** is running on the Engine Body. It watches one file:
  `C:\SFV_BLUEPRINT\CURRENT_DIRECTIVE.md`.
- When you (or Will) write a directive there with `STATUS: ACTIVE`, it is detected
  in ~1s at **zero token cost**, dispatched to the right executor, and the result
  lands in `99_INBOX\OUTPUTS\{DIRECTIVE_ID}_RESULT.md` + a row in `DECISION_LOG.md`.
- Four executors are live: `ollama` (free local), `claude`, `claude_code`, `codex`.
- It survives reboot (logon Scheduled Tasks). It is currently **idle**.
- Full spec: **`05_AI_LAYER/HERMES_LOOP.md`**. Build/decision trail:
  `00_DEV_LOG/HANDOFF_2026-06-29_HERMES_LOOP.md`.

---

## HOW YOU DRIVE IT (the only thing you must learn)
Overwrite `C:\SFV_BLUEPRINT\CURRENT_DIRECTIVE.md` with a directive:

```markdown
---
STATUS: ACTIVE
DIRECTIVE_ID: TASK-20260629-SOMETHING-001
EXECUTOR: ollama
---

<the task / prompt goes here — this whole body is what the executor receives>
```

Rules that matter:
- **Only `STATUS: ACTIVE` fires.** Leave it `IDLE` (or anything else) to stage a
  draft without running it. The file currently sits at `STATUS: IDLE`.
- **`DIRECTIVE_ID` must be unique** — a given id runs at most once (re-fire guard).
  Re-running means a new id.
- **One at a time.** There is no queue yet; a new directive overwrites the file.
  A running dispatch blocks the watcher until it returns (changes are buffered,
  not lost).
- Read the result back from `99_INBOX\OUTPUTS\{DIRECTIVE_ID}_RESULT.md`, decide the
  next step, write the next directive. That is the loop.

---

## PICK THE RIGHT EXECUTOR
| EXECUTOR | Use it for | Cost |
|----------|------------|------|
| `ollama` (default) | quick local reasoning, classification, summaries, drafts | free (qwen3:14b, local) |
| `claude` | harder single-prompt reasoning, judgment, writing | cloud (subscription) |
| `claude_code` | multi-file vault work that needs to read/edit many files | cloud (subscription) |
| `codex` | **routine coding + cross-reference guides — it can WRITE files into the vault** | cloud (ChatGPT sub) |

If you omit `EXECUTOR`, it defaults to free local `ollama` (so a forgotten field
never spends cloud money).

---

## LIVE STATE (2026-06-29)
- **Watcher:** running, single-instance, auto-restarts in ~5s if killed. Logon
  task `SFV_HermesLoopWatcher`.
- **Gateway:** moved onto logon task `SFV_HermesGateway` (+ auto-restart). Takes
  effect next reboot; the running gateway/Telegram was left untouched.
- **CURRENT_DIRECTIVE.md:** `STATUS: IDLE` (nothing pending).
- Machine code lives at `C:\Users\willa\AppData\Local\hermes\sfv_loop\`
  (`router.py`, `watcher.py`, keepalive, `persistence_selftest.py`).

## VERIFIED THIS SESSION (all passed)
Preflight, router selftest, watcher detect + re-fire guard, kill→auto-restart
single-instance, end-to-end for `claude` + `ollama` + `codex`, codex **write**
into the vault, and cold-start persistence (`PERSISTENCE_SELFTEST_PASS`).

---

## ⚠️ SAFETY NOTES (read before sending a codex directive)
- **`codex` runs UNSANDBOXED** on Windows (no OS sandbox exists) with the **vault**
  as its working root — it can read and write anything under `C:\SFV_BLUEPRINT`,
  including CANON and the loop's own code. Only send **trusted, specific** codex
  directives. Every change is git-tracked (auto-commit) so it's reviewable and
  revertible. Narrow the scope with the `SFV_CODEX_WORKDIR` env var if needed.
- Treat the loop as **build infra, not an autonomous goal-seeker** — it does what
  the directive says, once.

---

## OPEN FOR WILL / NEXT STEPS
1. **After next reboot:** confirm the gateway/Telegram auto-starts, and run
   `python C:\Users\willa\AppData\Local\hermes\sfv_loop\persistence_selftest.py`
   (expect `PERSISTENCE_SELFTEST_PASS`).
2. **Ratify** whether `05_AI_LAYER/HERMES_LOOP.md` + the `sfv_loop/` machine get
   promoted out of FOR HUMAN REVIEW to CANON.
3. **Decide** if codex should keep full-vault write, or be scoped to a subfolder
   (`SFV_CODEX_WORKDIR`).
4. **Not yet built (when you want them):** a multi-directive queue, a Telegram
   "done" ping on dispatch completion, per-executor cost guardrails.

## POINTERS
- Loop spec / contract: `05_AI_LAYER/HERMES_LOOP.md`
- Build + decision trail (Claude Code): `00_DEV_LOG/HANDOFF_2026-06-29_HERMES_LOOP.md`
- Hermes platform eval: `00_DEV_LOG/HERMES_EVAL.md`
- Live dispatch log: `99_INBOX/DECISION_LOG.md`

## CONNECTED FILES
- [[HERMES_LOOP|HERMES_LOOP.md]]
- [[CURRENT_DIRECTIVE|CURRENT_DIRECTIVE.md]]
- [[TOOL_STACK|TOOL_STACK.md]]
- [[INTEGRATIONS|INTEGRATIONS.md]]
- [[VAULT_DASHBOARD_DRAFT|VAULT_DASHBOARD_DRAFT.md]]
- [[HARDWARE_CONTEXT|HARDWARE_CONTEXT.md]]
- [[HANDOFF_2026-06-29_HERMES_LOOP|HANDOFF_2026-06-29_HERMES_LOOP.md]]
