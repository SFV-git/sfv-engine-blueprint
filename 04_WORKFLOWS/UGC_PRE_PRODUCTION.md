---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
BRANCH: SFV_UGC
---

# UGC PRE-PRODUCTION MANAGER

> Purpose: Generate a script and shot list before every UGC shoot.
> No more scrambling in post. Everything decided before the shoot day.

---

## WHAT THIS SYSTEM DOES

Will (or a client) fills out a shoot intake. The system pulls from stored databases
(locations, clients, gear) and generates two PDFs:
1. Shot List — every shot planned, sequence, notes
2. Script — talking points, hooks, CTAs, tone per deliverable

---

## CORE ENTITIES

### 1. SHOOT
- Shoot ID (auto-generated)
- Date
- Shooter (Will for now — built to support multiple)
- Brand / Client (linked to Client DB)
- Location (linked to Location DB)
- Gear Loadout (linked to Gear DB)
- Status: PLANNED / CONFIRMED / COMPLETED
- Intake: linked intake form or filled by Will

### 2. LOCATION DATABASE
- Location ID
- Name
- Address
- Type (indoor / outdoor / studio / public / private)
- Permit required: YES / NO
- Parking notes
- Lighting conditions (natural / controlled / mixed)
- Tags (e.g. urban, minimal, luxury, raw)
- Notes (freeform)

### 3. CLIENT / BRAND DATABASE
- Client ID
- Brand name
- Contact name + email + phone
- IG handle(s)
- Brand tone (e.g. raw, aspirational, minimal, hype)
- Product category
- Deliverables typically needed (Reels, Stories, stills, etc.)
- Past shoot IDs (linked)
- Brief history / notes

### 4. GEAR DATABASE
- Item ID
- Item name
- Category: camera / lens / lighting / audio / stabilizer / accessory
- Assigned node: Engine Body / R&D Terminal / field kit
- Status: AVAILABLE / IN USE / NEEDS SERVICE
- Notes

### 5. INTAKE FORM
Fields:
- Brand / Client (dropdown from Client DB)
- Shoot date
- Location (dropdown from Location DB)
- Shooter (dropdown — Will only for now)
- Deliverables needed (multi-select: Reels, Stories, stills, BTS)
- Number of looks / outfits
- Key products or services to feature
- Tone / vibe (freeform or dropdown from brand profile)
- Hooks (3 options minimum — what grabs attention in first 2 seconds)
- Talking points (bullet list)
- CTA (what the viewer does at the end)
- References (links or descriptions)
- Special requirements (freeform)

Intake can be:
- Filled by Will directly in the app
- Sent as a shareable link for the client to fill out

---

## OUTPUTS

### Shot List PDF
- Header: Brand, Date, Shooter, Location
- Table: Shot #, Description, Angle, Lens/focal length, Lighting setup, Duration estimate, Notes
- Gear loadout section at bottom
- Generated from intake + gear DB

### Script PDF
- Header: Brand, Date, Deliverable type
- Per deliverable:
  - Hook (first 2 seconds)
  - Body (talking points in sequence)
  - CTA
  - Tone notes
- One page per deliverable where possible

---

## STACK + TECH

- Frontend: React web app (single file, runs locally or hosted)
- Storage: JSON flat files in vault (one per entity type) — no external DB for v1
- PDF generation: client-side (jsPDF or react-pdf)
- File locations:
  - App: C:\SFV_BLUEPRINT\06_APPS\ugc_preproduction\
  - Data: C:\SFV_BLUEPRINT\06_APPS\ugc_preproduction\data\
    - locations.json
    - clients.json
    - gear.json
    - shoots.json
  - Outputs: D:\SFV_UGC\PRE_PRODUCTION\ (per shoot subfolder)

---

## SCALING NOTES (FOR HUMAN REVIEW)
- Multi-shooter: add shooter DB, assign per shoot, shooter sees their own schedule only
- Client portal: shareable intake link per shoot (not per client account — no auth for v1)
- n8n integration: on intake submit → trigger n8n to notify shooter + log to queue
- AI assist: Ollama generates hook options and script draft from intake fields (future)

---

## BUILD ORDER (for Claude Code)
1. Scaffold React app with routing: Dashboard / New Shoot / Databases / Outputs
2. Build JSON data layer (CRUD for locations, clients, gear)
3. Build intake form (pulls from data layer dropdowns)
4. Build shot list generator (intake + gear → structured data)
5. Build script generator (intake → per-deliverable script structure)
6. Build PDF export for both outputs
7. Wire output save path to D:\SFV_UGC\PRE_PRODUCTION\{shoot_id}\

---

## CONNECTED FILES
- [[04_WORKFLOWS/INGEST.md]]
- [[04_WORKFLOWS/DELIVERY.md]]
- [[03_INFRASTRUCTURE/MULTI_AGENT_WORKFLOW.md]]
- [[05_AI_LAYER/AI_USE_CASE_PROFILE.md]]
