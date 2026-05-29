---
STATUS: UNCONFIRMED
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# INTEGRATIONS

How external tools connect to the SFV Engine.

---

## PIXIESET
- Purpose: client photo gallery delivery
- Confirmed for: SFV_STUDIO
- Status for SFV_EVENTS: UNCONFIRMED
- Integration: manual upload for now, API integration later
- Gallery type: collective gallery, subjects self-claim

## INSTAGRAM (8 accounts)
- SFV_abbass, SFV_LIVE, SFV_EVENTS, SFV_ATHLETICS,
  SFV_STUDIO, SFV_UGC, SFV_ARCHIVE, SFV_WORLD, SFV_404
- Scheduling tool: UNCONFIRMED (Later vs Buffer)
- Accounts with engine scheduling: EVENTS, STUDIO, UGC, LIVE, ATHLETICS, ARCHIVE, WORLD, 404
- abbass: manual posting

## ARE.NA
- Purpose: myth-building overflow content
- Branches: MYTHOLOGY, SFV_WORLD (unused content)
- Integration: manual upload [possible API later]

## GOOGLE DRIVE
- Purpose: overflow video storage, proxy storage
- Not used for primary structure
- Other shooters can deliver via Drive (Morning Walk)

## ICLOUD
- Purpose: personal backup
- Not integrated into Engine workflows

## WETRANSFER
- Purpose: current client delivery (temporary)
- Will be replaced by proper delivery system

## TAILSCALE [UNCONFIRMED]
- Purpose: secure private network between Engine and R&D terminal
- Also: remote access to both nodes from anywhere
- Interface: web or app [UNCONFIRMED — Will's preference]

## SUPABASE [FUTURE]
- Purpose: central database for all IDs
- Tables: clients, events, persons, assets, shoots
- Schema: not yet designed

## N8N [FUTURE]
- Purpose: workflow orchestration and model routing
- Connects: Engine scripts, local models, Claude API, scheduling tools

## CONNECTED FILES
- [[06_TOOLS/TOOL_STATUS|Tool Status]]
- [[05_AI_LAYER/COST_ROUTING|Cost Routing]]
