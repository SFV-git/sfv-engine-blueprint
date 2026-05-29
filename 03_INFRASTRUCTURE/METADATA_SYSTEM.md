---
STATUS: UNCONFIRMED
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# METADATA SYSTEM

## PURPOSE
Every file in the Engine carries metadata.
Metadata enables search, sorting, routing, and AI processing.

## METADATA EXTRACTED ON INGEST

### From EXIF (automatic)
- Date/time shot
- Camera model
- Lens used
- ISO, aperture, shutter speed
- GPS coordinates (if available)
- File size and format

### Added by Engine on ingest
- Branch assignment
- Event/client ID
- Shoot ID
- Ingest timestamp
- Checksum hash (for duplicate detection)
- Cull status (pending/select/reject)

## DATABASE IDs [UNCONFIRMED — Supabase schema not yet designed]
- CLIENT_ID: unique per client
- EVENT_ID: unique per event
- PERSON_ID: unique per subject (face clustering)
- ASSET_ID: unique per file
- SHOOT_ID: unique per shoot session

## METADATA STORAGE [UNCONFIRMED]
- Tool: Supabase / Postgres [approved direction, schema TBD]
- Sidecar files: XMP alongside RAWs
- Central database: Supabase instance

## FACE CLUSTERING [FUTURE]
- PERSON_ID foundations for repeat subject recognition
- Relevant for SFV_STUDIO bulk shoots (Morning Walk)
- Local model on R&D terminal handles clustering

## CONNECTED FILES
- [[ENVIRONMENT_CONFIG|Environment Config]]
- [[NAMING_CONVENTIONS|Naming Conventions]]
- [[DATABANK_ARCHITECTURE|Databank Architecture]]
- [[STORAGE_ARCHITECTURE|Storage Architecture]]
- [[INGEST|Ingest]]
- [[RD_TERMINAL_ARCHITECTURE|RD Terminal Architecture]]
- [[CLIENT_BANKS|Client Banks]]
