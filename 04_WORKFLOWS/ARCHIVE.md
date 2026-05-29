---
STATUS: UNCONFIRMED
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# ARCHIVE WORKFLOW

## PURPOSE
Move completed content from ACTIVE to WARM to COLD storage safely.
Nothing gets deleted. Everything gets indexed.

## ARCHIVE TIERS

```
ACTIVE_STORAGE (5TB Seagate)
→ WARM: recently completed projects
→ COLD: Porsche SSD 4TB [BLOCKED — fix file system first]
→ Cloud backup: overflow video storage
```

## FLOW
```
Project delivered
→ wait [X days — TBD]
→ auto-flag for archive review
→ Will confirms archive-ready
→ move to WARM tier
→ after [X months — TBD]
→ move to COLD tier (Porsche SSD)
→ archive index updated
→ archive log written
```

## SFV_ARCHIVE BRANCH SPECIFICALLY
Content in SFV_ARCHIVE branch = best work, not cold storage.
These files stay accessible for ongoing posting.
Cold storage = raw files and project files no longer needed actively.

## PENDING
- [ ] Fix Porsche SSD file system issue
- [ ] Define archive timing thresholds
- [ ] Design archive index structure

## CONNECTED FILES
- [[STORAGE_ARCHITECTURE|Storage Architecture]]
- [[METADATA_SYSTEM|Metadata System]]
- [[DELIVERY|Delivery]]
