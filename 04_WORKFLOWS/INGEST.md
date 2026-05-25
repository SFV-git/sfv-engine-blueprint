---
STATUS: CANON
VERSION: v0.2.0
OWNER: WILL
LAST_UPDATED: 2026-05-25
---

# INGEST WORKFLOW

## PURPOSE
Move files from any source into the Engine cleanly and safely.
No file is ever lost. Every file is verified before it moves.
This is the first step of every pipeline — it must be bulletproof.

## CONNECTED FILES
- [[03_INFRASTRUCTURE/NAMING_CONVENTIONS|Naming Conventions]]
- [[03_INFRASTRUCTURE/ENVIRONMENT_CONFIG|Environment Config]]
- [[04_WORKFLOWS/CULLING|Culling Workflow]]
- [[04_WORKFLOWS/EXPORT|Export Workflow]]
- [[04_WORKFLOWS/DELIVERY|Delivery Workflow]]
- [[02_BRANCHES/SFV_STUDIO|SFV_STUDIO]] — primary ingest branch (Morning Walk)
- [[02_BRANCHES/SFV_EVENTS|SFV_EVENTS]] — overlaps Studio for Morning Walk
- [[08_TESTS/PAPER_TRIAL_RUNS|Paper Trial Runs]] — May 28 stress test

---

## INGEST SOURCES (all types)

