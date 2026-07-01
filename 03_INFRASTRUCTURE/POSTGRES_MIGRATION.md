---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE
---

# POSTGRES MIGRATION — n8n OFF SQLITE

> Critical before any concurrent execution scaling. SQLite corrupts under parallel webhook hits.
> Will supervises this migration. Do not run unsupervised.

---

## CONTEXT

n8n currently uses SQLite at its default data path. SQLite is single-writer — parallel executions and queue mode will cause database lock errors or corruption. PostgreSQL is the n8n-recommended production database.

**Blocks until complete:** Redis queue mode, concurrent workflow execution, n8n scaling beyond single-threaded operation.

---

## PRE-MIGRATION — BACKUP SQLITE

Run before touching anything:

```powershell
# Find n8n data directory (default location)
$n8nData = "$env:USERPROFILE\.n8n"

# Stop n8n before backing up
# (close the n8n window or stop the process)

# Copy entire .n8n folder
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item -Recurse "$n8nData" "$n8nData`_BACKUP_$timestamp"
```

Verify backup exists before proceeding:
```
C:\Users\[user]\.n8n_BACKUP_[timestamp]\
  database.sqlite   ← the critical file
  config            ← n8n configuration
```

---

## POSTGRESQL INSTALL (Node A — Engine Body)

**Option A — native Windows install (recommended for stability)**
1. Download PostgreSQL 15 installer from postgresql.org
2. Install to default location (`C:\Program Files\PostgreSQL\15\`)
3. Set superuser password — record it (use a strong password, store in secrets policy)
4. Default port: 5432 — accept default
5. Deselect pgAdmin if not needed (saves space)
6. Complete install

**Option B — Docker (requires Docker installed first)**
```
docker run -d \
  --name n8n-postgres \
  -e POSTGRES_USER=n8n \
  -e POSTGRES_PASSWORD=[PASSWORD] \
  -e POSTGRES_DB=n8n \
  -p 5432:5432 \
  postgres:15
```
[INFERENCE: Docker option is cleaner for future migration/backup, but AI_STACK_ARCHITECTURE_BLUEPRINT §2 assigns PostgreSQL to C:\ (SSD) for webhook performance — this aligns with Option A (native install). Use Option B only if Will explicitly decides to change the storage allocation. Confirm before choosing.]

---

## CREATE n8n DATABASE + USER

Run in psql (as postgres superuser):

```sql
CREATE USER n8n WITH PASSWORD '[N8N_DB_PASSWORD]';
CREATE DATABASE n8n OWNER n8n;
GRANT ALL PRIVILEGES ON DATABASE n8n TO n8n;
```

[FOR HUMAN REVIEW: N8N_DB_PASSWORD must be set before running. Add to secrets policy before this step.]

---

## N8N ENVIRONMENT CONFIGURATION

Add these to `n8n_env.ps1` (already gitignored):

```powershell
$env:DB_TYPE                  = "postgresdb"
$env:DB_POSTGRESDB_HOST       = "localhost"
$env:DB_POSTGRESDB_PORT       = "5432"
$env:DB_POSTGRESDB_DATABASE   = "n8n"
$env:DB_POSTGRESDB_USER       = "n8n"
$env:DB_POSTGRESDB_PASSWORD   = "[N8N_DB_PASSWORD]"
$env:DB_POSTGRESDB_SCHEMA     = "public"
```

Also add to `n8n_env.template.ps1` with placeholder values for git safety.

---

## MIGRATION RUN

n8n handles the SQLite → PostgreSQL migration automatically on first startup with new DB config.

1. Ensure PostgreSQL is running and n8n DB user exists
2. Update `n8n_env.ps1` with PostgreSQL vars
3. Start n8n via `start_n8n.ps1` as normal
4. n8n will detect the new database and run its internal migration
5. Monitor the n8n console output — migration logs will appear
6. Migration typically takes 1–5 minutes depending on existing data volume

---

## VALIDATION CHECKS

After startup with PostgreSQL:

| Check | Pass criteria |
|---|---|
| n8n loads without errors | Console shows no DB connection errors |
| Workflows are visible | All workflows appear in n8n UI |
| Workflow history preserved | Execution history visible in n8n UI |
| File trigger fires | Drop a test JSON in QUEUE/ — workflow executes |
| Concurrent test | Drop 3 JSON files simultaneously — all process without lock error |

---

## ROLLBACK PLAN

If migration fails or n8n fails to start:

1. Stop n8n
2. Remove PostgreSQL env vars from `n8n_env.ps1`
3. Restore SQLite backup:
   ```powershell
   Copy-Item "$env:USERPROFILE\.n8n_BACKUP_[timestamp]\database.sqlite" `
             "$env:USERPROFILE\.n8n\database.sqlite"
   ```
4. Restart n8n — it will read SQLite again
5. Log failure to `00_DEV_LOG/QUESTIONS_FOR_WILL.md` with error output

---

## WHAT UNLOCKS AFTER MIGRATION

| Blocked item | Unlocks |
|---|---|
| Redis queue mode | Safe concurrent execution |
| Parallel webhook handling | Multiple triggers fire simultaneously |
| n8n scaling to multiple workers | Queue mode pre-requisite |
| Gap 16 (concurrency spec) | Can be implemented once PostgreSQL is live |

---

## CONNECTED FILES
- [[AI_STACK_ARCHITECTURE_BLUEPRINT|AI Stack Architecture Blueprint]]
- [[DATABANK_ARCHITECTURE|Databank Architecture]]
- [[SESSION_STATE|Session State]]
- [[RATE_LIMITS|Rate Limits]]
- [[TOOLBOX|Toolbox]]
