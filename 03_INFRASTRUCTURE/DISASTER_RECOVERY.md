---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE
---

# DISASTER RECOVERY

Recovery plan for the SFV Engine stack — vault, n8n, Ollama models, and active media.

---

## 1. WHAT NEEDS TO BE RECOVERABLE

Prioritized by irreplaceability and operational impact.

| Priority | Asset | Why critical |
|---|---|---|
| P1 | Vault — C:\SFV_BLUEPRINT | All blueprints, decisions, configuration — months of work |
| P2 | n8n database | Workflow definitions and execution history — not re-creatable from scratch |
| P3 | n8n credentials and env vars (n8n_env.ps1) | API keys and secrets — single point of failure if lost |
| P4 | Active media — D:\ | Raw files — irreplaceable originals |
| P5 | Ollama models | Large but re-pullable from Ollama registry — low risk |

---

## 2. CURRENT BACKUP STATE

| Asset | Current backup | Gap |
|---|---|---|
| Vault (C:\SFV_BLUEPRINT) | Syncthing A↔B (live sync) + Git push to GitHub | No off-site beyond GitHub; GitHub IS the off-site |
| n8n database | None | CRITICAL gap — no backup exists |
| n8n_env.ps1 (secrets) | None | CRITICAL gap — gitignored, not on Node B |
| Ollama models (D:\) | None | Low risk — re-pull from Ollama registry |
| Active media (D:\) | Robocopy nightly A→B | No off-site; both nodes on same LAN |

---

## 3. VAULT OFF-SITE BACKUP

### Current state
Git push to GitHub provides off-site backup for the vault. Syncthing provides a live second copy on Node B on the same LAN.

### Gap: n8n_env.ps1
`n8n_env.ps1` contains API keys and secrets. It is gitignored and is NOT pushed to GitHub. It is not synced by Syncthing (or if it is, it is on-LAN only). If Engine Body is destroyed, these secrets are lost.

### Fix — DECIDED: Bitwarden
Store all contents of `n8n_env.ps1` in Bitwarden under entry "SFV Engine — API keys / n8n secrets".

**Decision (Will, 2026-06):** Bitwarden is the secrets manager — chosen over Windows Credential Manager, which is machine-local and does not solve the off-site problem. **ACTION STILL PENDING: Will confirms the keys have actually been entered into Bitwarden.** Until then this gap is open.

### What to store in the password manager
- All API keys referenced in n8n_env.ps1
- Ollama endpoint URL if non-default
- PostgreSQL connection string and credentials (when PostgreSQL migration is complete)
- Any webhook secrets or signing keys

---

## 4. n8n DATABASE BACKUP

This is the most critical unaddressed gap. No backup exists for n8n workflow definitions or execution history.

### After PostgreSQL migration

```
# Daily pg_dump — run via Windows Task Scheduler or n8n cron workflow
pg_dump n8n > D:\SFV_ACTIVE\BACKUPS\n8n_[date].sql

# Retention: keep last 7 days, delete older files
# Robocopy nightly job already runs D:\ → Node B
# Point it at D:\SFV_ACTIVE\BACKUPS\ to copy n8n dumps to Node B as well
```

[FOR HUMAN REVIEW]: Should the pg_dump be triggered by a Windows Task Scheduler job or by an n8n cron workflow? If n8n itself is what runs the backup, and n8n is the thing that crashed, the backup may not run. Recommend Windows Task Scheduler for independence.

### Before PostgreSQL migration (SQLite — current state)

```
# Daily: copy SQLite database file to backup location
# Source: %USERPROFILE%\.n8n\database.sqlite
# Destination: D:\SFV_ACTIVE\BACKUPS\n8n_sqlite_[date].sqlite
# Retention: 7 days
```

[FOR HUMAN REVIEW]: The SQLite backup script has not been written yet. Script placeholder location: `C:\SFV_BLUEPRINT\99_INBOX\backup_n8n.ps1` — this needs to be built and scheduled before it provides any protection.

### Node B copy
Robocopy nightly job (already configured, A→B) should include the BACKUPS folder so n8n dumps land on Node B automatically. Verify the Robocopy source path includes BACKUPS.

---

## 5. OLLAMA MODEL RECOVERY

Ollama models are stored on D:\ (Seagate 5TB). If D:\ survives an Engine Body OS failure (drive is intact), models do not need to be re-pulled — just re-point Ollama to the existing model path.

If models must be re-pulled from scratch, recovery commands are:

