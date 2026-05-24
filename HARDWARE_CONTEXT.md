---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# HARDWARE CONTEXT

## ENGINE BODY
- CPU: Ryzen 9 9900X
- GPU: RTX 5080
- RAM: 32GB current → upgrading to 64GB
- PSU: 850W
- Internal NVMe: ~1.75TB total
- OS: Windows 11
- Network: WiFi current → Ethernet planned
- Monitors: three-screen setup planned [UNCONFIRMED — confirmed or still planned?]

## R&D TERMINAL
- GPU: RTX 3060
- RAM: 16GB
- Role: local models + research 24/7
- Status: separate node, never touches production directly
- Local models: Ollama + Qwen/Llama/DeepSeek

## STORAGE INVENTORY
| Drive | Size | Current Role | Target Role |
|-------|------|-------------|-------------|
| Internal NVMe | ~1.75TB | OS + apps | OS + Engine intelligence |
| Seagate SSD | 5TB | Portable | Primary active storage |
| SanDisk SSD | 1TB | Portable | Field ingest |
| Porsche SSD | 4TB | BLOCKED (file system issue) | Archive/secondary |
| WD EasyStore | 1TB | UNKNOWN | Pending audit |
| Seagate Expansion | 1TB | Portable | Backup/redundancy |
| WD My Passport | UNKNOWN size | UNKNOWN | Pending audit |

## ELECTRICITY CONSTRAINT
Lab is located inside mall photography studio space.
Owner doesn't use much electricity.
Power spikes may trigger rent increase from mall management.
Engine runs 24/7 — power draw must be managed.
Will pays extra monthly to cover electric costs.
R&D terminal should throttle during idle periods.

## CLOUD STORAGE (current)
- Google Drive: 200GB
- iCloud: unknown amount
- WeTransfer: used for current delivery
- Role: overflow and video storage only. Internal structure stays internal.

## PATH SYSTEM
All paths use %SFV_ROOT% environment variable.
Never hardcode drive letters.
Change one line in ENVIRONMENT_CONFIG to migrate drives.

## FUTURE BOTTLENECKS [UNCONFIRMED]
- RAM upgrade to 64GB (planned)
- NVMe expansion (when active storage fills)
- NAS (only when real bottleneck exists)
- Second Engine node (v9.x)
