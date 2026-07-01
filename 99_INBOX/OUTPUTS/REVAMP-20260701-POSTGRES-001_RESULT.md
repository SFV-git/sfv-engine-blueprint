# RESULT -- REVAMP-20260701-POSTGRES-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-07-01 15:20:11

---

# PostgreSQL Migration Runbook for n8n (SFV Engine)

## 1. Prerequisites  
- **Docker must be running** on the Engine Body (Ryzen 9 9900X, RTX 5080, Windows 11).  
- **Backup SQLite data**:  
  - Stop the current n8n container (if running).  
  - Locate the SQLite database file (typically in the n8n Docker volume, e.g., `~/.n8n` or the host-mounted directory).  
  - Copy the SQLite file to a secure backup location (e.g., `n8n_sqlite_backup.db`).  

## 2. Stand Up PostgreSQL Container  
- **Create a named Docker volume** for PostgreSQL data:  
  ```bash
  docker volume create postgres_data
  ```  
- **Run PostgreSQL container** with persistent volume and network access:  
  ```bash
  docker run --name postgres_n8n -e POSTGRES_USER=n8n_user -e POSTGRES_PASSWORD=your_secure_password -e POSTGRES_DB=n8n_db -v postgres_data:/var/lib/postgresql/data -p 5432:5432 -d postgres
  ```  
  [UNCONFIRMED — verify against current n8n docs]: Confirm PostgreSQL image version compatibility.  

## 3. Configure n8n for PostgreSQL  
- **Set environment variables** in the n8n Docker container (or host environment):  
  ```bash
  DB_TYPE=postgres
  DB_POSTGRESDB_HOST=postgres_n8n
  DB_POSTGRESDB_PORT=5432
  DB_POSTGRESDB_DATABASE=n8n_db
  DB_POSTGRESDB_USER=n8n_user
  DB_POSTGRESDB_PASSWORD=your_secure_password
  ```  
  - Ensure `DB_POSTGRESDB_HOST` matches the PostgreSQL container name.  
  - If using a custom network, ensure both containers are on the same network.  

## 4. Export and Re-Import n8n Data  
- **Export workflows and credentials** before migration:  
  - Use n8n's REST API with an API key:  
    ```bash
    curl -X GET "http://localhost:5000/rest/workflows" -H "Authorization: Bearer <your_api_key>" -o workflows_export.json
    curl -X GET "http://localhost:5000/rest/credentials" -H "Authorization: Bearer <your_api_key>" -o credentials_export.json
    ```  
- **Re-import data after migration**:  
  - Use the same API endpoints to import the exported files.  

## 5. Verification Steps  
- **Check n8n health**:  
  ```bash
  curl -X GET "http://localhost:5000/health"
  ```  
  - Expect HTTP 200 OK.  
- **Verify workflows/credentials**:  
  - Log in to the n8n UI and confirm workflows and credentials are present.  
- **Test execution**:  
  - Trigger a sample workflow and confirm it completes without errors.  

## 6. Rollback Procedure  
- **Stop PostgreSQL container**:  
  ```bash
  docker stop postgres_n8n
  ```  
- **Remove PostgreSQL volume** (data will be lost):  
  ```bash
  docker volume rm postgres_data
  ```  
- **Revert n8n to SQLite**:  
  - Remove PostgreSQL environment variables and restart n8n with default SQLite settings.  
- **Restore SQLite backup**:  
  - Copy the previously backed-up `n8n_sqlite_backup.db` into the n8n data directory.  
  - Restart the n8n container.  

---  
**Notes**:  
- Ensure PostgreSQL and n8n containers can communicate (same Docker network).  
- Test PostgreSQL connectivity with `psql` or a client before proceeding.  
- [UNCONFIRMED — verify against current n8n docs]: Confirm if `DB_POSTGRESDB_DATABASE` must match `POSTGRES_DB` exactly.
