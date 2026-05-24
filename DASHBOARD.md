---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# SFV ENGINE — DASHBOARD

> Open this every session. It tells you what needs you.

---

## NEEDS YOUR ATTENTION

```dataview
LIST
FROM "FOR_HUMAN_REVIEW"
WHERE status != "REJECTED"
```

## UNCONFIRMED ITEMS

```dataview
LIST
FROM ""
WHERE status = "UNCONFIRMED"
```

## OPEN QUESTIONS

```dataview
LIST
FROM "00_DEV_LOG"
WHERE file.name = "QUESTIONS_FOR_WILL"
```

## RECENT CHANGES

```dataview
TABLE file.mtime AS "Last Modified"
SORT file.mtime DESC
LIMIT 10
```

## NEXT MILESTONES
- [ ] Morning Walk stress test — May 28 2025
- [ ] Shamar Tournament — June 6 2025
- [ ] Brandon Bellotti shoot — this week
- [ ] ProEdge / Will Wilver outreach — this week

## CURRENT BUILD PHASE
v0.x — Blueprint Foundation
