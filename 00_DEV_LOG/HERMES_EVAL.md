# HERMES AGENT — EVALUATION

> STATUS: CANON
> VERSION: v1.1
> OWNER: WILL
> LAST_UPDATED: 2026-06-28
> CREATED_BY: Claude Code (eval) · resolution by Claude Opus 4.8 (Claude Chat)
> RATIFICATION: Adoption ratified by Will — confirmed verbally in-session 2026-06-28 (resolves the prior header/footer FHR-vs-CANON contradiction).

**Environment:** Engine Body, Windows 11, RTX 5080.
**Install path root:** `C:\Users\willa\AppData\Local\hermes\` (subdirs: `app\` = source tree + `.venv`; `bin\` = `uv.exe` + `hermes.cmd` global shim; `scripts\`; `cron\`; `config.yaml`).
**Global launcher:** `C:\Users\willa\AppData\Local\hermes\bin\hermes.cmd` added to User PATH; `HERMES_HOME` env var set.
**Versions:** Hermes Agent v0.17.0 (2026.6.19); Python 3.13.14 (provisioned by uv); uv 0.11.25.

---

## Summary Tally

| Criterion | Verdict |
|---|---|
| C1 — Install | PASS |
| C2 — Daemon persistence | PASS (with caveats) |
| C3 — Anthropic API connection | PASS (brief premise corrected) |
| C4 — Local Ollama | PASS |
| C5 — File watch (critical / deal-breaker) | PARTIAL |
| C6 — Telegram notification | PENDING (PENDING_WILL_CONFIRM) |
| C7 — Claude Code headless spawn | PASS |

---

## C1 — Install

**PASS**

The official Windows installer `iex (irm https://hermes-agent.nousresearch.com/install.ps1)` FAILED partway: it downloaded `uv.exe` into `bin\` but then errored with "EPERM uv_spawn powershell.exe" — the uv tool could not spawn a nested powershell child in this environment. The "desktop app v0.15.2" named in the SFV brief does NOT exist as a release: the repo's latest release is v0.17.0 and there is no standalone desktop installer for 0.15.2. Workaround = manual install from source: git clone the repo (required `core.longpaths=true` because Windows MAX_PATH broke checkout of deeply-nested website/i18n docs paths), `uv venv --python 3.13` (required `UV_NATIVE_TLS=1` / `UV_SYSTEM_CERTS=1` because uv's bundled cert store rejected the GitHub python-build-standalone download as "invalid peer certificate: UnknownIssuer" — a proxy/MITM cert), then `uv pip install -e .`. Hermes requires Python >=3.11,<3.14; the system Python was 3.14.5 (too new), so uv provisioned CPython 3.13.14. Source relocated to durable `C:\Users\willa\AppData\Local\hermes\app`, plus a global `hermes.cmd` shim + User PATH + `HERMES_HOME`. `hermes --version` and `hermes status` confirm it runs.

- **Install/affected path:** `C:\Users\willa\AppData\Local\hermes\` (`app\` source tree + `.venv`; `bin\hermes.cmd` shim); User PATH + `HERMES_HOME` set.
- **Windows-specific issues:** official installer fails at uv nested powershell spawn (EPERM uv_spawn); Windows MAX_PATH breaks git checkout of deep i18n paths (needs `core.longpaths=true`); uv bundled TLS rejects GitHub download ("UnknownIssuer", needs `UV_NATIVE_TLS`/`UV_SYSTEM_CERTS`); system Python 3.14.5 too new (Hermes needs 3.11–3.13).
- **Workarounds applied:** manual source install; `core.longpaths=true`; `UV_NATIVE_TLS=1` / `UV_SYSTEM_CERTS=1`; uv provisioned CPython 3.13.14; relocated source to durable AppData path with global shim.
- **Setup time:** ~25–30 min (mostly downloads + troubleshooting the three Windows issues).

---

## C2 — Daemon persistence

**PASS** (with caveats)

The Hermes daemon is the "gateway" (`hermes gateway run`); it stays alive even with no messaging platform configured (it runs the cron ticker). Hermes' `gateway install` supports ONLY systemd (Linux) / launchd (macOS) — there is NO native Windows service/Task Scheduler support in the code. Both `schtasks /Create /XML` and PowerShell `Register-ScheduledTask` returned "Access is denied" in this non-elevated session. Persistence was instead achieved with no admin: a Startup-folder shortcut (`C:\Users\willa\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\HermesGatewayEngineBody.lnk`) pointing to a keep-alive wrapper (`C:\Users\willa\AppData\Local\hermes\hermes_keepalive.cmd`) that loops `hermes gateway run` and relaunches within ~5s if it exits. Auto-restart was DEMONSTRATED: gateway came up as PID 20796, was force-killed, and the wrapper auto-restarted a new gateway (PID 45140) in ~3 seconds with no manual intervention. For reboot-survival without login + restart-on-failure, Will should register the provided XML (`C:\Users\willa\AppData\Local\hermes\hermes_task.xml`) from an ELEVATED prompt one time.

- **Install/affected path:** Startup-folder shortcut `...\Startup\HermesGatewayEngineBody.lnk`; keep-alive wrapper `C:\Users\willa\AppData\Local\hermes\hermes_keepalive.cmd`; Task Scheduler XML `C:\Users\willa\AppData\Local\hermes\hermes_task.xml`.
- **Windows-specific issues:** no native Windows daemon (systemd/launchd only); Task Scheduler registration needs elevation (`schtasks /Create /XML` and `Register-ScheduledTask` both returned "Access is denied" non-elevated).
- **Workarounds applied:** no-admin Startup-folder shortcut + keep-alive wrapper loop (relaunch within ~5s); auto-restart demonstrated (PID 20796 killed → PID 45140 up in ~3s). Reboot-survival without login requires Will to register `hermes_task.xml` once from an elevated prompt.
- **Setup time:** ~10 min.

---

## C3 — Anthropic API connection

**PASS** (brief premise corrected)

The SFV brief said to read `ANTHROPIC_API_KEY` from `n8n_env.ps1`, but that file contains NO Anthropic key (only Tavily, Ollama, Postgres vars), and `ANTHROPIC_API_KEY` is not set anywhere on the system (Process/User/Machine env all unset). However, the installed `claude` CLI (Claude Code, at `C:\Users\willa\.local\bin\claude`) is authenticated via the Claude subscription and works headless with no API key. A Hermes cron job in `--no-agent` mode (which skips the LLM entirely = ZERO Hermes orchestration tokens) ran a script calling `claude -p "Reply with the word CONNECTED and nothing else."`; Hermes spawned it and captured an output file (`C:\Users\willa\AppData\Local\hermes\cron\output\fb059dcf1c4f\...md`) containing exactly "CONNECTED". So the real Anthropic path is Hermes spawning the already-authenticated claude CLI, matching the SFV architecture ("Hermes never consumes tokens for orchestration"). Caveat: the claude call itself bills the Claude subscription (~$0.04 observed per call), not a standalone Anthropic API key.

- **Install/affected path:** `claude` CLI at `C:\Users\willa\.local\bin\claude`; helper `scripts\c3_connected.sh`; output `C:\Users\willa\AppData\Local\hermes\cron\output\fb059dcf1c4f\...md`.
- **Windows-specific issues:** none specific to this criterion (brief premise corrected: no `ANTHROPIC_API_KEY` in `n8n_env.ps1` or anywhere on system).
- **Workarounds applied:** used the subscription-authenticated `claude` CLI spawned by a Hermes `--no-agent` cron job (zero Hermes orchestration tokens) instead of a standalone API key.
- **Setup time:** ~5 min.

---

## C4 — Local Ollama

**PASS**

Ollama was running at `http://127.0.0.1:11434` with `qwen3:14b` present. `hermes config set model ollama/qwen3:14b` auto-expanded to provider:custom + base_url `http://127.0.0.1:11434/v1` + default `qwen3:14b`. Two gates hit: first "No inference provider configured", then Hermes' hard 64K-context MINIMUM — `qwen3:14b` advertises only 40,960 tokens. Workaround: set `model.context_length=65536` AND `model.ollama_num_ctx=65536` (forces Ollama to load the model at 64K). After that, `hermes -z "Reply with the word OLLAMA_OK and nothing else."` returned exactly "OLLAMA_OK". Note: 64K context on a 14B Q4 model raises VRAM use (fine on RTX 5080).

- **Install/affected path:** `config.yaml` model settings (provider:custom, base_url `http://127.0.0.1:11434/v1`, `qwen3:14b`, `context_length=65536`, `ollama_num_ctx=65536`).
- **Windows-specific issues:** Hermes' 64K-context minimum vs `qwen3:14b`'s 40,960 default; 64K context on 14B Q4 raises VRAM use (fine on RTX 5080).
- **Workarounds applied:** `model.context_length=65536` + `model.ollama_num_ctx=65536` to force Ollama to load the model at 64K.
- **Setup time:** ~10 min.

---

## C5 — File watch (critical / deal-breaker)

**PARTIAL**

Requirement: watch `C:\SFV_BLUEPRINT\CURRENT_DIRECTIVE.md` and fire a handler within 10s with 0 tokens. KEY FINDING: Hermes has NO native filesystem-event watcher. Its cron scheduler ticks every 60 seconds (`TICKER_INTERVAL_SECONDS=60`) with minute-granularity schedules — i.e. a 60s poll, which fails the <10s bar; and the `file_watch:` config the SFV architecture doc assumes does NOT exist in Hermes. `webhook` is HTTP-POST driven, `hooks` fire on Hermes events (not file changes). HOWEVER Hermes bundles the `watchfiles` library (OS-native FS events). A ~20-line custom watchfiles watcher was built and measured: a one-line change to `CURRENT_DIRECTIVE.md` was detected in ~0.098 seconds (98 ms), with the handler being a pure local echo and ZERO API tokens. So the literal outcome (handler fired, <10s, 0 tokens, no API poll, change not missed) PASSES — BUT this is NOT a native Hermes feature; it required a custom watchfiles wrapper run as its own process (e.g. under the same Startup/keep-alive daemon). Verdict PARTIAL: the zero-token sub-100ms watcher is achievable on the Hermes stack and was demonstrated, but Hermes itself provides no native <10s file-watch — Will must decide whether a small bundled-watchfiles wrapper is acceptable for this deal-breaker. A test file `CURRENT_DIRECTIVE.md` was created at the vault root, marked "STATUS: RESEARCH — safe to delete".

- **Install/affected path:** test file `C:\SFV_BLUEPRINT\CURRENT_DIRECTIVE.md` (STATUS: RESEARCH — safe to delete); custom ~20-line `watchfiles` wrapper on the Hermes stack.
- **Windows-specific issues:** no native file-watch in Hermes — needs a `watchfiles` wrapper.
- **Workarounds applied:** custom `watchfiles` watcher (~20 lines) run as its own process; measured detection ~0.098s (98 ms), pure local echo handler, zero API tokens.
- **Setup time:** ~10 min.

---

## C6 — Telegram notification

**PENDING** (PENDING_WILL_CONFIRM)

Claude Code cannot create a Telegram bot via BotFather (no Telegram access) and will not fabricate a token. Will agreed to create the bot and provide the token + chat_id. Hermes supports Telegram natively (gateway setup; cron `--deliver telegram`; `hermes send`). Once Will supplies `TELEGRAM_BOT_TOKEN` + chat_id, completing this is ~5 min: set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_ALLOWED_USERS` in `C:\Users\willa\AppData\Local\hermes\.env`, run `hermes gateway setup`, then send "HERMES_EVAL: criterion 6 test." Status: blocked on Will's token; Will then confirms receipt.

- **Install/affected path:** `C:\Users\willa\AppData\Local\hermes\.env` (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USERS`).
- **Windows-specific issues:** none specific to this criterion.
- **Workarounds applied:** none yet — blocked on Will supplying `TELEGRAM_BOT_TOKEN` + chat_id (PENDING_WILL_CONFIRM).
- **Setup time:** ~5 min once Will supplies the token.

