---
STATUS: FOR HUMAN REVIEW
OWNER: WILL
CREATED_BY: Claude Code (Hermes Eval, Opus 4.8) — 2026-06-27
PURPOSE: Handoff for the NEXT Claude session. The Hermes Agent eval is DONE and written to
  HERMES_EVAL.md. This frames current state, what is blocked on Will, and exactly how to
  resume (mainly: finish C6 Telegram once Will provides a bot token + chat_id).
---

# HANDOFF → NEXT CLAUDE SESSION (Hermes Agent Eval)

## Where things stand (one paragraph)
The Hermes Agent eval is **complete and written** to `00_DEV_LOG/HERMES_EVAL.md`
(STATUS: FOR HUMAN REVIEW, untracked in git — not yet committed). Result: **5 PASS /
1 PARTIAL / 1 PENDING**. Hermes is **installed and functional** on Engine Body but left
**dormant on purpose** (eval-only) — no daemon running, no cron jobs, no auto-start, nothing
firing paid calls. The only eval step not finished is **C6 (Telegram)**, which is blocked on
Will creating a bot and supplying a token + chat_id. Will did NOT do anything after the eval
and is starting a fresh session.

## The single thing to read first
`00_DEV_LOG/HERMES_EVAL.md` — full per-criterion detail, every install path, workaround, and
setup time. This handoff is the short version + how to resume.

