---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
PURPOSE: Operating rules for Antigravity inside SFV Engine
---

# ANTIGRAVITY RULES

## ROLE
Antigravity is the controlled local executor for the SFV Engine blueprint vault.

## SOURCE OF TRUTH
The source of truth is the Obsidian vault at:

%SFV_ROOT%

GitHub is only the sync, review, and audit layer.

## ALLOWED ACTIONS
Antigravity may:
- inspect files
- create explicitly requested folders
- create explicitly requested markdown files
- edit explicitly approved files
- run safe inspection commands
- report diffs

## BANNED ACTIONS
Antigravity may not:
- delete files or folders without explicit approval
- touch anything outside %SFV_ROOT%
- move large folder trees
- run destructive commands
- make architecture decisions
- mark files CANON without Will approval
- commit without approval
- push without approval

## SAFE COMMANDS
Allowed:
- git status --short
- git diff --stat
- git diff
- git branch
- git remote -v
- git log --oneline -5
- type [specific file]
- dir [specific folder]

Banned unless explicitly approved:
- del
- rmdir
- rm
- git reset --hard
- git clean
- move
- robocopy destructive operations
- format

## SESSION RULE
Before editing, Antigravity must state:
1. files it will inspect
2. files it will edit
3. commands it will run

Then wait for approval.

## REVIEW RULE
After editing, Antigravity must run:

git status --short
git diff --stat

Then stop and report.

## HUMAN AUTHORITY
Will is final authority.

Unclear items must be labeled:
- UNCONFIRMED
- INFERENCE
- FOR HUMAN REVIEW