| Source | Method | Branch | Notes |
|--------|--------|--------|-------|
| SD card (Will's camera) | Python script auto-copy | Depends on shoot | Primary source |
| SanDisk Extreme SSD (E:\) | Python script auto-copy | Depends on shoot | Field ingest drive |
| Other photographer SD/drive | Manual drop to INGEST_STAGING | Depends on shoot | Requires manual branch tag |
| Google Drive (other shooters) | Manual download → INGEST_STAGING | Depends on shoot | Morning Walk scenario |
| iPhone / phone camera | Manual drop to INGEST_STAGING | MYTHOLOGY or WORLD | Will decides branch |

---

## INGEST FLOW — STANDARD

```
SOURCE MEDIA CONNECTED OR FILES DROPPED TO STAGING
    ↓
STEP 1 — COPY (not move) to INGEST_STAGING on D:\
    Target: D:\SFV_ACTIVE\INGEST_STAGING\[YYYYMMDD]_[BRANCH]_PENDING\
    Copy all files. Never delete from source until verified.
    ↓
STEP 2 — VERIFY
    Checksum hash (MD5) generated for every file
    Checksums compared: source vs destination
    Any mismatch → file flagged, quarantined, error log entry
    Source card stays intact until Will manually confirms OK
    ↓
STEP 3 — BRANCH TAG
    Auto-detect from folder structure or filename if possible
    Unknown branch → goes to D:\SFV_ACTIVE\FOR_HUMAN_REVIEW\
    Will assigns branch → script continues
    ↓
STEP 4 — RENAME
    Apply naming convention from NAMING_CONVENTIONS.md
    Format: [BRANCH]_[YYYYMMDD]_[SEQUENCE]_[OPTIONAL_TAG].[ext]
    Example: STUDIO_20260528_001_MORNINGWALK.ARW
    ↓
STEP 5 — DUPLICATE CHECK
    Compare filenames + file size + hash against existing library
    Exact duplicate → flagged, NOT deleted, log entry, skip
    Near-duplicate → flagged FOR HUMAN REVIEW, continue
    ↓
STEP 6 — MOVE TO BRANCH FOLDER
    D:\SFV_ACTIVE\BRANCHES\[BRANCH]\INGEST\[YYYYMMDD]\
    Original staging folder deleted only after verified move
    ↓
STEP 7 — LOG
    INGEST_LOG_[YYYYMMDD]_[BRANCH].txt written to branch LOGS\
    Log contains: files copied, failed, duplicates, branch assignments, errors
    ↓
STEP 8 — NOTIFY
    Terminal print: "Ingest complete — X files | Y failed | Z duplicates"
    Log path printed for Will's review
    [Future: desktop notification via Windows toast]
```

---

## MORNING WALK SPECIAL CASE — MAY 28

### Sources
| Source | Content | Branch |
|--------|---------|--------|
| Will's SD card (camera 1) | Studio portraits, 3 shots/model, ~150 RAW files | SFV_STUDIO |
| Will's SD card (camera 2) or same card | Flashmob/event coverage | SFV_EVENTS |
| Google Drive (other shooters) | BTS, group shots, candids | SFV_STUDIO or FOR_HUMAN_REVIEW |

### Critical constraints
- Same-day Pixieset delivery required
- 150+ files → ingest must be fast, no bottlenecks
- Two branches from one shoot → branch tagging is manual or pre-flagged
- Google Drive files → no auto-detection, manual download + drag to staging

### Morning Walk ingest steps (Will does these in order)
```
1. Insert SD card → INGEST_STAGING auto-populates (or drag files manually)
2. Run: python C:\SFV_BLUEPRINT\99_INBOX\ingest.py --branch STUDIO --date 20260528
3. Script runs steps 1-8 above for Studio files
4. Repeat with: --branch EVENTS for flashmob content
5. Download Google Drive folder → drag to D:\SFV_ACTIVE\INGEST_STAGING\
6. Run: python C:\SFV_BLUEPRINT\99_INBOX\ingest.py --branch STUDIO --source staging
7. Open Lightroom → point to D:\SFV_ACTIVE\BRANCHES\SFV_STUDIO\INGEST\20260528\
8. Cull, sync preset, export → see EXPORT.md
9. Upload to Pixieset → see DELIVERY.md
```

### Time budget for May 28
| Step | Time estimate |
|------|--------------|
| SD card copy + verify (~150 RAW files) | ~5-10 min |
| Rename + duplicate check | ~2 min |
| Move to branch folder | ~1 min |
| Google Drive download | ~10-15 min (depends on connection) |
| Manual review of Google Drive files | ~15 min |
| **Total ingest** | **~35-45 min** |

---

## FAILURE BEHAVIOR

| Failure | Response |
|---------|----------|
| Copy fails mid-transfer | File stays on source, flagged in error log, rest continues |
| Checksum mismatch | File quarantined to D:\SFV_ACTIVE\FOR_HUMAN_REVIEW\QUARANTINE\ |
| Unknown branch | File goes to D:\SFV_ACTIVE\FOR_HUMAN_REVIEW\ with original name |
| Duplicate found | Flagged in log, NOT deleted, Will reviews |
| Disk full on D:\ | Ingest stops, error printed, Will notified |
| Script crashes | Source files untouched (copy not move), Will re-runs |

---

## TOOLS REQUIRED

| Tool | Status | Purpose |
|------|--------|---------|
| Python | INSTALLED | ingest.py script runtime |
| hashlib (stdlib) | BUILT-IN | MD5 checksum generation |
| shutil (stdlib) | BUILT-IN | File copy operations |
| pathlib (stdlib) | BUILT-IN | Path handling |
| ExifTool | NOT YET INSTALLED | EXIF metadata extraction [FUTURE] |
| FFmpeg | APPROVED | Video file verification [FUTURE] |

### Install ExifTool (Will does once)
```
winget install exiftool
```
Not required for May 28 — metadata extraction is a future enhancement.

---

## INGEST SCRIPT SPEC
> Script to be built in Claude Code session.
> File: C:\SFV_BLUEPRINT\99_INBOX\ingest.py

### Arguments
```
python ingest.py --branch [BRANCH_NAME] --date [YYYYMMDD] --source [auto|staging|path]
```

### Defaults
- `--source auto` = looks for removable drives (D:\ excluded, E:\ included)
- `--source staging` = processes D:\SFV_ACTIVE\INGEST_STAGING\ contents
- `--date` = defaults to today if omitted
- `--branch` = required (no auto-branch-detection in v1)

### Output
```
[INGEST] Starting: STUDIO_20260528
[INGEST] Source: E:\ (SanDisk Extreme)
[INGEST] Files found: 152
[INGEST] Copying... ████████████████ 152/152
[INGEST] Verifying checksums... OK (152/152)
[INGEST] Renaming... done
[INGEST] Duplicates found: 0
[INGEST] Moving to branch folder... done
[INGEST] Log written: D:\SFV_ACTIVE\BRANCHES\SFV_STUDIO\LOGS\INGEST_LOG_20260528.txt
[INGEST] Complete. 152 files ingested. 0 failed. 0 duplicates.
```

---

## LOG FORMAT
```
INGEST LOG — SFV_STUDIO — 2026-05-28
=====================================
Source: E:\ (SanDisk Extreme SSD)
Start: 14:32:01
End:   14:37:44
Duration: 5m 43s

FILES COPIED: 152
FILES FAILED: 0
DUPLICATES: 0
CHECKSUM ERRORS: 0
BRANCH: SFV_STUDIO
DESTINATION: D:\SFV_ACTIVE\BRANCHES\SFV_STUDIO\INGEST\20260528\

ERRORS: none
```

---

## FUTURE ENHANCEMENTS (not needed for May 28)
- ExifTool: extract and tag EXIF metadata on ingest
- Auto-branch detection from EXIF GPS or camera body
- Windows toast notification on complete
- Blur/exposure pre-check via Ollama immediately post-ingest
- FFmpeg integrity check on video files
- Whisper transcription trigger for video with audio

---
*May 28 critical path: Python ingest.py script must be built before Thursday.*
*Build in Claude Code session. Reference this file as spec.*
