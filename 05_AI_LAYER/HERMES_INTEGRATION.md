---
STATUS: FOR HUMAN REVIEW
VERSION: v0.2.0
OWNER: WILL
LAST_UPDATED: 2026-06-27
CREATED_BY: Antigravity
RATIFIED: 2026-06-27 — Will confirmed Option A (Hermes eval before adopt). Architecture ratified.
DECISION_REQUIRED: Claude Code runs eval → Will reviews HERMES_EVAL.md → adopt or reject
---

# HERMES AGENT — INTEGRATION SPEC

> Hermes Agent (Nous Research, MIT license, Feb 2026).
> Repo: https://github.com/NousResearch/hermes-agent
> Self-evolution repo: https://github.com/NousResearch/hermes-agent-self-evolution
> Desktop app: v0.15.2, Windows supported (shipped June 2, 2026)

---

## DECISION STATUS

**RATIFIED 2026-06-27 by Will.** Option A locked. Option B is dead unless eval fails.

- **OPTION A — LOCKED:** Evaluate Hermes. If eval passes, adopt. If eval fails, fall back to Option B.
- **OPTION B — STANDBY ONLY:** Custom ~150-line Node.js TaskRunner. Only if Criterion 2 or 3 fails.

### RATIFIED ARCHITECTURE

**Roles (CANON):**
| Role | Tool | Notes |
|------|------|-------|
| DIRECTIVE WATCHER | Hermes (file watch, 0 tokens) | Watches CURRENT_DIRECTIVE.md for changes — fires first claude -p |
| PLANNER + EXECUTOR | Claude Code headless (`claude -p`) | Reads directive, builds, commits, writes STEP_RESULTS/ |
| STEP-TO-STEP TRIGGER | n8n + localFileTrigger | Sees STEP_RESULTS/ file → fires next claude -p |
| GATEKEEPER | Ollama qwen3:14b (cheap, always-on) | Before each step: in-scope or human-gate? Routes HANDOFFS/ if needed |
| INNER REVIEWER | Claude Code headless (read-only) | Every 3–5 steps. Writes REVIEW_NNN.md. No Antigravity rate limit consumed. |
| FINAL REVIEWER | Antigravity | Once per completed directive phase. Rare. |
| AUTHORITY | Will | Writes CURRENT_DIRECTIVE.md. Reviews HANDOFFS/. Approves phases. |

**The loop:**
```
Will writes CURRENT_DIRECTIVE.md
  → Hermes detects file change (0 tokens) → spawns first claude -p
  → Claude Code plans + executes one step → writes to STEP_RESULTS/
  → n8n localFileTrigger fires → Ollama gate: in-scope? 
      → YES: n8n fires next claude -p
      → NO (human-gate): write HANDOFFS/, Hermes pings Will via Telegram
  → every 3-5 steps: claude -p review pass → REVIEW_NNN.md
  → directive complete → Antigravity full review
      → PASS: Hermes pings Will "phase complete"
      → FAIL: new directive written, loop restarts
```

**Key principle:** Hermes never consumes tokens for orchestration. It is a file watcher and process spawner only. All intelligence sits in Claude Code and Ollama.

Next step: Claude Code runs eval directive below → writes HERMES_EVAL.md → Will reviews.

---

## WHAT HERMES IS (RELEVANT TO SFV)

| Capability | SFV relevance |
|------------|---------------|
| Persistent Windows daemon | Replaces missing loop driver — survives reboots |
| Spawns `claude -p` sessions | Drives autonomous build loop without Will initiating |
| Cross-session skill memory | Each completed task writes a skill — 40% efficiency gain at ~20 skills |
| Cron + file watcher scheduling | Watches CURRENT_DIRECTIVE.md for changes, fires loop |
| Telegram / Discord / Slack | Pings Will when HANDOFF or PHASE_COMPLETE — walk-away loop |
| Local Ollama support | Routes cheap tasks to qwen3:14b at 127.0.0.1:11434 |
| Anthropic API support | Sends claude -p calls with your existing API key |
| MCP support | Can later use n8n-MCP, Qdrant MCP when those are live |
| MIT license | Free. Pay only API costs. |

---

## EVAL DIRECTIVE FOR CLAUDE CODE

> Copy this entire section and give it to Claude Code as a directive.
> Claude Code installs Hermes on Engine Body, runs the eval, writes HERMES_EVAL.md.
> Do NOT integrate with vault or workflows during eval — test only.

---

### DIRECTIVE TEXT (paste to Claude Code)

