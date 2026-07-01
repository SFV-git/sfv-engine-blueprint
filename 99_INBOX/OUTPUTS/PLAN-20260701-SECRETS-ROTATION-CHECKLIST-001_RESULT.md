# RESULT -- PLAN-20260701-SECRETS-ROTATION-CHECKLIST-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-07-01 01:58:25

---

```markdown
# API Key Rotation Checklist

- [ ] **Generate New Key**  
  - Log in to the API provider's management console.  
  - Navigate to the API key generation section.  
  - Create a new API key with appropriate permissions.  
  - Save the new key in a secure password manager or encrypted file.  

- [ ] **Update Key References**  
  - Search all code repositories, config files, and environment variables for the old key.  
  - Replace the old key with the new one in:  
    - Application configuration files (e.g., `.env`, `config.yaml`).  
    - Hardcoded values in source code.  
    - CI/CD pipelines or deployment scripts.  
    - Cloud provider secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault).  
  - Commit changes with a clear message (e.g., "Rotate API key for [service]").  

- [ ] **Revoke Old Key**  
  - Access the API provider's console or use their API to delete the compromised key.  
  - Confirm the old key is marked as revoked or deleted.  
  - Note any provider-specific steps for key revocation (e.g., disabling access, setting expiration).  

- [ ] **Restart Dependent Services**  
  - Restart any services, servers, or containers that use the API key (e.g., backend apps, cron jobs).  
  - Ensure load balancers, proxies, or orchestration tools (e.g., Kubernetes) are updated.  
  - Verify that services are no longer using the old key (e.g., via logs or monitoring).  

- [ ] **Verify New Key Functionality**  
  - Make a small test call to the API using the new key (e.g., a `GET /health` endpoint).  
  - Confirm the response is successful (e.g., HTTP 200 OK) and there are no authentication errors.  
  - Check logs for any unexpected behavior or errors related to the new key.  

- [ ] **Log Rotation Details**  
  - Record the rotation in a secure audit log with a timestamp (e.g., "2023-10-05T14:30:00Z").  
  - Include:  
    - Old key (if still accessible).  
    - New key (hashed or redacted for security).  
    - Services affected by the rotation.  
    - Notes on the reason for rotation (e.g., "Exposure in config file").  
  - Store logs in a secure, versioned location (e.g., encrypted file, audit database).  
```
