---
STATUS: CANON
VERSION: v0.2.0
OWNER: WILL
LAST_UPDATED: 2026-05-25
---

# ANTIGRAVITY RULES

## WHAT IT IS
Google Antigravity 2.0 — agentic development platform (IDE + CLI + SDK).
Launched Google I/O 2026. VS Code fork. Runs multiple AI agents in parallel.
Supports: Gemini 3.5 Flash (default, FREE), Gemini 3.1 Pro, Claude Sonnet 4.6, Claude Opus 4.6.
Desktop app: antigravity.google

## CURRENT SETUP — PROBLEM
Antigravity is running Claude Sonnet/Opus as its model.
This burns Anthropic API tokens for work Gemini 3.5 Flash handles equally well.

## FIX (Will does once — 2 minutes)
```
Antigravity Settings → Model → Gemini 3.5 Flash
Keep Claude Sonnet available as secondary for complex blueprint decisions only.
```
After this: Antigravity runs free during preview. Zero token spend on routine work.

## ROLE IN SFV STACK
Antigravity is the PRIMARY BUILD ENVIRONMENT for the vault.
It replaces ad-hoc Claude Code sessions for most build tasks.

| What to use Antigravity for | Model |
|-----------------------------|-------|
| Writing vault .md files | Gemini 3.5 Flash (free) |
| Building Python scripts (ingest.py, daemon, etc.) | Gemini 3.5 Flash (free) |
| Git audits, status, diff inspection | Gemini 3.5 Flash (free) |
| Running parallel agents on multiple modules | Gemini 3.5 Flash (free) |
| Scheduled background vault tasks | Gemini 3.5 Flash (free) |
| Complex architecture decisions | Claude Sonnet 4.6 (when needed) |
| Hard cross-module reasoning | Claude Opus 4.6 (explicit request only) |

## ANTIGRAVITY vs CLAUDE CODE
| Situation | Use |
|-----------|-----|
| Building multiple vault files at once | Antigravity (parallel agents) |
| Background scheduled build tasks | Antigravity (scheduled tasks) |
| Single focused module, deep context | Claude Code |
| Planning and blueprint decisions | Claude Chat (this interface) |

## WORKSPACE SETUP
Point Antigravity at: C:\SFV_BLUEPRINT
Context file for Antigravity sessions: ANTIGRAVITY.md (to be created — mirrors CLAUDE.md)

## SOURCE OF TRUTH
The source of truth is the Obsidian vault at C:\SFV_BLUEPRINT.
GitHub is only the sync, review, and audit layer.

## ALLOWED ACTIONS
Antigravity may:
- Inspect files
- Create explicitly requested folders and markdown files
- Edit explicitly approved files
- Run safe inspection commands
- Build Python scripts per spec
- Report diffs

## BANNED ACTIONS
Antigravity may not:
- Delete files or folders without explicit approval
- Touch anything outside C:\SFV_BLUEPRINT
- Make architecture decisions
- Mark files CANON without Will approval
- Commit without approval
- Push without approval

## SAFE COMMANDS
Allowed:
- git status --short
- git diff --stat
- git diff
- git branch
- git log --oneline -5

Banned without approval:
- del, rmdir, rm, git reset --hard, git clean, format

## SESSION RULE
Before editing, Antigravity must state:
1. Files it will inspect
2. Files it will edit
3. Commands it will run
Then wait for approval.

## REVIEW RULE
After editing, Antigravity must run:
  git status --short
  git diff --stat
Then stop and report.

## PARALLEL AGENT USE
Antigravity 2.0 can run multiple agents simultaneously.
Use for: building multiple workflow .md files at once, parallel script + doc builds.
Each agent still follows the approval gate above.

## SCHEDULED TASKS
Antigravity can schedule background tasks.
Use for: overnight vault audits, doc consistency checks.
These complement (not replace) the Ollama daemon — Ollama handles AI inference tasks,
Antigravity handles code and file structure tasks.

## RATE LIMITS
- Gemini 3.5 Flash: effectively unlimited during free preview
- Preview end date: not announced — build with this now
- AI Ultra plan ($100/mo): 5x Pro limits when preview ends
- Claude models inside Antigravity: hits Anthropic API quota — use sparingly

## HUMAN AUTHORITY
Will is final authority.
Unclear items labeled: UNCONFIRMED / INFERENCE / FOR HUMAN REVIEW