```
Install Hermes Agent on Engine Body and run the eval checklist below.
Repo: https://github.com/NousResearch/hermes-agent

EVAL CHECKLIST — REQUIRED PASS/FAIL FOR EACH:

CRITERION 1 — INSTALL
Install Hermes Agent on Windows (Engine Body, RTX 5080).
Use the desktop app installer if available (v0.15.2). 
If desktop app fails: try npm/node install from repo.
Result: PASS if Hermes process is running. FAIL if installation errors out with no workaround.

CRITERION 2 — DAEMON PERSISTENCE
After install, restart the machine (or simulate: kill Hermes, re-launch via Task Scheduler or startup).
Result: PASS if Hermes restarts automatically on boot without manual intervention.
       FAIL if it requires manual restart after reboot.

CRITERION 3 — ANTHROPIC API CONNECTION
Configure Hermes with the Anthropic API key from n8n_env.ps1 (ANTHROPIC_API_KEY variable).
Drop a simple test task: "Reply with the word CONNECTED and nothing else."
Result: PASS if Hermes fires a claude -p call and returns "CONNECTED" to the output.
       FAIL if authentication errors, connection refused, or no output.

CRITERION 4 — LOCAL OLLAMA CONNECTION
Configure Hermes to use local Ollama at http://127.0.0.1:11434 with model qwen3:14b.
Drop a simple test task: "Reply with the word OLLAMA_OK and nothing else."
Result: PASS if Hermes fires the call and returns "OLLAMA_OK".
       FAIL if connection refused or model not found error.

CRITERION 5 — TELEGRAM NOTIFICATION
Configure Hermes with a Telegram bot token. (If no bot exists: create one via BotFather — 
takes 2 minutes. Document the bot token in HERMES_EVAL.md so Will can save it.)
Send a test notification: "HERMES_EVAL: criterion 5 test — if you see this, messaging works."
Result: PASS if Will receives the Telegram message.
       FAIL if no message received within 60 seconds.
       PARTIAL if bot creation works but message delivery fails.
(Note: Will must confirm receipt — write a placeholder row and flag for Will to confirm.)

CRITERION 6 — SKILL PERSISTENCE
After completing criteria 1-4, check if Hermes created a skills directory.
Look for: any directory named skills/, .hermes/, or similar in the Hermes install path.
Result: PASS if a persistent skills/memory directory exists and survived the criterion 2 restart.
       FAIL if no persistent storage found.
       PARTIAL if directory exists but was empty after restart.

CRITERION 7 — CLAUDE CODE HEADLESS SPAWN
Confirm that Hermes can spawn `claude -p` headlessly (not via Hermes' own internal call — 
via a task that explicitly runs the claude CLI with a simple prompt and captures output).
Test: create a Hermes task that runs: claude -p "Reply HEADLESS_OK" --output-format json
Result: PASS if Hermes spawns the claude CLI and captures the JSON output.
       FAIL if claude CLI not found or output not captured.
       PARTIAL if it runs but output format is broken.

EVAL OUTPUT:
Write all results to: C:\SFV_BLUEPRINT\00_DEV_LOG\HERMES_EVAL.md
Format each criterion as: PASS / FAIL / PARTIAL with one paragraph of detail.
Include: install path, any Windows-specific issues found, workarounds applied.
Include: estimated setup time for each criterion.
Do NOT integrate Hermes with the vault or n8n workflows. Eval only.
Stop after writing HERMES_EVAL.md.

ADOPTION DECISION RULE (Claude Code does not decide this — Will decides):
- 7/7 PASS: Adopt immediately
- 5-6/7 PASS (with PARTIAL on 5): Adopt with notes on what to fix
- Criterion 2 FAIL: Do not adopt — daemon persistence is non-negotiable
- Criterion 3 FAIL: Do not adopt — Anthropic API is the primary backend
- Criterion 5 PARTIAL + everything else PASS: Adopt, fix Telegram separately
- 3 or more FAIL: Reject, build Option B
```

---

## SKILL SEEDING PLAN

> Pre-loaded skills to give Hermes at adoption time.
> Goal: skip the cold-start period and get compounding efficiency from day one.
> These are written as Hermes skill files. Claude Code imports them during integration session.
> All skills derived from existing vault docs — no new content invented.

### Skill 1 — SFV System Context
**Trigger phrases:** "sfv", "engine", "what is this system", "context"
**Content summary:** What SFV Engine is, two nodes (Engine Body + R&D Terminal), money makers (UGC + EVENTS), branch structure, vault location.
**Source:** MASTER_CONTEXT.md + COMPRESSED_CONTEXT.md

