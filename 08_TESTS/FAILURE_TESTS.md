---
STATUS: UNCONFIRMED
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# FAILURE TESTS

What happens when things go wrong.
Every workflow needs a defined failure behavior.

---

## INGEST FAILURES
- SD card disconnects mid-copy → partial files flagged, retry from last checkpoint
- Checksum mismatch → file quarantined, error log, Will notified
- Drive full → ingest stops, error log, Will notified immediately
- Unknown branch → file goes to FOR_HUMAN_REVIEW folder

## EXPORT FAILURES
- Lightroom crashes mid-batch → log last successful export, resume from there
- Export spec wrong → flag for re-export, do not deliver
- Pixieset upload fails → retry 3x, then flag for manual upload

## DELIVERY FAILURES
- Scheduling tool fails → flag for manual post, log it
- Client notification fails → log it, Will notified

## POWER FAILURE
- Engine loses power mid-workflow → Git commit protects vault
- Checksum system protects files (incomplete copies detectable)
- Workflows designed to resume from last checkpoint

## R&D TERMINAL FAILURES
- Local model fails → task escalates to Claude API with cost warning
- R&D terminal offline → Engine continues without AI assist, flags tasks for later
