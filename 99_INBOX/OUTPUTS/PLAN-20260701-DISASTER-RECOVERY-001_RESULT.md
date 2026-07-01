# RESULT -- PLAN-20260701-DISASTER-RECOVERY-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-07-01 01:57:12

---

```markdown
# Recovery Runbook: Automation Server Down

## 1. Immediate Checks
- **Power**: Confirm the machine is powered on and the power cable is securely connected.
- **Network**: Verify the server has a stable internet connection and is reachable via SSH or local network tools.
- **Process Status**:
  - Run `systemctl status n8n` and `systemctl status ollama` to check if services are active.
  - Use `ps aux | grep n8n` and `ps aux | grep ollama` to confirm processes are running.
  - Check logs for errors: `journalctl -u n8n` and `journalctl -u ollama`.

## 2. Restore n8n from Backup
- **Locate Backup**: Access the most recent backup (stored in `/backups/n8n/` or external storage).
- **Stop n8n**: `sudo systemctl stop n8n`.
- **Replace Data**: Copy the backup's `data` directory to `/home/n8n/.n8n/` (or the configured storage path).
- **Restart n8n**: `sudo systemctl start n8n`.
- **Verify**: Open the n8n UI at `http://localhost:5678` and confirm workflows and credentials are intact.

## 3. Verify Ollama Models
- **Check Model Files**: Ensure the Ollama model directory (`~/.ollama/models/`) contains all expected files.
- **List Models**: Run `ollama list` to confirm models are present and functional.
- **Test Model Load**: Use `ollama run <model-name>` to verify a model loads without errors.

## 4. Final "Confirm Everything Works" Checklist
- [ ] n8n is running and all workflows are visible in the UI.
- [ ] Ollama services are active and models are listed with no errors.
- [ ] The local automation vault (e.g., `/vault/`) is accessible and files are intact.
- [ ] Network connectivity is stable (ping external services, test SSH access).
- [ ] Run a test automation workflow to confirm end-to-end functionality.
- [ ] Document the incident in the studio's incident log with timestamps and resolution steps.
- [ ] Monitor server logs (`journalctl -f`) for 1 hour post-restart to ensure no recurring issues.
```
