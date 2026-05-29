---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# PAPER TRIAL RUNS

Walk every workflow on paper before any code runs.
If it breaks on paper it will break in production.

---

## TRIAL 01 — MORNING WALK STUDIO PIPELINE
Target date: May 28 2025
Status: NOT YET RUN

Walk-through:
```
[ ] SD card 1 (studio portraits) inserted
[ ] Ingest triggered
[ ] Files named correctly: STUDIO_20250528_MORNINGWALK_0001_RAW
[ ] Branch tagged: SFV_STUDIO
[ ] Checksum verified
[ ] Duplicates checked
[ ] Files in SFV_STUDIO/INGEST/
[ ] Lightroom Classic opens correct folder
[ ] Sync preset applied across all 150+ photos
[ ] Export batch runs: FULLRES + 1080SQ
[ ] Files in SFV_STUDIO/EXPORTS/20250528_MORNINGWALK/
[ ] Pixieset upload (manual first time)
[ ] Gallery link ready for models
[ ] Content scheduled for SFV_STUDIO IG
```

Failure points to watch:
- SD card 1 vs SD card 2 mixed up on ingest
- Other shooters' Google Drive content needs separate intake
- 150+ photos in one Lightroom sync — test export time
- Pixieset upload time for 150+ photos

---

## TRIAL 02 — SHAMAR TOURNAMENT LIVE PIPELINE
Target date: June 6 2025
Status: NOT YET RUN

Walk-through: TBD — define before June 6

---

## HOW TO RUN A PAPER TRIAL
1. Write out every step in the flow
2. Check each box manually without code running
3. Find where it would break
4. Fix the break in the blueprint
5. Re-run the paper trial
6. Only then write the code

## CONNECTED FILES
- [[04_WORKFLOWS/INGEST|Ingest Workflow]]
- [[04_WORKFLOWS/DELIVERY|Delivery Workflow]]
