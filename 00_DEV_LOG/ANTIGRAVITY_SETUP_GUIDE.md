---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-25
---

# ANTIGRAVITY SETUP + INGEST BUILD GUIDE

> Step-by-step. No assumptions. Every action labeled WHO DOES IT.

---

## PART 1 — ANTIGRAVITY SETUP (15 min, one time)

### Step 1 — Verify model is set to Gemini Flash
WHO: Will
WHERE: Antigravity desktop app

```
Open Antigravity
→ Click gear icon (Settings) top-right or press Ctrl+,
→ Find "Model" or "Default Model"
→ Set to: Gemini 3.5 Flash
→ Save / close settings
```
Why: Flash is fast and free during preview. Pro/Ultra burns quota faster.
Use Pro or Claude Sonnet only when you explicitly switch for a hard task.

---

### Step 2 — Confirm project is open
WHO: Will
WHERE: Antigravity desktop app

```
Left sidebar → Projects → confirm C:\SFV_BLUEPRINT is listed
If not: File → Open Folder → C:\SFV_BLUEPRINT
```
The project is already linked to GitHub — no action needed there.

---

### Step 3 — Set ANTIGRAVITY.md as context
WHO: Will
WHERE: Antigravity — new chat session

At the start of EVERY Antigravity session, paste this as your first message:

```
@ANTIGRAVITY.md
Read this file before doing anything. Confirm you understand your role in one sentence.
```

Antigravity will confirm. Then give it the task.

---

### Step 4 — Model switching shortcut
WHO: Will

For ROUTINE tasks (writing .md files, building scripts, git inspection):
→ Keep Gemini 3.5 Flash

For HARD tasks (cross-module architecture, complex reasoning):
→ Click model dropdown in chat → switch to Claude Sonnet 4.6 for that message
→ Switch back to Flash after

---

### Step 5 — Run find_orphans.py
WHO: Will
WHERE: Windows Terminal

```
python C:\SFV_BLUEPRINT\99_INBOX\find_orphans.py
```
Output: 00_DEV_LOG/ORPHANS.md
Open in Obsidian → review → add missing links manually or tell Antigravity to fix them.

---

### Step 6 — Start vault_watcher.py (keep running in background)
WHO: Will
WHERE: Windows Terminal — dedicated tab, leave open

```
python C:\SFV_BLUEPRINT\99_INBOX\vault_watcher.py
```
Every new .md file added to vault gets:
- Standard CONNECTED FILES links added automatically
- Ollama task queued to suggest additional semantic links
Leave this running whenever you're doing vault work.

---

## PART 2 — BUILD INGEST.PY IN ANTIGRAVITY

ingest.py is already written at C:\SFV_BLUEPRINT\99_INBOX\ingest.py
Use Antigravity to review, improve, and test it.

---

### Step 1 — Open Antigravity session for ingest
WHO: Will
WHERE: Antigravity — new session

Paste exactly:
```
@ANTIGRAVITY.md @04_WORKFLOWS/INGEST.md @99_INBOX/ingest.py

Review ingest.py against the spec in INGEST.md.
Do not change anything yet.
List:
1. Any spec requirements not yet implemented
2. Any bugs or edge cases you can see
3. Anything that would break for 150+ files on May 28
Output as numbered list only.
```

Read Antigravity's response carefully. It will find real issues.

---

### Step 2 — Approve improvements
WHO: Will

After reviewing Antigravity's list, respond:

```
Implement items [X, Y, Z] from your list.
Do not implement the rest yet.
After changes: run git status --short and git diff --stat. Then stop and show me.
```

Review the diff before approving anything further.

---

### Step 3 — Dry run test (no media required)
WHO: Will
WHERE: Windows Terminal

```
python C:\SFV_BLUEPRINT\99_INBOX\ingest.py --branch STUDIO --tag MORNINGWALK --dry-run
```

Expected output — validates paths and config WITHOUT needing files:
```
 SFV INGEST v2
 Branch  : STUDIO
 Tag     : MORNINGWALK

 DRY RUN — validating configuration only. No files moved.

  ✓  Active storage (D:\SFV_ACTIVE): D:\SFV_ACTIVE
  ✓  Branches root: D:\SFV_ACTIVE\BRANCHES
  ✓  ENVIRONMENT_CONFIG.md: C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\ENVIRONMENT_CONFIG.md

  Destination would be: D:\SFV_ACTIVE\BRANCHES\SFV_STUDIO\INGEST\20260528
  Rename format would be: STUDIO_20260528_MORNINGWALK_0001_RAW.arw

  Source: E:\ not connected — no files to count (expected in dry run)
  Config loaded from: ENVIRONMENT_CONFIG.md
  All paths OK
```

