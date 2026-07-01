---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-25
---

# SFV ENGINE — FULL STACK INTEGRATION PLAN
## Claude + Obsidian + Ollama + Antigravity

> Built session 2026-05-25. Will is final authority on all decisions.
> Antigravity specifics marked UNCONFIRMED — confirm before routing tasks to it.

---

## THE STACK (confirmed)

| Tool | Node | Status | Role |
|------|------|--------|------|
| Claude Chat (claude.ai) | Engine Body | LIVE | Planning, session starts, blueprint decisions |
| Claude Code (Code tab) | Engine Body | LIVE | Vault edits, scripts, file ops, git |
| Claude Cowork (desktop) | Engine Body | LIVE | Desktop automation, file routing |
| Antigravity | Engine Body | LIVE | Local Integration Agent (complex automated tasks, scripting, background runs, web API research) |
| Obsidian | Engine Body | LIVE | Vault GUI, Dataview, graph view |
| Windows Terminal | Engine Body | LIVE | Daemon control, git ops |
| Ollama qwen3:14b | R&D Terminal | LIVE* | Free local inference, batch tasks |

*Confirm: `ollama list` to verify qwen3:14b pull completed.

---

## VERSION 1 — STEP BY STEP SETUP
### Claude + Obsidian + Ollama + Antigravity (no Cowork/Code layer)

### STEP 1 — Verify Ollama is live (Will does this)
```
# In Windows Terminal on R&D Terminal:
ollama list
# Must show qwen3:14b. If not: ollama pull qwen3:14b
# Then start daemon:
ollama serve
# Tab 2:
python C:\SFV_BLUEPRINT\99_INBOX\ollama_daemon.py
```
**Can I do this for you?** NO — requires R&D Terminal access. Will runs this.

### STEP 2 — Verify Obsidian plugins are installed (Will does this)
Required plugins (all in Settings > Community Plugins):
- [x] Dataview
- [x] Templater
- [x] Obsidian Git
- [x] Metadata Menu
- [x] QuickAdd
- [x] Excalidraw
- [x] Local GPT — INSTALL IF NOT DONE
- [x] Smart Connections — INSTALL IF NOT DONE

**Local GPT config** (after install):
Settings > Local GPT:
- Provider: Ollama
- Model: qwen3:14b
- URL: http://localhost:11434

**Can I do this for you?** NO — Obsidian plugin install requires Will to click. I can write config files if needed.

### STEP 3 — Confirm Antigravity (Confirmed)
Antigravity is the local agentic executor and integration developer. It handles end-to-end task execution: writing scripts, running terminal commands, managing background/scheduled operations, conducting web/API research, and coordinating multi-agent checks.

### STEP 4 — Claude Chat session protocol (already live)
This is already working. Protocol:
1. New session → I read SESSION_STATE.md, DASHBOARD.md, QUESTIONS_FOR_WILL.md
2. Report 3 lines max
3. Wait for Will's direction
4. Use COMPRESSED_CONTEXT.md as context fuel — NOT full vault reads

**No changes needed. Already operational.**

### STEP 5 — Obsidian ↔ Claude Chat handoff (Will + I do this)
- I write vault docs directly (via Desktop Commander in this session)
- Obsidian reads them via file system — instant sync
- Graph view in Obsidian shows relationships once wikilinks are added
- Dataview queries in DASHBOARD.md auto-surface UNCONFIRMED + FOR HUMAN REVIEW items

**Wikilinks needed** (I can write these): All branch files in 01_BRANCHES/ need `[[wikilinks]]` added. Say "add wikilinks to branch files" and I'll do it.

### STEP 6 — Antigravity integration (Confirmed)
Antigravity executes integration workflows:
- Builds, runs, and monitors backend scripts (like the Ollama daemon and ingest automation).
- Researches external API documentation and updates integration blueprints.
- Spawns specialized subagents for parallel research or deep code audits.

---

## VERSION 2 — FULL STACK WITH CLAUDE CODE + COWORK

Same as Version 1, PLUS:

