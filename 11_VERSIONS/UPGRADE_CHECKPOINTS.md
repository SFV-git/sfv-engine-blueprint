---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# UPGRADE CHECKPOINTS

Records when hardware, storage, and infrastructure upgrades
become necessary. Check these as the Engine scales.

---

## RAM: 32GB → 64GB
Trigger: multiple parallel Claude Code sessions + local models simultaneously
Status: planned, not yet purchased
Watch for: slowdowns during parallel processing

## INTERNAL NVMe EXPANSION
Trigger: Engine intelligence folder exceeds 1TB
Status: monitor
Watch for: vault + scripts + configs approaching 80% of NVMe

## ACTIVE STORAGE EXPANSION
Trigger: 5TB Seagate SSD reaches 80% capacity
Status: monitor
Current: early days, significant headroom
Next step: audit WD EasyStore + WD Passport for additional storage

## PORSCHE SSD ACTIVATION
Trigger: fix Mac file system issue (NTFS/exFAT)
Status: blocked — fix before activating
Use: cold archive tier

## NAS / SERVER STORAGE
Trigger: multiple operators feeding Engine simultaneously
OR: 5TB Seagate + Porsche SSD both approaching capacity
Status: v8.x — only after real bottleneck
Do NOT build early.

## SECOND ENGINE NODE
Trigger: render queue consistently backing up overnight
OR: active processing competing with storage management
Status: v9.x — far future

## ELECTRICITY CEILING
Trigger: mall management questions power usage
OR: Will's payment to studio owner increases significantly
Current concern: Engine 24/7 + R&D terminal 24/7 = significant draw
Action: monitor, throttle R&D terminal during idle, consider home option if costs spike

## UPS INSTALLATION [FOR HUMAN REVIEW]
Trigger: any power instability event
Recommendation: APC Back-UPS 1500VA
Protects: overnight runs, ingest during storms, prevents corrupt files

## CONNECTED FILES
- [[SESSION_STATE|Session State]]
- [[DASHBOARD|Dashboard]]
