---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# BRANCH INDEPENDENCE

## PRINCIPLE
Each branch operates independently.
Adding or removing a branch does not break others.
Scaling one branch does not require rebuilding others.

## WHAT EACH BRANCH OWNS
- Own folder structure
- Own ingest workflow
- Own export pipeline
- Own delivery system
- Own scheduling pipeline
- Own client management
- Own caption system
- Own Instagram account

## WHAT BRANCHES SHARE
- Core ingest scripts (inherited, not rebuilt)
- Naming convention system
- Storage tiering logic
- Engine config
- Log system
- n8n routing layer [FUTURE]
- Database (shared schema, separate records)
- %SFV_ROOT% path system

## ADDING A NEW BRANCH AT SCALE
1. Copy branch template folder structure
2. Configure branch rules file
3. Add to ENVIRONMENT_CONFIG
4. Add to n8n routing [FUTURE]
5. Deploy — no other branches affected

## REPOST ECOSYSTEM
Branches support each other through reposts.
Independence does not mean isolation.
```
GROUP A — Creative/Talent: ARCHIVE + 404 + ATHLETICS
GROUP B — Service:         STUDIO + UGC + EVENTS
GROUP C — Lifestyle:       WORLD + abbass
GROUP D — Hub:             abbass (all groups feed this)
```

## CONNECTED FILES
- [[COMPRESSED_CONTEXT|Compressed Context]]
- [[02_BRANCHES/SFV_UGC|SFV_UGC]]