### Claude Code — what it adds
Claude Code has direct file system access. It replaces me (Claude Chat) for all file operations.

**Task routing:**
| Task | Before Code | With Code |
|------|-------------|-----------|
| Write/edit vault files | I write, Will copies | Code writes directly |
| Run Python scripts | Will runs in terminal | Code can execute |
| Git commits | Will runs git | Code can run git |
| Bulk file creation | I generate, Will saves | Code creates files |
| Read vault for context | I ask, Will pastes | Code reads any file |

**How to use Claude Code for vault work:**
1. Open Code tab in Claude Desktop app
2. Code reads CLAUDE.md automatically (already optimized)
3. Say "edit [filename]" and Code edits it directly
4. Code can run: `git add . && git commit -m "message"` without Will touching terminal

**IMPORTANT:** Claude Code and Claude Chat are separate sessions. They don't share memory. CLAUDE.md + COMPRESSED_CONTEXT.md exist to give Code the same context I have.

### Claude Cowork — what it adds
INFERENCE: Cowork handles desktop-level automation without code.

**Likely task routing for SFV:**
- Moving delivered files from Desktop to Seagate (5TB active storage)
- Organizing 99_INBOX/ — auto-sort dropped files
- Opening Obsidian, running daemon, checking OLLAMA_RESULTS.md on session start
- File naming enforcement (NAMING_CONVENTIONS.md rules)
- Pre-delivery folder prep (Pixieset structure)

**How to use Cowork:**
1. Open Claude in the desktop Cowork interface
2. Describe the task in plain language
3. Cowork executes — no code required

**NOTE:** Cowork cannot edit vault files intelligently — that's Claude Code's job. Cowork moves/organizes, Code writes.

---

## MODEL ROUTING — WHERE EACH CLAUDE FITS

```
DECISION TREE:

Is it a planning/blueprint decision?
  → Claude Chat (Sonnet 4.6) — THIS interface

Is it a complex decision that Sonnet can't crack?
  → Claude Chat (Opus 4.6) — Will explicitly requests

Does it require editing vault files or running code?
  → Claude Code (Sonnet 4.6) — Code tab

Does it require moving files or desktop automation?
  → Claude Cowork — desktop app

Is it repeatable, bulk, or overnight?
  → Ollama qwen3:14b — TASK_QUEUE.md → OLLAMA_RESULTS.md

Is it a complex system integration (requires planning, scripting, local execution, and API research)?
  → Antigravity — agentic executor

```

### Specific task examples:

| Task | Tool | Reasoning |
|------|------|-----------|
| Build INGEST.md workflow | Claude Chat | Blueprint planning = Chat |
| Actually write INGEST.md to vault | Claude Code | File write = Code |
| Pull qwen3:14b | Will + Terminal | Hardware command |
| Draft 50 Morning Walk captions | Ollama | Bulk, repeatable, free |
| Audit branch files for missing fields | Ollama (overnight) | Batch audit = TASK_QUEUE |
| Organize delivered Morning Walk files | Cowork | File routing = Cowork |
| Complex SFV_EVENTS monetization decision | Opus | Hard reasoning = Opus |
| Auto-fill Pixieset delivery folders | Cowork | Desktop automation |
| Write Python processing script | Claude Code | Code = Code |
| Summarize athlete footage for caption | Ollama | Local inference, free |
| Web research for competitor analysis | Antigravity (UNCONFIRMED) | Browser agent? |

---

## TOKEN OPTIMIZATION — FULL SYSTEM

### Rule 1: Ollama absorbs all volume
Every task that is repeatable, bulk, or low-stakes goes to TASK_QUEUE.md.
These cost $0 Claude tokens. Examples:
- Caption drafting (all branches)
- Content summarization
- Audit checks (field completeness, naming convention violations)
- Hashtag research
- Overnight batch processing

### Rule 2: Compressed context — never paste full vault into chat
- COMPRESSED_CONTEXT.md = session fuel for Claude Chat
- CLAUDE.md = session fuel for Claude Code
- SESSION_STATE.md = 3-line report only, then wait
- Never read full branch files into chat unless Will asks for deep work on that branch

