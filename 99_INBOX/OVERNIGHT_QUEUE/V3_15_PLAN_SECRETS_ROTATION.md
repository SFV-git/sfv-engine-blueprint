---
STATUS: ACTIVE
DIRECTIVE_ID: PLAN-20260701-SECRETS-ROTATION-CHECKLIST-001
EXECUTOR: ollama
---

Draft a general-purpose "API Key Rotation Checklist" for a solo operator rotating a compromised or cleartext-exposed API key (e.g. a search API key that was accidentally left in plaintext in a config file). Cover: generate new key at provider, update the key everywhere it's referenced, revoke the old key, restart any dependent service, verify the new key works with a small test call, and log the rotation with a timestamp. Output only the finished markdown checklist, no preamble.