---

## C7 — Claude Code headless spawn

**PASS**

A Hermes cron job in `--no-agent` mode (zero Hermes tokens) ran `claude -p "Reply HEADLESS_OK" --output-format json`; Hermes spawned the claude CLI and captured clean JSON to an output file (`C:\Users\willa\AppData\Local\hermes\cron\output\11d82d4c37c6\...md`) containing `"result":"HEADLESS_OK","is_error":false` plus the full usage block. claude call cost ~$0.038.

- **Install/affected path:** helper `scripts\c7_headless.sh`; output `C:\Users\willa\AppData\Local\hermes\cron\output\11d82d4c37c6\...md`.
- **Windows-specific issues:** none specific to this criterion.
- **Workarounds applied:** same mechanism as C3 — Hermes `--no-agent` cron job spawns the subscription-authenticated `claude` CLI (zero Hermes tokens).
- **Setup time:** ~3 min (same mechanism as C3).

---

## Windows-Specific Issues (consolidated)

1. Official installer fails at uv nested powershell spawn (EPERM uv_spawn) — manual source install needed.
2. Windows MAX_PATH breaks git checkout of deep i18n paths — needs `core.longpaths=true`.
3. uv's bundled TLS rejects GitHub downloads ("UnknownIssuer") — needs `UV_NATIVE_TLS`/`UV_SYSTEM_CERTS` to use the Windows cert store.
4. System Python 3.14.5 too new (Hermes needs 3.11–3.13) — uv provisioned 3.13.14.
5. No native Windows daemon (systemd/launchd only).
6. Task Scheduler registration needs elevation (used Startup folder as no-admin workaround).
7. Hermes' 64K-context minimum vs `qwen3:14b`'s 40,960 default — needs `context_length` + `ollama_num_ctx` override.
8. No native file-watch — needs a `watchfiles` wrapper.