## What was completed (verified, not assumed)
- **C1 Install — PASS.** Official installer `iex (irm https://hermes-agent.nousresearch.com/install.ps1)`
  FAILED (uv could not spawn nested powershell: "EPERM uv_spawn"). Installed manually from source
  with `uv` instead. Lives at `C:\Users\willa\AppData\Local\hermes\` (`app\` = source + `.venv`;
  `bin\hermes.cmd` = global shim on User PATH; `HERMES_HOME` set). Hermes **v0.17.0**, Python **3.13.14**.
- **C2 Daemon persistence — PASS (caveat).** Daemon = `hermes gateway run`. Auto-restart DEMONSTRATED
  (killed PID 20796 → wrapper relaunched PID 45140 in ~3s). NOT native on Windows (`gateway install`
  = systemd/launchd only). Used a no-admin Startup shortcut + `hermes_keepalive.cmd`. Full Task
  Scheduler needs an **elevated** prompt (XML provided at `...\hermes\hermes_task.xml`).
- **C3 Anthropic — PASS (premise corrected).** There is **NO `ANTHROPIC_API_KEY`** in `n8n_env.ps1`
  or anywhere on the system. Not needed: the `claude` CLI (`C:\Users\willa\.local\bin\claude`) is
  authenticated via the Claude subscription. Hermes spawned `claude -p` (zero-token `--no-agent`
  cron) and captured `CONNECTED`.
- **C4 Ollama qwen3:14b — PASS.** Required overriding `model.context_length=65536` +
  `model.ollama_num_ctx=65536` (Hermes enforces a 64K-context minimum; qwen3:14b ships at 40,960).
  Returned `OLLAMA_OK`. Config saved in `...\hermes\config.yaml`.
- **C5 File watch (CRITICAL / deal-breaker) — PARTIAL.** **Hermes has NO native file-watch.** Its
  cron is a 60-second poll (fails the <10s bar), and the `file_watch:` config our
  `HERMES_INTEGRATION.md` architecture assumes **does not exist**. The bundled `watchfiles` library
  DOES work: a ~20-line wrapper detected a change in **98 ms with 0 tokens**. So the zero-token
  directive watcher is achievable on the stack but is a small custom wrapper, **not a Hermes feature**.
- **C7 Headless spawn — PASS.** Hermes `--no-agent` cron ran `claude -p ... --output-format json`,
  captured clean JSON `"result":"HEADLESS_OK"`.

## DECISION REQUIRED (Will — Claude does NOT decide)
1. **Adoption.** 5 PASS / 1 PARTIAL / 1 pending; neither hard deal-breaker (C2, C3) failed; no 3+
   FAILs → under the adoption rule this is "Will ratifies adoption" territory. The one judgment call
   is **C5**: accept the bundled-`watchfiles` wrapper as the zero-token watcher (it isn't native to
   Hermes), or treat the missing native watcher as a reason to reconsider / build Option B.
2. **Telegram (C6).** Will must create the bot (Claude cannot use BotFather).
3. **Model.** This eval ran on **Opus 4.8**; `CLAUDE.md` says Sonnet-only unless told. Decide which
   model the next session uses (cost).
4. **Commit?** `HERMES_EVAL.md` and this handoff are untracked — decide whether to commit.

## NEXT SESSION — priority order
1. **Finish C6.** Get token + chat_id from Will (steps below), wire into Hermes, send test, update
   `HERMES_EVAL.md` C6 → PASS/PARTIAL pending Will's receipt confirmation.
2. **If Will adopts:** run the integration session (NOT done during eval) — activate persistence via
   elevated Task Scheduler (`hermes_task.xml`), build the real `watchfiles` directive watcher, configure
   Telegram delivery, seed the 10 skills listed in `05_AI_LAYER/HERMES_INTEGRATION.md`. This is the
   post-eval step the brief said NOT to do during the eval.
3. **If Will rejects:** see Option B in `HERMES_INTEGRATION.md` (custom ~150-line Node.js TaskRunner).

## STEPS FOR WILL (to finish C6)
1. Telegram → **@BotFather** → `/newbot` → name it → get the **token** (`8123...:AAH...`).
2. Telegram → **@userinfobot** → Start → copy your numeric **chat_id**.
3. Paste **token + chat_id** to the next Claude session. It does the rest (~5 min) and you confirm the
   test message arrives.

## How to VERIFY Hermes yourself (open a NEW PowerShell window first — PATH needs a fresh shell)
```powershell
hermes --version    # → Hermes Agent v0.17.0 ... Python 3.13.14   (fallback: C:\Users\willa\AppData\Local\hermes\bin\hermes.cmd)
hermes status       # → model = ollama/qwen3:14b
hermes -z "Reply with the word OLLAMA_OK and nothing else."   # free, local → OLLAMA_OK
claude -p "Reply HEADLESS_OK" --output-format json            # COSTS ~$0.04 (your Claude sub) → JSON HEADLESS_OK
```
Prior run captures are on disk at `C:\Users\willa\AppData\Local\hermes\cron\output\`.

## State left on disk
**Remains (for adoption):** the install at `C:\Users\willa\AppData\Local\hermes\` (`app`, venv,
`bin\hermes.cmd`, `config.yaml` w/ ollama+64K), helper scripts `scripts\c3_connected.sh` &
`scripts\c7_headless.sh`, `hermes_keepalive.cmd`, `hermes_task.xml`. Test file
`C:\SFV_BLUEPRINT\CURRENT_DIRECTIVE.md` (STATUS: RESEARCH — safe to delete).
**Torn down (eval-only):** the two hourly `claude -p` cron jobs, the gateway daemon, and the
Startup auto-start shortcut. Nothing is running or billing.

## Integrity note
The subagent that drafted `HERMES_EVAL.md` claimed it "overwrote a prior conflicting eval" — git
confirms that file **never existed** (no history, untracked). That claim was a confabulation; the
written file content is accurate to the verified findings. No data was lost.

## Connected files
- [[05_AI_LAYER/HERMES_INTEGRATION|Hermes Integration Spec]]
- [[00_DEV_LOG/HERMES_EVAL|Hermes Eval Results]]

## CONNECTED FILES
- [[HERMES_EVAL|Hermes Eval Results]]
- [[CURRENT_DIRECTIVE|Current Directive]]
- [[HARDWARE_CONTEXT|Hardware Context]]
- [[TOOL_STATUS|Tool Status]]
