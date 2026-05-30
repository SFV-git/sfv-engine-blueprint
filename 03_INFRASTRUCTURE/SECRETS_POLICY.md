---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE
---

# SECRETS POLICY — API KEYS AND CREDENTIALS

---

## CURRENT STATE

| Secret | Location | Gitignored? | Encrypted? | Status |
|---|---|---|---|---|
| Tavily API key | `n8n_env.ps1` | ✅ yes | ❌ no | ACTIVE — live in n8n |
| Perplexity API key | `n8n_env.ps1` | ✅ yes | ❌ no | web-only (no API calls yet) |
| PostgreSQL password | not yet set | — | — | PENDING — set before migration |
| n8n encryption key | n8n auto-generated | ✅ (in .n8n/) | ✅ by n8n | ACTIVE |
| Future: Gemini API key | not set | — | — | FUTURE |
| Future: Claude API key | not set | — | — | FUTURE |

**Risk:** `n8n_env.ps1` sits in plaintext on `C:\`. If Engine Body is compromised, all keys are exposed.

---

## STORAGE RULES

1. **n8n_env.ps1 is the only place API keys live.** Never paste them into vault `.md` files, workflow JSON files, or commit messages.
2. **n8n_env.ps1 stays gitignored.** `n8n_env.template.ps1` (placeholder values only) is the git-tracked version.
3. **Never log API keys to DECISION_LOG.md or OLLAMA_RESULTS.md.** n8n workflows must not echo key values to output files.
4. **PostgreSQL password:** set only in `n8n_env.ps1` and never in any other file.

---

## ROTATION PLAN

| Key | Rotation trigger | How to rotate |
|---|---|---|
| Tavily | Quarterly OR on suspected exposure | tavily.ai dashboard → regenerate → update n8n_env.ps1 → restart n8n |
| Perplexity | Quarterly OR on suspected exposure | perplexity.ai settings → regenerate → update n8n_env.ps1 |
| PostgreSQL password | On suspected exposure only | `ALTER USER n8n WITH PASSWORD '[new]'` → update n8n_env.ps1 → restart n8n |
| Future cloud keys | Per provider recommendation | Same pattern: regenerate → update n8n_env.ps1 → restart |

**Rotation log:** Append to `00_DEV_LOG/DECISIONS.md` with date and "KEY ROTATED" note — no key values, just the event.

---

## ENCRYPTION AT REST

**Current:** Plaintext on local disk, gitignored. Acceptable for a single-user local system.

**[FOR HUMAN REVIEW]:** If Engine Body is ever internet-accessible (e.g., Tailscale remote access from outside LAN), consider:
- Windows Credential Manager for secret storage instead of `.ps1` file
- Or: use n8n's built-in credential store (encrypted with n8n's key) and remove API keys from `n8n_env.ps1` entirely

**Recommend:** Defer encryption-at-rest hardening until remote access is enabled. Not blocking current stack.

---

## ACCESS CONTROL

- Only Will has access to Engine Body directly
- n8n runs on localhost only — not exposed to LAN (port 5678 bound to 127.0.0.1)
- Ollama runs on `0.0.0.0:11434` — accessible from R&D Terminal (192.168.137.0/24 only per firewall rules)
- n8n_env.ps1 is not accessible from R&D Terminal (no share configured for C:\)

**If adding Tailscale remote access:** review all ports. n8n should remain localhost-only even when Tailscale is active.

---

## n8n CREDENTIAL STORE (alternative to env vars)

n8n has a built-in encrypted credential store (Settings → Credentials). Keys stored there are encrypted with n8n's encryption key (`N8N_ENCRYPTION_KEY` env var or auto-generated).

**Advantage:** Keys don't appear in `n8n_env.ps1` at all — managed inside n8n UI.
**Trade-off:** Harder to script; credentials must be re-entered if n8n is reinstalled.

**[FOR HUMAN REVIEW]:** Migrate Tavily and future cloud keys to n8n credential store after PostgreSQL migration is stable? Recommend: yes, in Phase 2.

---

## PRE-MIGRATION CHECKLIST

Before running POSTGRES_MIGRATION.md:
- [ ] Set `N8N_DB_PASSWORD` — record it somewhere secure (password manager)
- [ ] Add PostgreSQL vars to `n8n_env.ps1`
- [ ] Add PostgreSQL placeholder vars to `n8n_env.template.ps1`

---

## CONNECTED FILES
- [[POSTGRES_MIGRATION|PostgreSQL Migration]]
- [[ENGINE_COMMUNICATION_MODEL|Engine Communication Model]]
- [[AI_STACK_ARCHITECTURE_BLUEPRINT|AI Stack Architecture]]
- [[FAILOVER_MODEL|Failover Model]]