### Skill 2 — Drop a Task to Queue
**Trigger phrases:** "drop task", "add to queue", "run this through n8n", "queue a job"
**Content summary:** How to create a valid job envelope JSON (JOB_ENVELOPE_SPEC.md schema), required fields, status must be PENDING, file goes to `C:\SFV_BLUEPRINT\99_INBOX\QUEUE\`.
**Source:** JOB_ENVELOPE_SPEC.md

### Skill 3 — Update SESSION_STATE
**Trigger phrases:** "update session state", "log what we did", "record progress"
**Content summary:** SESSION_STATE.md location, format, what to include (last completed, current state, open flags, next steps). Rule: always update at session end before stopping.
**Source:** SESSION_STATE.md header + session protocol in ANTIGRAVITY.md

### Skill 4 — Write a HANDOFF
**Trigger phrases:** "write handoff", "human gate", "pause for Will", "need Will's decision"
**Content summary:** HANDOFF file format, location (`C:\SFV_BLUEPRINT\00_DEV_LOG\HANDOFF_YYYY-MM-DD.md`), required sections (WHAT WAS COMPLETED, DECISION REQUIRED, NEXT SESSION PRIORITY ORDER, STEPS FOR WILL).
**Source:** HANDOFF_2026-06-27.md (as template reference)

### Skill 5 — Canon Rules
**Trigger phrases:** "can I", "am I allowed to", "should I", "is this allowed"
**Content summary:** 12 canon rules verbatim. Emphasis on: no invention (Rule 01), label everything (Rule 02), human taste is final (Rule 03), blueprint before build (Rule 07), CANON promotion requires Will.
**Source:** 01_CANON_RULES/RULES.md

### Skill 6 — n8n Health Check
**Trigger phrases:** "check n8n", "is n8n running", "n8n health", "workflow status"
**Content summary:** n8n health endpoint (`http://127.0.0.1:5678/healthz`), workflow IDs (WF1/WF2/WF4), how to check active/published status, what to do if health check fails (check logs, restart via start_n8n.ps1).
**Source:** HANDOFF_2026-06-27.md + SESSION_STATE.md

### Skill 7 — Cost Check Before API Call
**Trigger phrases:** "about to call claude", "spawn claude -p", "api call", "before I run"
**Content summary:** Before any Claude API call: read COST_ALERTS.md. If unresolved alert and remaining budget < $0.50: write HANDOFF, ping Will, do not fire. Ceiling is $25 (Anthropic enforced). Alert at $20.
**Source:** COST_CEILING_POLICY.md

### Skill 8 — Git Checkpoint
**Trigger phrases:** "create checkpoint", "git branch", "before I start", "autonomous session"
**Content summary:** Before any autonomous build session: `git checkout -b autonomous/DIR-YYYYMMDD-NNN`. After session: `git add -A && git commit -m "[DIR-ID] autonomous session complete"`. Will pushes to remote manually. Never force-push.
**Source:** RULES.md Rule 10 + SESSION_STATE.md git notes

### Skill 9 — Branch Classification
**Trigger phrases:** "which branch", "classify this file", "what branch does this belong to"
**Content summary:** SFV branch definitions — MYTHOLOGY (hub, Level 1), LIVE (event coverage, 3.5), EVENTS (on-site portraits, money maker, 5-6.5), ATHLETICS (sports, 3.5), STUDIO (studio production, 5.5), UGC (primary money engine, 6.5), ARCHIVE (portfolio, 3.5), WORLD (life/alias, 2.5), 404 (experimental, 2.5).
**Source:** BRANCH_OUTPUTS.md

