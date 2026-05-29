---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# STORAGE ARCHITECTURE

## PATH SYSTEM
All paths use %SFV_ROOT% environment variable.
Defined once in ENVIRONMENT_CONFIG.md.
Never hardcode drive letters anywhere.

```
%SFV_ROOT% = [current drive root — set in ENVIRONMENT_CONFIG]
```

## STORAGE TIERS

```
ACTIVE  → files currently in production
WARM    → recently completed, not yet archived
ARCHIVE → long-term cold storage
```

Files move through tiers automatically based on age and access.

## DRIVE ROLES

| Label | Drive | Size | Role |
|-------|-------|------|------|
| ENGINE_INTELLIGENCE | Internal NVMe | ~1.75TB | OS + Engine scripts + vault |
| ACTIVE_STORAGE | Seagate SSD | 5TB | All live project files |
| FIELD_INGEST | SanDisk SSD | 1TB | SD card intake on location |
| ARCHIVE_COLD | Porsche SSD | 4TB | Cold archive [BLOCKED — fix file system] |
| BACKUP_1 | Seagate Expansion | 1TB | Redundancy backup |
| AUDIT_1 | WD EasyStore | 1TB | [UNKNOWN — needs content audit] |
| AUDIT_2 | WD My Passport | UNKNOWN | [UNKNOWN — needs content audit] |

## ACTIVE STORAGE STRUCTURE

```
%SFV_ROOT%\ACTIVE_STORAGE\
├── BRANCHES\
│   ├── MYTHOLOGY\
│   ├── SFV_LIVE\
│   ├── SFV_EVENTS\
│   ├── SFV_ATHLETICS\
│   ├── SFV_STUDIO\
│   ├── SFV_UGC\
│   ├── SFV_ARCHIVE\
│   ├── SFV_WORLD\
│   └── SFV_404\
├── INGEST_STAGING\
├── EXPORTS\
└── DELIVERY\
```

## PER-BRANCH FOLDER STRUCTURE

```
[BRANCH]\
├── INGEST\         ← files land here from SD card
├── RAW\            ← verified originals
├── SELECTS\        ← post-cull approved files
├── EXPORTS\        ← finished deliverables
├── DELIVERY\       ← client-ready packages
├── ARCHIVE\        ← moved to cold after delivery
├── LOGS\           ← per-branch workflow logs
└── CONFIG\         ← branch-specific settings
```

## REDUNDANCY

```
SD card
→ FIELD_INGEST (SanDisk SSD) — immediate backup on location
→ Engine ACTIVE_STORAGE — primary home
→ BACKUP_1 (Seagate Expansion) — redundancy
→ Cloud (Google Drive / iCloud) — overflow video storage
No single point of failure.
```

## CLOUD USAGE
Google Drive and iCloud: overflow and video storage only.
Internal folder structure stays internal.
Proxies can be stored in cloud. Originals stay on Engine.

## PENDING TASKS
- [ ] Audit WD EasyStore contents
- [ ] Audit WD My Passport contents and size
- [ ] Fix Porsche SSD file system issue (Mac compatibility)
- [ ] Confirm %SFV_ROOT% permanent location

## CONNECTED FILES
- [[ENVIRONMENT_CONFIG|Environment Config]]
- [[NAMING_CONVENTIONS|Naming Conventions]]
- [[BRANCH_OUTPUTS|Branch Outputs]]
- [[INGEST|Ingest]]
- [[EXPORT|Export]]
- [[ARCHIVE|Archive]]
- [[CULLING|Culling]]
- [[PENDING_REVIEW|Pending Review]]