---

## What remains on disk

The persistent/cost-incurring pieces were torn down (see note). What remains:

- The Hermes install at `C:\Users\willa\AppData\Local\hermes\` (`app`, venv, `bin` shim, `config.yaml` with ollama + 64K settings).
- The helper scripts (`scripts\c3_connected.sh`, `scripts\c7_headless.sh`).
- The keep-alive wrapper (`hermes_keepalive.cmd`) and Task Scheduler XML (`hermes_task.xml`) for Will to activate on adoption.
- The test file `C:\SFV_BLUEPRINT\CURRENT_DIRECTIVE.md` (STATUS: RESEARCH, deletable).

**Note:** The two hourly claude-spawn cron jobs (c3-connected, c7-headless), the running gateway daemon, and the Startup-folder auto-start shortcut were REMOVED/STOPPED after testing so the eval leaves nothing firing paid claude calls or auto-starting before Will ratifies adoption.

---

## Adoption inputs (Will decides — not Claude Code)

Tally = 5 PASS (C1, C2, C3, C4, C7), 1 PARTIAL (C5), 1 PENDING (C6).

Against the SFV adoption rule:

- C2 did NOT fail (PASS) and C3 did NOT fail (PASS), so neither deal-breaker tripped.
- C5 (the zero-token watcher deal-breaker) is PARTIAL not FAIL — the zero-token <100ms watcher works but is not native to Hermes.
- There were not 3+ FAILs.

Net: ≥5 PASS, which under the rule puts it in "Will ratifies adoption" territory, contingent on (a) Will's judgment on the C5 native-vs-wrapper gap and (b) completing C6.

These are inputs only — Claude Code does NOT render an adopt/reject decision. Will decides.

---

## Setup Run 2026-06-28
- Toolsets enabled: coding, file, terminal, search, memory, skills, vision
  - NOTE: `file` and `terminal` were already enabled (not present in `disabled_toolsets`). Actual removals from the disabled list: coding, search, memory, skills, vision.
- Local Ollama configured: http://localhost:11434/v1 (OLLAMA_API_KEY=ollama), added to `.env` after the header comment block.
- Vault MCP added: sfv-vault → C:\SFV_BLUEPRINT (`@modelcontextprotocol/server-filesystem` via npx).
- Smart model routing: enabled.
- Memory: memory_enabled=true, user_profile_enabled=true.
- Constraints honored: model.default unchanged (claude-sonnet-4-6); no ANTHROPIC_API_KEY or existing keys touched (none were present/active in `.env`); no n8n/Postgres configs modified.
- Backups written: config.yaml.bak.20260628, .env.bak.20260628 (in hermes install dir).
- config.yaml re-validated as parseable YAML after edits.
- Status: RATIFIED BY WILL 2026-06-28 — CANON.

---

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>


---

## TLS / Norton + Two-Venv Resolution — 2026-06-28 (CANON)

> Resolves the "Telegram connects but model reply fails" blocker from HANDOFF_2026-06-28.
> Brain decision: **Ollama `qwen3:14b`** (local, free, private) for chat; `claude` CLI stays for coding (zero-token). Ratified by Will in-session.

### Root cause (the real one — not TLS, not config format)
The Norton fix (`truststore.inject_into_ssl()` via `sitecustomize.py`) replaces Python's default `SSLContext`. Hermes' SSL pre-flight guard (`agent/ssl_guard.py` → `verify_ca_bundle()` → `_validate_bundle_path()`) calls `ctx.get_ca_certs()`, which **truststore raises as a bare `NotImplementedError()` whose `str()` is empty**. That empty exception was swallowed by `agent/agent_init.py:962` into the meaningless `"Failed to initialize OpenAI client: "`. It passed in the original eval only because truststore was added *afterward* (late-night 06-28), so the eval never hit it.

### Fixes applied (all CANON)
1. **`HERMES_SKIP_SSL_GUARD=1`** — Hermes' own intended escape hatch; skips the broken pre-flight. SAFE: real cert validation still happens in httpx via truststore (verified: Anthropic 401, Telegram 302). Persisted in: keepalive wrapper (`set HERMES_SKIP_SSL_GUARD=1`) + **User-scope env var** + (NOT in `.env` — file was exclusively locked by the desktop app; User env var covers it).
2. **Two-venv split fixed.** There are two non-shared venvs: `app\.venv` (truststore, NO Telegram) and `hermes-agent\venv` (Telegram via `python-telegram-bot`, was MISSING truststore). `api.telegram.org` IS Norton-intercepted, so the Telegram venv needs truststore too. Fixed by **copying the pure-Python `truststore` package** `app\.venv → hermes-agent\venv` site-packages (avoids a pip download Norton would break). The gateway must run from **`hermes-agent\venv`** (only venv with Telegram).
3. **Keepalive wrapper repointed** to `hermes-agent\venv\Scripts\hermes.exe` (was `app\.venv`).
4. **Model config** (`config.yaml` `model:` block) set to nested-dict Ollama form: `provider: custom`, `base_url: http://127.0.0.1:11434/v1`, `api_key: ollama`, `default: qwen3:14b`, `context_length: 65536`, `ollama_num_ctx: 65536`. (Hermes reads `model.api_key`; the OpenAI SDK requires a non-empty key even for Ollama. Backup: `config.yaml.bak.20260628_184304`.)