If any path shows ✗ NOT FOUND — fix before May 28.

---

### Step 4 — Live test with real files (do before May 28)
WHO: Will

1. Put 5-10 test photos on the SanDisk (E:\)
2. Run:
   ```
   python C:\SFV_BLUEPRINT\99_INBOX\ingest.py --branch STUDIO --date 20260527
   ```
3. Verify in File Explorer:
   - Files appear in: D:\SFV_ACTIVE\BRANCHES\SFV_STUDIO\INGEST\20260527\
   - Named: STUDIO_20260527_0001.ARW etc.
   - Log written: D:\SFV_ACTIVE\BRANCHES\SFV_STUDIO\LOGS\INGEST_LOG_20260527_STUDIO.txt
4. If anything looks wrong: tell Antigravity what happened + paste the log

---

### Step 5 — Commit when clean
WHO: Will
WHERE: Windows Terminal or Antigravity

```
git add .
git commit -m "feat: ingest.py v1 — tested and ready for May 28"
```

---

## PART 3 — MORNING WALK (MAY 28) INGEST RUN

### On the day — exact command sequence

```
# SD card in, SanDisk connected as E:\

# Studio portraits first
python C:\SFV_BLUEPRINT\99_INBOX\ingest.py --branch STUDIO --date 20260528

# Events/flashmob content (same day, different source if second card)
python C:\SFV_BLUEPRINT\99_INBOX\ingest.py --branch EVENTS --date 20260528

# Google Drive files: download → drag to D:\SFV_ACTIVE\INGEST_STAGING\
# Then:
python C:\SFV_BLUEPRINT\99_INBOX\ingest.py --branch STUDIO --source staging --date 20260528
```

### After ingest — go straight to:
1. D:\SFV_ACTIVE\BRANCHES\SFV_STUDIO\INGEST\20260528\ → open in Lightroom Classic
2. Cull, sync preset, export → EXPORT\ folder
3. Upload EXPORT\ contents to Pixieset
4. Done

---

## PART 4 — PARALLEL AGENT STRATEGY (Antigravity 2.0)

Antigravity 2.0 can run multiple agents at the same time.
Use this to build multiple blueprint docs simultaneously.

### How to spin up parallel agents:
```
In Antigravity → click "New Agent" or "+" next to the chat tab
Run separate sessions for separate modules
```

### Recommended parallel build (tonight):
- Agent 1: @ANTIGRAVITY.md @08_TESTS/PAPER_TRIAL_RUNS.md → "Build a complete May 28 walkthrough from SD card to Pixieset. Use INGEST.md as reference. Write directly to the file."
- Agent 2: @ANTIGRAVITY.md @04_WORKFLOWS/DELIVERY.md → "Build out the Pixieset delivery workflow. Reference SFV_STUDIO branch for context."
- Agent 3: @ANTIGRAVITY.md @02_BRANCHES/SFV_UGC.md → "Fill in all UNCONFIRMED fields with placeholders and FOR HUMAN REVIEW tags."

Each agent works independently. Review diffs. Approve commits separately.

---

## QUICK REFERENCE — ANTIGRAVITY SESSION STARTERS

Copy-paste these to start common Antigravity tasks:

### Review a file:
```
@ANTIGRAVITY.md @[path/to/file.md]
Review this file against vault standards. List: missing fields, UNCONFIRMED items, broken paths. Do not edit. Output list only.
```

### Build a script:
```
@ANTIGRAVITY.md @[spec-file.md] @[target-script.py if exists]
Build [script name] per the spec. Use parallel processing where applicable. No hardcoded paths — use vars from ENVIRONMENT_CONFIG.md. Show me the plan before writing code.
```

### Git audit:
```
@ANTIGRAVITY.md
Run: git status --short
Then: git diff --stat
Report what changed. Do not commit.
```

### Fix orphans (after running find_orphans.py):
```
@ANTIGRAVITY.md @00_DEV_LOG/ORPHANS.md
For each orphaned file listed, add appropriate wikilinks to its CONNECTED FILES section.
Do MYTHOLOGY and SFV_WORLD first. Show me the plan. Wait for approval.
```

---
*Built: 2026-05-25. ingest.py written and ready at 99_INBOX/ingest.py.*
*Run dry-run first. Test with real files before May 28.*

## CONNECTED FILES
- [[SESSION_STATE|Session State]]
- [[DASHBOARD|Dashboard]]
