---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-25
---

# SFV ENGINE — MULTI-AGENT WORKFLOW

> How Claude Chat, Claude Code, Claude Cowork, Antigravity, Ollama, and Obsidian
> operate together. The vault is the integration point — everything reads from and
> writes to C:\SFV_BLUEPRINT.

---

## THE CORE PRINCIPLE

The vault is the nervous system. No tool holds state.
Every tool writes its output back to the vault.
Every tool reads its instructions from the vault.
Will reviews in Obsidian. Will is the only one who makes canon decisions.

---

## TOOL ROLES (CONFIRMED)

| Tool | Role | Can write vault? | Needs approval? |
|------|------|-----------------|-----------------|
| Claude Chat | Planning, decisions, architecture | Via Desktop Commander | No — Will directs in real time |
| Claude Code | File edits, scripts, git ops | Directly | No — Will runs Code tab |
| Claude Cowork | Desktop automation, file routing | Indirectly (moves files) | No — Will runs Cowork |
| Antigravity | Local vault executor | Yes — with stated plan first | YES — must state then wait |
| Ollama (daemon) | Batch tasks, overnight processing | OLLAMA_RESULTS.md only | No — runs from TASK_QUEUE |
| Obsidian | GUI layer, human review interface | Via editor | Will edits directly |

---

## WORKFLOW: BLUEPRINT BUILD SESSION

```
SESSION START
├── Will opens Claude Chat
├── Claude Chat reads: SESSION_STATE.md + DASHBOARD.md + QUESTIONS_FOR_WILL.md
├── Claude Chat reports: 3 lines max
└── Will gives direction

PLANNING PHASE (Claude Chat)
├── Claude Chat plans the doc/workflow/decision
├── Claude Chat writes draft to vault via Desktop Commander
└── Claude Chat flags anything FOR HUMAN REVIEW

EXECUTION PHASE (Claude Code)
├── Will opens Code tab
├── Code reads CLAUDE.md (auto) + specific files as needed
├── Code writes directly to vault files
├── Code runs: git status, git diff, git commit
└── Code reports what changed

AUTOMATION PHASE (Antigravity)
├── Antigravity states: files to inspect + files to edit + commands to run
├── Will approves
├── Antigravity executes
├── Antigravity runs: git status --short + git diff --stat
└── Antigravity reports. Stops.

BATCH PHASE (Ollama daemon — runs parallel or overnight)
├── Will or Claude adds tasks to TASK_QUEUE.md
├── Daemon picks up every 30 seconds
├── Ollama processes using qwen3:14b
├── Results written to OLLAMA_RESULTS.md
└── Claude Chat reads OLLAMA_RESULTS.md next session start

REVIEW PHASE (Obsidian)
├── Will opens Obsidian
├── DASHBOARD.md shows: FOR HUMAN REVIEW items, UNCONFIRMED items, open questions
├── Will reviews, marks decisions, closes questions
└── Graph view shows vault connections

SESSION END
├── Claude Chat or Code updates SESSION_STATE.md
├── Claude Chat seeds TASK_QUEUE.md with overnight Ollama jobs
└── Will runs: git add . && git commit -m "session YYYY-MM-DD"
```

---

## WORKFLOW: FILE DELIVERY (example)

```
Shoot complete → SD cards in hand

1. INGEST (Will + Python script)
   → Files copied to staging folder
   → Checksums verified
   → Named per NAMING_CONVENTIONS.md

2. CULLING (Claude Code or Ollama)
   → Blur/duplicate detection task added to TASK_QUEUE.md
   → Ollama processes overnight if not urgent
   → Claude Code runs script if urgent

3. EDITING (Will)
   → Lightroom / Capture One
   → No AI layer here (Will's creative control)

4. EXPORT (Claude Code)
   → Runs export script per branch spec
   → Files land in DELIVERY staging folder

5. DELIVERY PREP (Claude Cowork)
   → Cowork organizes delivery folder structure
   → Renames for client-facing format
   → Uploads to Pixieset (if automated)

6. CAPTION GENERATION (Ollama)
   → Task added to TASK_QUEUE.md
   → Ollama drafts per OLLAMA_PROMPTS.md voice
   → Results in OLLAMA_RESULTS.md
   → Will approves before posting

7. POSTING (Antigravity — FUTURE)
   → Posts approved captions to platforms
   → Reports back to vault
```

---

## OLLAMA DAEMON — FIX AND VERIFY

### THE ERROR (resolved)
"bind: Only one usage of each socket address" = Ollama is ALREADY running.
This is normal if Ollama was auto-started by winget install or a previous session.

### CORRECT STEPS (Will runs these)
```
# DO NOT run: ollama serve   (already running)

# Step 1: Verify Ollama is live
# Open browser: http://localhost:11434
# Should show: "Ollama is running"

# Step 2: Verify model is pulled
# In Windows Terminal:
ollama list
# Must show qwen3:14b or qwen3

# Step 3: Run daemon only
python C:\SFV_BLUEPRINT\99_INBOX\ollama_daemon.py

# Step 4: Verify daemon is working
# Watch terminal output — should show:
# " Ollama OK"
# " Model: qwen3:14b"
# "[HH:MM:SS] 3 task(s) found"   ← because TASK_QUEUE has 3 tasks
# "Done → written to OLLAMA_RESULTS.md"
```