### Verified live 2026-06-28
- `hermes -z "PING"` → `PING` via Ollama qwen3:14b. ✅
- Gateway from `hermes-agent\venv` → `[Telegram] Connected to Telegram (polling mode)` → `Gateway running with 1 platform(s)`, no SSL errors, 52 bot-commands registered. ✅
- `hermes send --to telegram` → delivered to home channel 7888020584. ✅

### KEY LEARNINGS (CANON)
- **truststore + Hermes SSL guard are incompatible** — truststore's `SSLContext.get_ca_certs()` is `NotImplementedError` (empty). Always set `HERMES_SKIP_SSL_GUARD=1` on any Hermes install behind an AV TLS-interceptor.
- **`api.telegram.org` IS Norton-intercepted** — the Telegram venv needs truststore, not just the model venv.
- **Two venvs, no shared packages** — fixes (truststore, etc.) must be applied to BOTH `app\.venv` and `hermes-agent\venv`. The gateway runs from `hermes-agent\venv`.
- **Local Ollama needs no truststore** (plain http, not intercepted) — but still needs a non-empty `model.api_key`.

### OPEN [FOR HUMAN REVIEW] — not done this session
- **Reboot persistence**: gateway is running via keepalive launched this session, but there is NO auto-start on boot/login. Register `hermes_task.xml` from an ELEVATED prompt (Will-only) OR re-create the no-admin Startup-folder shortcut → `hermes_keepalive.cmd`.
- **Telegram bot token rotation** (still cleartext-exposed per HANDOFF_2026-06-28; `/revoke` via BotFather) + **Tavily key rotation** (standing CRITICAL_PATH).
- **Inbound→reply loop** not yet user-tested — Will to message the bot and confirm a qwen3:14b reply.
- `.env` append for `HERMES_SKIP_SSL_GUARD` skipped (file locked by desktop app); covered by User env var instead. Add to `.env` if desired when desktop app is closed.