```
ollama pull qwen3:14b
ollama pull qwen2.5-coder:7b
ollama pull minicpm-v:8b
```

Recovery time is download-bound (each model is 5–9 GB). Estimated total re-pull time on a standard connection: 30–90 minutes.

**MODEL_LOCK.md is the recovery checklist.** Keep it current (see MODEL_LIFECYCLE_POLICY.md). When MODEL_LOCK.md is accurate, Ollama recovery requires no guesswork.

---

## 6. ACTIVE MEDIA RECOVERY

### Current state
Raw media on D:\ is backed up nightly to Node B via Robocopy (already configured and running).

### Gap: same-LAN risk
Node B is on the same LAN as Engine Body — possibly in the same physical location. If the building is lost (fire, flood, theft), both nodes are lost simultaneously. Robocopy to Node B does not protect against this scenario.

### Off-site options

[FOR HUMAN REVIEW]: Choose one or both:

**Option A — Cloud backup (Backblaze B2)**
- Cost: approximately $7/TB/month
- Benefit: true off-site, automatic, continuous or scheduled
- Drawback: upload bandwidth required; large initial seed upload for existing D:\ content

**Option B — Periodic cold storage to external drive stored off-site**
- Cost: one-time drive cost (~$50–$80 for 2TB portable)
- Benefit: no ongoing cost, no bandwidth dependency
- Drawback: manual process, only as current as the last rotation

**Recommended approach:**
- Option B for archived and delivered content (cold storage, rotated monthly or quarterly)
- Option A for the active working set if bandwidth allows

Neither option is currently configured. This is a gap to address after the n8n backup gap (P2 above).

---

## 7. RECOVERY RUNBOOK — ENGINE BODY FAILURE

Use when Engine Body is non-functional and must be rebuilt on a replacement machine.

1. Provision a replacement Windows 11 machine
2. Install base software: Python 3.11+, Git, Ollama, Docker Desktop, n8n
3. Clone vault from GitHub:
   ```
   git clone [repo-url] C:\SFV_BLUEPRINT
   ```
4. Restore `n8n_env.ps1` from password manager — recreate the file from stored credentials
5. Restore n8n database from latest backup on Node B:
   - PostgreSQL: `psql n8n < [latest .sql file from Node B]`
   - SQLite: copy `.sqlite` file to `%USERPROFILE%\.n8n\database.sqlite`
6. Start n8n with env vars applied — all workflow definitions will be present
7. Re-pull Ollama models using MODEL_LOCK.md as the checklist (see Section 5)
8. Verify workflow1 runs a test task end-to-end

**Estimated recovery time: 2–4 hours** (assuming steps 3–5 data sources are intact and available)

[INFERENCE]: Recovery time estimate assumes broadband available for model re-pull and that Node B is intact with current backups. If Node B is also lost, n8n database recovery is not possible until the backup gap (Section 4) is addressed.

---

## 8. RECOVERY RUNBOOK — VAULT CORRUPTION

Use when C:\SFV_BLUEPRINT files are corrupted, accidentally overwritten, or partially deleted.

### Option A — Git rollback (preferred)
```
# On Engine Body or any machine with vault clone
git log --oneline                          # identify last clean commit
git checkout [clean-commit-hash] -- .      # restore all vault files to that state
git status                                 # confirm which files were restored
git commit -m "fix: restore vault to [clean-commit-hash] after corruption"
```

### Option B — Syncthing version history on Node B
Syncthing maintains version history for synced files (if version history is enabled on Node B).
Navigate to Node B Syncthing interface → browse version history for the affected file(s) → restore previous version.

[FOR HUMAN REVIEW]: Is Syncthing version history enabled on Node B? If not, Option B is not available and Git is the only rollback path.

---

## 9. GAPS SUMMARY

| Gap | Severity | Action needed |
|---|---|---|
| n8n database — no backup | CRITICAL | Build and schedule backup_n8n.ps1 |
| n8n_env.ps1 — no off-site copy | CRITICAL | Store in password manager now |
| Active media — no off-site | HIGH | Choose Option A or B from Section 6 |
| Syncthing version history — status unknown | MEDIUM | Verify Node B config |

---

## CONNECTED FILES
- [[AI_STACK_ARCHITECTURE_BLUEPRINT]]
- [[POSTGRES_MIGRATION]]
- [[SECRETS_POLICY]]
- [[FAILOVER_MODEL]]
- [[MODEL_LIFECYCLE_POLICY]]
- [[MONITORING_STACK]]
