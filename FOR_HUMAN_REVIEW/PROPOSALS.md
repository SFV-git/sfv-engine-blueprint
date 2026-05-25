---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# FOR HUMAN REVIEW — PROPOSALS

Claude proposals awaiting Will's decision.
Nothing here gets built until Will explicitly approves.

---

## OPEN PROPOSALS

### PROPOSAL 001 — OpenClaw as R&D Terminal Agent
Date: 2026-05-24
Proposed by: Claude

OpenClaw is an open source autonomous AI agent (250k+ GitHub stars).
Runs locally on R&D terminal. 100+ built-in skills.
Handles file operations, research, proposal generation continuously.
Bring your own API key — no subscription needed.

Potential role: R&D terminal's autonomous layer.
Would handle: routine research, trend monitoring, blueprint audits.
Risk: ecosystem still experimental.

Decision needed: YES / NO / RESEARCH MORE

---

### PROPOSAL 002 — Tailscale for Node Connection
Date: 2026-05-24
Proposed by: Claude

Tailscale creates a private encrypted network between Engine and R&D terminal.
Also enables remote access from anywhere (school, location shoots).
Free tier available. Simple setup.

Decision needed: APPROVE / EVALUATE ALTERNATIVES

---

### PROPOSAL 003 — UPS for Engine Protection
Date: 2026-05-24
Proposed by: Claude

Recommendation: APC Back-UPS 1500VA (~$150 CAD)
Protects overnight runs from power interruption.
Prevents corrupt files during ingest.
Relevant given electricity constraint at lab location.

Decision needed: YES / NOT YET / DIFFERENT SPEC

---

### PROPOSAL 004 — R&D Terminal Idle Throttling
Date: 2026-05-24
Proposed by: Claude

R&D terminal should reduce CPU/GPU load when no active tasks.
Ollama has idle mode. Estimated 40-60% power reduction during idle.
Relevant given electricity cost concern at mall studio.

Decision needed: YES / CONFIGURE DIFFERENTLY

---

### PROPOSAL 005 — SFV World as are.na Output Channel
Date: 2026-05-24
Proposed by: Claude

Unused/overflow content from SFV_WORLD automatically queued for are.na.
Simple rule: Will rejects from WORLD → goes to are.na pipeline folder.
are.na upload: manual for now, API integration possible later.

Decision needed: YES / DIFFERENT LOGIC

---

### PROPOSAL 006 — Git Commit Convention
Date: 2026-05-24
Proposed by: Claude

Proposed commit message format:
```
feat: [new thing added]
fix: [something corrected]
docs: [blueprint updated]
vault: auto-commit [timestamp]
status: [file] moved from [old status] to [new status]
```

Decision needed: APPROVE / MODIFY FORMAT

---

### PROPOSAL 007 — Evolved R&D Terminal (Sentinel & Sandbox)
Date: 2026-05-25
Proposed by: Antigravity

Evolve the R&D Terminal from a local model box into a dashboard, client review gateway, and isolated sandbox environment.
Would handle:
- Visualizing logs and telemetry from both machines.
- Running a secure reverse proxy/caching server for client review (reels/photos) so Engine Body is isolated from the internet.
- Running a Docker sandbox for algorithmic trading (Polymarket, stocks) with a small budget ($200-$300).

Details: C:\SFV_BLUEPRINT\05_AI_LAYER\RD_TERMINAL_ARCHITECTURE.md

Decision needed: YES / NO / REVISE SPEC

---

## APPROVED PROPOSALS
[Moved here once Will approves — becomes CANON in relevant file]

---

## REJECTED PROPOSALS
[Moved here once Will rejects — stays for record]
