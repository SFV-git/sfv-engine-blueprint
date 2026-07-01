---
STATUS: UNCONFIRMED
VERSION: v0.2.0
OWNER: WILL
LAST_UPDATED: 2026-06-09
---

# UNCONFIRMED ITEMS

Items discussed but not yet locked by Will.
Nothing here gets built until moved to CANON.
Reconciled 2026-06-09 — resolved items moved to bottom with their resolution.

---

## ACCOUNT / BRAND
- Alias burner account details (off Engine, Will only)

## HARDWARE
- Exact motherboard model and NVMe slot count
- RAM upgrade timeline (32GB → 64GB)

## TOOLS
- Canva — REMOVED from stack 2026-05-27 (Q004) — graphics tool for Level 6+ still TBD if needed
- n8n — ACTIVE since 2026-05-29; remaining: PostgreSQL migration, queue mode timing

## WORKFLOWS
- abbass catch logic (auto-detected or manually flagged?)
- Exact cross-branch rules (human review confirmed, exact rules TBD)
- Caption voice per branch
- Hashtag strategy per branch

## TECHNICAL
- Supabase schema design
- Databank initial seeding content
- Video export specs per branch
- Photo export specs per branch
- Whisper port + endpoint on Node B (blocks MEDIA pipeline build)

## INFRASTRUCTURE
- WD EasyStore contents (needs audit)
- WD My Passport contents and size (needs audit)
- 4TB Porsche SSD file system fix timeline
- Syncthing version history enabled on Node B? (affects DISASTER_RECOVERY rollback Option B)
- GitHub remote for vault confirmed pushing? (DR assumes it — verify `git remote -v` + last push)

## SCALING
- Exact Halifax office timeline
- Company car timeline
- First Maritime city target after Halifax

---

## RESOLVED (moved 2026-06-09 — decisions logged in QUESTIONS_FOR_WILL / SESSION_STATE / PROPOSALS)
- ~~SFV_UGC final name~~ → stays SFV_UGC internally (2026-05-26)
- ~~SFV_404 platform~~ → own IG account (2026-05-27)
- ~~Three monitor setup~~ → 3 on Engine Body, 2 on R&D Terminal (2026-05-27)
- ~~Scheduling tool~~ → Later (2026-05-26)
- ~~Remote access~~ → Tailscale approved + installed (2026-05-26)
- ~~Docker yes/no~~ → approved; install pending restart (2026-05-26)
- ~~Whisper local vs API~~ → local on R&D Terminal (2026-05-27)
- ~~SFV_EVENTS delivery method~~ → Pixieset standard; Zenfolio Sports & Events (QR workflow) for multi-day events

## CONNECTED FILES
- [[HARDWARE_CONTEXT|Hardware Context]]
- [[STORAGE_ARCHITECTURE|Storage Architecture Audit]]
- [[DATABANK_ARCHITECTURE|Databank Architecture]]
- [[NATIONWIDE|Nationwide Expansion Timeline]]
- [[BRAND_BANKS|Brand Banks]]
