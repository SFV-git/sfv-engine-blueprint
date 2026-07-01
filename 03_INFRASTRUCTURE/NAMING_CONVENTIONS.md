---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# NAMING CONVENTIONS

Universal naming rules for all SFV Engine files and folders.
No exceptions. No creative naming. No final_final_v2 files.

---

## CORE PRINCIPLES
- Dates always YYYYMMDD format
- Branch prefix always first
- Sequence numbers always 4 digits (0001, 0047, 0150)
- Status always last
- No spaces — use underscores
- All caps for structural labels, mixed for client/event names

---

## NAMING TEMPLATES

### RAW files (off SD card)
```
[BRANCH]_[YYYYMMDD]_[EVENT/CLIENT]_[####]_RAW
STUDIO_20250528_MORNINGWALK_0001_RAW
LIVE_20250606_SHAMAR_0047_RAW
EVENTS_20250528_MORNINGWALK_0012_RAW
```

### Selects (post-cull)
```
[BRANCH]_[YYYYMMDD]_[EVENT/CLIENT]_[####]_SELECT
STUDIO_20250528_MORNINGWALK_0001_SELECT
```

### Photo exports
```
[BRANCH]_[YYYYMMDD]_[EVENT/CLIENT]_[SPEC]_[####]
STUDIO_20250528_MORNINGWALK_FULLRES_0001
STUDIO_20250528_MORNINGWALK_1080SQ_0001
LIVE_20250606_SHAMAR_1080SQ_0023
```

### Reels / Video files
```
[BRANCH]_[YYYYMMDD]_[CLIENT]_REEL_[###]_[STATUS]
UGC_20250601_PROEDGE_REEL_001_DRAFT
UGC_20250601_PROEDGE_REEL_001_APPROVED
UGC_20250601_PROEDGE_REEL_002_REJECTED
```

### Client deliverables
```
[CLIENT_ID]_[YYYYMMDD]_[DELIVERABLE]_v[##]
PROEDGE_20250601_REEL_v01
PROEDGE_20250601_REEL_v02
BELLOTTI_20250528_REEL_v01
```

### Project folders
```
[YYYYMMDD]_[EVENT/CLIENT]/
20250528_MORNINGWALK/
20250606_SHAMAR/
20250601_PROEDGE/
```

### Ingest pending (unprocessed)
```
INGEST_[YYYYMMDD]_[BRANCH]_[####]_PENDING
INGEST_20250528_STUDIO_0001_PENDING
```

### Archive files
```
[BRANCH]_[YYYYMMDD]_[PROJECT]_[####]_ARCHIVE
ARCHIVE_20250528_MORNINGWALK_0001_ARCHIVE
```

### Log files
```
[WORKFLOW]_LOG_[YYYYMMDD].txt
INGEST_LOG_20250528.txt
EXPORT_LOG_20250528.txt
SYNC_LOG_20250528.txt
ERROR_LOG_20250528.txt
CULL_LOG_20250528.txt
```

### Config files
```
[BRANCH/TOOL]_CONFIG.env
STUDIO_CONFIG.env
N8N_CONFIG.env
OLLAMA_CONFIG.env
```

---

## CAPTION SYSTEM (Instagram)

```
[SFV LIVE|01]
[SFV EVENTS|01]
[SFV STUDIO|01]
[SFV ARCHIVE|01]
[SFV ATHLETICS|01]
[SFV UGC|01]
[SFV WORLD|01]
[SFV 404|01]
```

Sequential per branch. Consistent across all posts. Never skip numbers.

---

## WHAT TO AVOID
- final_v2.jpg
- newedit.mp4
- IMG_4829.jpg (camera defaults — rename on ingest)
- Copy of Copy of...
- Random dump folder names
- Spaces in filenames

## CONNECTED FILES
- [[04_WORKFLOWS/EXPORT|Export]]
- [[12_DATABANKS/CLIENT_BANKS|Client Banks]]
- [[02_BRANCHES/SFV_ARCHIVE|SFV Archive]]
- [[06_TOOLS/TOOL_STACK|Tool Stack]]
