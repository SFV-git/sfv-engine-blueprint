---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE — after install, update docker references in AI_STACK_ARCHITECTURE_BLUEPRINT to CONFIRMED
---

# DOCKER INSTALL CHECKLIST — ENGINE BODY

> Docker is approved (2026-05-26). Install requires a restart — do at end of a session.
> This doc tracks what blocks on Docker and what to confirm after install.

---

## INSTALL STEPS (Will runs)

1. Download Docker Desktop for Windows from docker.com
2. Run installer — accept defaults
3. Enable WSL2 integration when prompted (required on Windows 11)
4. **Restart Engine Body**
5. After restart: open Docker Desktop — confirm daemon is running (whale icon in taskbar)
6. Verify in terminal:
   ```
   docker --version
   docker run hello-world
   ```

---

## WHAT UNLOCKS AFTER DOCKER

| Blocked item | Gap # | After Docker |
|---|---|---|
| Open WebUI | Gap 11 | Deploy per OPEN_WEBUI_SPEC.md |
| n8n-MCP server | Gap 7 | Deploy per N8N_MCP_SPEC.md |
| n8n queue mode (Redis) | Gap 16 | Redis container |
| Client Review Gateway | RD_TERMINAL_ARCHITECTURE Role 2 | nginx + app container |
| Trading sandbox | RD_TERMINAL_ARCHITECTURE Role 4 | isolated container |

---

## POST-INSTALL — UPDATE THESE REFERENCES

After Docker is confirmed running, update the following to remove [FUTURE] / DEFERRED tags:

| File | Section | Change |
|---|---|---|
| `AI_STACK_ARCHITECTURE_BLUEPRINT.md` §7 | Deploy n8n-MCP via Docker | Phase 1 → ACTIVE |
| `AI_STACK_ARCHITECTURE_BLUEPRINT.md` §7 | Deploy Open WebUI | Phase 1 → ACTIVE |
| `RD_TERMINAL_ARCHITECTURE.md` Role 2 | Docker required | DEFERRED → ACTIVE |
| `RD_TERMINAL_ARCHITECTURE.md` Role 4 | Docker container | DEFERRED → ACTIVE |
| This file | STATUS | FOR HUMAN REVIEW → CANON |

---

## CONNECTED FILES
- [[AI_STACK_ARCHITECTURE_BLUEPRINT|AI Stack Architecture]]
- [[OPEN_WEBUI_SPEC|Open WebUI Spec]]
- [[N8N_MCP_SPEC|n8n-MCP Spec]]
- [[RD_TERMINAL_ARCHITECTURE|R&D Terminal Architecture]]
- [[CONCURRENCY_QUEUE_SPEC|Concurrency and Queue Mode]]
- [[TOOLBOX|Toolbox]]