### HOW TO CONFIRM DAEMON WORKED
After running daemon: open Obsidian → navigate to 99_INBOX/OLLAMA_RESULTS.md
Should contain entries with timestamps and task results.
If OLLAMA_RESULTS.md is still empty after 2 minutes: daemon failed — report error from terminal.

---

## ANTIGRAVITY — CONFIRMED ROLE

Source: 05_AI_LAYER/ANTIGRAVITY_RULES.md

Antigravity is the LOCAL VAULT EXECUTOR. It runs directly on the Engine Body.
It can inspect, create, and edit vault files — but only with Will's explicit approval per action.

### Approval gate (every session, every action):
Antigravity must state BEFORE acting:
1. Files it will inspect
2. Files it will edit
3. Commands it will run
→ Will says yes → Antigravity executes → reports git diff → stops

### Task routing to Antigravity:
- Vault file creation (new folders, new branch files)
- Safe git inspection (status, diff, log)
- Running approved scripts
- Reporting diffs after changes

### Antigravity vs Claude Code:
| Situation | Use |
|-----------|-----|
| Will is in Claude Chat and needs vault edits | Claude Code (open Code tab) |
| Will wants automated local execution without switching tabs | Antigravity |
| Bulk file creation | Claude Code |
| Git audit without coding | Antigravity |

---

## GOOGLE TOOLS — WHAT'S WORTH ADDING

### CONFIRMED WORTH IT

**Google AI Studio** (aistudio.google.com) — FREE
- Access to Gemini 2.5 Pro (1M token context window)
- Use for: ingesting entire shoot logs, processing large reference docs
- Best for: tasks where context is massive and Claude context limit is a constraint
- Add to stack: YES

**NotebookLM** (notebooklm.google.com) — FREE
- Upload PDFs, docs, links → AI synthesizes and answers questions
- Use for: SFV research (competitor analysis, industry references, case studies)
- Add audio overviews of complex topics
- Add to stack: YES — use for 10_REFERENCES/ material

### SITUATIONALLY USEFUL

**Gemini Flash API** (via AI Studio)
- Cheaper than Sonnet for bulk text tasks
- Use only if Ollama can't handle a task and cost matters
- INFERENCE: probably not needed with Ollama running locally
- Add to stack: MAYBE — evaluate after Ollama is stable

**Google Colab** (colab.research.google.com) — FREE GPU
- Run Python notebooks with free GPU access
- Use for: testing larger local models, processing scripts, one-off heavy jobs
- Add to stack: MAYBE — useful if R&D Terminal hits limits

### NOT WORTH ADDING NOW

**Project IDX** — Cloud IDE. Redundant with Claude Code. NO.
**Jules** (Google coding agent) — Redundant with Claude Code. NO.
**Vertex AI** — Enterprise scale. Way overkill. NO.
**Firebase Genkit** — Agent framework. Not needed — vault + daemon does the job. NO.

### HOW GOOGLE TOOLS FIT IN WORKFLOW
```
Google AI Studio → use for: massive-context reads, reference synthesis
NotebookLM → use for: 10_REFERENCES/ research, competitor intel
Gemini Flash → use for: overflow from Ollama (if needed)
Everything else → current stack handles it
```

---

## BLUEPRINT BUILD PLAN (planning only — INGEST first)

### Priority order based on May 28 deadline:

1. **04_WORKFLOWS/INGEST.md** — needs full detail (May 28)
   What's missing: actual Python script spec, SD card detection logic,
   notification method, Google Drive intake process for other shooters

2. **08_TESTS/PAPER_TRIAL_RUNS.md** — Morning Walk walkthrough
   What's missing: full step-by-step simulation of May 28 shoot day

3. **04_WORKFLOWS/DELIVERY.md** — Pixieset setup detail
   What's missing: folder structure, naming for client delivery, turnaround time

4. **05_AI_LAYER/** — Antigravity integration, Google tools slots
   What's needed: update COST_ROUTING.md, update MODEL_ROUTING.md

5. **QUESTIONS_FOR_WILL.md** — scheduling tool still open
   Blocking: social posting workflow across 8+ accounts

---
*Written: 2026-05-25. All Antigravity rules sourced from 05_AI_LAYER/ANTIGRAVITY_RULES.md (CANON).*
*Google tool assessments: INFERENCE — FOR HUMAN REVIEW before purchasing any API access.*

## CONNECTED FILES
- [[SESSION_STATE|SESSION_STATE.md]]
- [[DASHBOARD|DASHBOARD.md]]
- [[QUESTIONS_FOR_WILL|QUESTIONS_FOR_WILL.md]]
- [[CLAUDE|CLAUDE.md]]
- [[ANTIGRAVITY_SETUP_GUIDE|ANTIGRAVITY_SETUP_GUIDE.md]]
- [[PROPOSALS|PROPOSALS.md]]
- [[INGEST|INGEST.md]]
