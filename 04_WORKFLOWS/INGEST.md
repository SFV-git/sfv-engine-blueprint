---
STATUS: UNCONFIRMED
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# INGEST WORKFLOW

## PURPOSE
Move files from SD card into the Engine cleanly and safely.
No file is ever lost. Every file is verified.

## TRIGGER
SD card inserted OR portable SSD connected to Engine.

## FLOW
```
SD card detected
→ auto-folder created: INGEST_[YYYYMMDD]_[BRANCH]_PENDING
→ files copied (not moved) to INGEST staging
→ checksum hash generated for every file
→ duplicate check against existing library
→ duplicates flagged, not deleted
→ files renamed per naming convention
→ EXIF metadata extracted
→ branch tagged (auto or FOR HUMAN REVIEW)
→ moved to [BRANCH]/INGEST/
→ ingest log written
→ Will notified (method TBD)
```

## FAILURE BEHAVIOR
- Failed copy → file stays on SD card, flagged in error log
- Duplicate found → flagged for review, not deleted
- Unknown branch → goes to FOR HUMAN REVIEW folder
- Checksum mismatch → file quarantined, error log entry

## LOG OUTPUT
```
INGEST_LOG_[YYYYMMDD].txt
- files copied: X
- files failed: X
- duplicates found: X
- branch assignments: list
- errors: list
```

## MORNING WALK SPECIAL CASE — MAY 28
Two SD cards:
1. Studio portraits (consistent lighting) → SFV_STUDIO branch
2. Flashmob video/photo → SFV_EVENTS branch
Plus Google Drive from other shooters → manual intake

## TOOLS NEEDED [UNCONFIRMED]
- Python script: primary ingest logic
- FFmpeg: video file verification
- ExifTool: metadata extraction