### Skill 10 — CURRENT_DIRECTIVE Interpretation
**Trigger phrases:** "read the directive", "what's the current task", "directive", "what am I doing"
**Content summary:** CURRENT_DIRECTIVE.md location, all field meanings, how to read SCOPE_BOUNDS/SUCCESS_CRITERIA/HUMAN_GATE_TRIGGERS, how to write STEP_RESULTS, how to write COMPLETION_FILE.
**Source:** DIRECTIVE_TEMPLATE.md (this session's new doc)

---

## HERMES CONFIGURATION SPEC (ENGINE BODY)

> Applied during integration session after eval passes.

```yaml
# hermes-config.yaml (Engine Body)
provider:
  primary: anthropic
  api_key: ${ANTHROPIC_API_KEY}  # reads from n8n_env.ps1 / Windows env
  model: claude-sonnet-4-5  # or claude-opus-4 for directive planning

local_provider:
  type: ollama
  base_url: http://127.0.0.1:11434
  model: qwen3:14b
  use_for: [classify, summarize, gate, health_check]

messaging:
  telegram:
    bot_token: ${TELEGRAM_BOT_TOKEN}
    chat_id: ${TELEGRAM_CHAT_ID}
  notify_on: [handoff, phase_complete, error, daily_digest]

file_watch:
  - path: C:\SFV_BLUEPRINT\CURRENT_DIRECTIVE.md
    on_change: fire_directive_loop
  - path: C:\SFV_BLUEPRINT\99_INBOX\QUEUE
    on_new_file: notify_only  # n8n handles queue — Hermes just watches

skills_dir: C:\SFV_BLUEPRINT\.hermes\skills\

loop_config:
  review_every_n_steps: 4
  git_branch_before_session: true
  cost_check_before_spawn: true
  max_concurrent_sessions: 1

daemon:
  startup: task_scheduler  # Windows Task Scheduler, ONSTART trigger
  restart_on_crash: true
  log_path: C:\SFV_BLUEPRINT\00_DEV_LOG\HERMES_DAEMON_LOG.md
```

---

## R&D TERMINAL — SEPARATE HERMES INSTANCE

> Second Hermes instance on R&D Terminal (RTX 3060).
> Runs independently from Engine Body Hermes.
> Handles: telemetry loop, weekly digest, trading sandbox notifications.

```yaml
# hermes-config.yaml (R&D Terminal)
provider:
  primary: ollama  # R&D Terminal uses local only — no Anthropic API calls
  base_url: http://127.0.0.1:11434
  model: qwen3:8b  # lighter model — R&D Terminal VRAM constraint

messaging:
  telegram:
    bot_token: ${TELEGRAM_BOT_TOKEN}  # same bot, same chat
    chat_id: ${TELEGRAM_CHAT_ID}
  notify_on: [weekly_digest, anomaly, trading_alert]

file_watch:
  - path: D:\SFV_ACTIVE\LOGS\TELEMETRY\
    on_new_file: run_telemetry_analysis

loop_config:
  telemetry_digest_cron: "0 9 * * 1"  # Monday 9am weekly digest
  max_concurrent_sessions: 1

daemon:
  startup: task_scheduler
  restart_on_crash: true
```

---

## ROLLBACK PROCEDURE (AUTONOMOUS SESSIONS)

> These rules apply to every autonomous session Hermes runs.
> They protect the vault from a bad overnight directive.

### Before every session:
1. Hermes runs: `git checkout -b autonomous/DIR-YYYYMMDD-NNN`
2. Hermes exports n8n workflows to `03_INFRASTRUCTURE/n8n_workflows/` (snapshot)
3. Hermes writes a session start entry to `HERMES_DAEMON_LOG.md`

### During session:
- Claude Code may write DRAFT-status docs only
- No CANON promotions
- Every 4 steps: review pass (read-only claude -p)
- If HUMAN_GATE_TRIGGER fires: stop, write HANDOFF, ping Will

### After session (COMPLETE):
- Hermes writes `STEP_RESULTS/DIR-YYYYMMDD-NNN_COMPLETE.md`
- Hermes pings Will via Telegram: "Directive DIR-YYYYMMDD-NNN complete. Review STEP_RESULTS/."
- Git commit on the branch
- Will reviews, promotes DRAFT to CANON manually, merges branch

### If session goes wrong (ROLLBACK):
```powershell
# Run on Engine Body — returns vault to pre-session state
git checkout main
git branch -D autonomous/DIR-YYYYMMDD-NNN  # deletes bad branch
# n8n workflows: re-import from last known good JSON in 03_INFRASTRUCTURE/
```

---

## IMPLEMENTATION ORDER (post-eval)

| Step | Action | Who | Prerequisite |
|------|--------|-----|-------------|
| 1 | Run eval directive | Claude Code | Will approves eval |
| 2 | Will reviews HERMES_EVAL.md | Will | Eval complete |
| 3 | Adopt/reject decision | Will | Eval reviewed |
| 4 | Integration session: install + configure | Claude Code | Adopt decision |
| 5 | Seed skills (Skills 1-10) | Claude Code | Integration complete |
| 6 | Configure Telegram bot | Will + Claude Code | Integration complete |
| 7 | Test: first real directive (small scope) | Will + Hermes | Skills seeded |
| 8 | R&D Terminal Hermes instance | Claude Code | Engine Body Hermes stable |

---

## CONNECTED FILES
- [[HERMES_EVAL|HERMES_EVAL.md]]
- [[CURRENT_DIRECTIVE|CURRENT_DIRECTIVE.md]]
- [[OLLAMA_SETUP|OLLAMA_SETUP.md]]
- [[CLAUDE_CODE_PROMPTS|CLAUDE_CODE_PROMPTS.md]]
- [[PROMPT_VERSIONING|PROMPT_VERSIONING.md]]
- [[ANTIGRAVITY|ANTIGRAVITY.md]]