### Rule 3: Locked decisions never get re-explained
See LOCKED section in SESSION_STATE.md. I never re-argue or re-discuss these. Zero tokens.

### Rule 4: File paths not file contents in Claude Code prompts
WRONG: "Here's the content of INGEST.md: [2000 tokens of content]..."
RIGHT: "Edit C:\SFV_BLUEPRINT\04_WORKFLOWS\INGEST.md — add section..."

### Rule 5: Sonnet default, Opus on request only
Sonnet 4.6 handles 95%+ of all SFV blueprint work. Opus only when Will explicitly says so.

### Rule 6: Batch before you prompt
If Will has 5 related questions → ask them all at once. Each session start = 1 read of 3 files only.

### Rule 7: Antigravity for integrations and automation
Antigravity handles local development, scripting, execution, and web research, reducing token usage on manual file syncing and external documentation lookups.

---

## OPTIMAL DAILY WORKFLOW (VERSION 2 — FULL STACK)

### Morning (session start)
1. R&D Terminal: Daemon running overnight → OLLAMA_RESULTS.md has output
2. Will opens Claude Chat → I read 3 files → 3-line report → wait
3. Will reviews OLLAMA_RESULTS.md in Obsidian → approves/flags overnight work
4. Will gives direction → I plan → Claude Code executes vault edits

### Active build session
- Claude Chat: blueprint decisions, planning, architecture
- Claude Code: writing to vault, running scripts, git commits
- Cowork: file organization, delivery prep (runs in background)
- Antigravity: (UNCONFIRMED tasks) — parallel to above
- Obsidian: Will reviews graph, runs Dataview queries, flags FOR HUMAN REVIEW

### Before session end
- I update SESSION_STATE.md with what happened (Claude Code writes it)
- I seed TASK_QUEUE.md with overnight Ollama jobs
- Will confirms git commit: `git add . && git commit -m "session YYYY-MM-DD"`

---

## WHAT I CAN DO RIGHT NOW (this session, Claude Chat)

✅ Write any vault file to disk (via Desktop Commander)
✅ Update SESSION_STATE.md, DASHBOARD.md, any .md file
✅ Design workflow documents (INGEST.md, DELIVERY.md, etc.)
✅ Write Python scripts (ollama_daemon improvements, etc.)
✅ Update COST_ROUTING.md with new model/tool routing
✅ Add wikilinks to branch files
✅ Seed TASK_QUEUE.md with Ollama jobs

❌ Run terminal commands (Will runs these)
❌ Install Obsidian plugins (Will clicks)
❌ Configure Antigravity (pending confirmation of what it is)
❌ Pull/start Ollama (R&D Terminal — Will)

---

## NEXT ACTIONS (in priority order)

1. **Will runs:** `ollama list` — confirm qwen3:14b pulled
2. **Will installs:** Local GPT + Smart Connections in Obsidian
3. **I build:** 04_WORKFLOWS/INGEST.md — May 28 deadline (say "build INGEST.md")
4. **I build:** 08_TESTS/PAPER_TRIAL_RUNS.md — Morning Walk walkthrough
5. **I update:** COST_ROUTING.md — add Antigravity + Cowork routing rules
6. **I add:** Wikilinks to all branch files (say "add wikilinks")

---
*INFERENCE markers: Antigravity role, Cowork specific SFV tasks — FOR HUMAN REVIEW*
*Everything else: based on confirmed vault state as of 2026-05-24*

## CONNECTED FILES
- [[SESSION_STATE|Session State]]
- [[DASHBOARD|Dashboard]]
- [[QUESTIONS_FOR_WILL|Questions for Will]]
- [[COMPRESSED_CONTEXT|Compressed Context]]
- [[ANTIGRAVITY|Antigravity]]
- [[OLLAMA_SETUP|Ollama Setup]]
- [[CURRENT_DIRECTIVE|Current Directive]]
- [[MASTER_CONTEXT|Master Context]]
