---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# DECISIONS LOG

Locked decisions made by Will. These are CANON.

---

## 2026-05-24

### Branch list locked
9 branches confirmed:
MYTHOLOGY, SFV_LIVE, SFV_EVENTS, SFV_ATHLETICS, SFV_STUDIO,
SFV_UGC (name pending), SFV_ARCHIVE, SFV_WORLD, SFV_404
Burner account: off Engine, Will manages privately.

### Vault structure locked
SFV_BLUEPRINT/ with 13 numbered folders + FOR_HUMAN_REVIEW + 99_INBOX

### Path system
Relative paths via %SFV_ROOT% environment variable.
Never hardcode drive letters.

### Git from day one
Every change tracked. Rollback available at all times.

### Storage direction
5TB Seagate SSD → primary active storage
Internal NVMe → OS + Engine intelligence
1TB SanDisk → field ingest

### Growth accounts
SFV_STUDIO and SFV_UGC only.
All other accounts: passion, talent display, myth-building.

### Primary money makers
SFV_UGC (content retainers) + SFV_EVENTS (on-site portraits)

### Archive feed
Both: promoted from other branches AND dedicated shoots.

### Stories
Engine handles Studio and UGC only. Rest manual.

### Cross-branch filing
FOR HUMAN REVIEW flag system during ingest.
Rules defined per branch but human makes final call on edge cases.

### Naming convention confirmed
See 03_INFRASTRUCTURE/NAMING_CONVENTIONS.md

### Repost ecosystem
All accounts support each other within logical groupings.
abbass is the hub. All branches can repost to it.

### Obsidian as blueprint brain
Vault IS the Obsidian vault. Same folder, opened in Obsidian.

### Claude Code
Used for implementation phase only, after blueprint is complete.
Not used for vault creation (Python script instead).

### R&D Terminal role
Local models 24/7. Research. Proposals only.
Never touches production directly.

## CONNECTED FILES
- [[NAMING_CONVENTIONS|Naming Conventions]]
- [[STORAGE_ARCHITECTURE|Storage Architecture]]
- [[ENVIRONMENT_CONFIG|Environment Config]]
- [[ARCHIVE|Archive]]
- [[LOCAL_MODELS|Local Models]]
- [[CLAUDE_CODE_PROMPTS|Claude Code Prompts]]
- [[PROPOSALS|Proposals]]
- [[ROADMAP|Roadmap]]
