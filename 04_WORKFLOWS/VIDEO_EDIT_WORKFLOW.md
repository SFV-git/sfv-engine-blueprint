---
STATUS: FOR HUMAN REVIEW
VERSION: v2.0.0
OWNER: WILL
LAST_UPDATED: 2026-07-01
REWRITTEN_BY: Claude Chat (autonomous, web-researched)
SUPERSEDES: v1 (scored 1.5/5 by Perplexity — hallucinated Premiere features: Content-Aware Fill,
  Keylight, "Audio Sync Tool", Preferences>Export path — all removed and corrected)
---

# VIDEO EDIT WORKFLOW

Pipeline picks up AFTER footage is ingested to the branch folder (see [[INGEST|Ingest Workflow]]).
Covers reel assembly for short-form vertical delivery (Instagram Reels, TikTok, Shorts).
All tool references verified against Adobe Premiere Pro 2026 documentation 2026-07-01.

## 0. SCOPE + SEQUENCE SETTINGS
- Delivery target: 9:16 vertical, 1080x1920, H.264 for social. Confirm per-branch.
- Frame rate: match source (typically 24 or 30fps for UGC; 60fps if shot for slow-mo). [FOR HUMAN REVIEW — confirm Will's capture fps per branch]
- Color space: Rec.709 for standard delivery. Log footage (S-Log3, C-Log) requires a LUT or Lumetri color-managed workflow before grading.
- Import via **Media Browser panel**, NOT drag-and-drop from Explorer — Media Browser preserves timecode, camera metadata, and reel names needed for multicam relink.

## 1. PROJECT + BIN STRUCTURE
- One .prproj per shoot/client, stored in the branch folder tree (maps to D:\ branch structure).
- Bins: `01_RAW`, `02_SELECTS`, `03_AUDIO`, `04_GRAPHICS`, `05_EXPORTS`.
- Proxies: generate via Premiere ingest proxy option (1/2 or 1/4 res) if source is 4K+ or high-bitrate (BRAW/HEVC). Store proxies in a sibling `PROXY` folder.

## 2. MULTICAM SYNC (live events, multi-angle UGC)
- Select camera clips → right-click → **Create Multi-Camera Source Sequence**.
- Sync method: **audio waveform** (default for run-and-gun, no shared timecode) or **timecode** (if jam-synced).
- Cam filename prefixes (Cam1_, Cam2_, Cam3_) prevent stream collision — matches the locked EVENTS convention.
- Fake multicam from single 4K talking head: drop clip on 3 tracks, crop wide/medium/close, nest, enable multicam.

## 3. ASSEMBLY — PANCAKE TIMELINE METHOD
This is the core reel-assembly technique. Verified fastest workflow for large footage volume:
1. Top sequence = selects/stringout (all usable takes in order).
2. Bottom sequence = master edit (the reel being built).
3. Drag the stringout tab upward to split the panel — both visible at once.
4. Set In/Out on the stringout, use Insert (,) or Overwrite (.) to drop selections into the master below.
5. Eliminates Source Monitor round-trips — significantly faster assembly.

Pacing targets per deliverable (proposed defaults — [FOR HUMAN REVIEW]):
- Reel/TikTok hook: cut within first 1.5s, clip lengths 0.8–2.5s for retention.
- Total duration: 15–30s for max reach, up to 60s for tutorial/story content.

## 4. VERTICAL REFRAME (horizontal source → 9:16)
- Select master sequence → **Sequence > Auto Reframe Sequence** → target 9:16.
- Premiere AI-tracks the primary subject and repositions frame.
- REVIEW manually: multi-subject shots and fast motion often need keyframe correction. Auto Reframe is a starting point, not final.

## 5. GREEN SCREEN (if used — ATHLETICS stat overlays, etc.)
- Chroma key tool is **Ultra Key** (Effects > Keying > Ultra Key). This is Premiere's native keyer.
- NOTE: Keylight is an After Effects plugin, NOT available in Premiere. For heavy compositing, round-trip to AE via Dynamic Link (Replace With After Effects Composition).
- Sports stat overlays: use Motion Graphics Templates (.mogrt) from Essential Graphics panel, or Dynamic Link to AE — NOT green screen.

## 6. AUDIO
- Treat as a distinct stage, not an afterthought.
- Sync method depends on capture: dual-system (separate recorder) → Merge Clips with audio waveform sync; on-camera audio only → no sync step.
- Music: pull from licensed library (see §9 licensing). Duck music under VO using the Essential Sound panel (assign clip as Dialogue vs Music, enable Auto-Ducking).
- Loudness: social platforms normalize to roughly -14 LUFS integrated. True peak ceiling -1 dBTP to avoid clipping on playback. Apply Loudness Radar (Audio Effects > Special) to master track to verify.

## 7. COLOR
- Lumetri Color panel. Apply branch LUT first, then adjust exposure/white balance/saturation.
- Brand LUT: [FOR HUMAN REVIEW — Will's actual per-branch LUT files are the missing deliverable here. Placeholder "Brand_LUT_v1" is not a real file yet.]
- If Log source: set input LUT in Lumetri > Basic Correction before creative grade.

## 8. CAPTIONS
- Auto-transcribe: Text panel > Transcribe Sequence (Premiere's built-in speech-to-text, free with subscription).
- Style captions via Essential Graphics. Keep high-contrast, safe-zone aware (not under IG/TikTok UI overlays — bottom ~15% and top ~10% are unsafe).
- Export burned-in for social (platforms don't reliably read sidecar .srt on reels).

## 9. LICENSING (critical for SaaS resale — see note)
- Music must be cleared for commercial + client use. Epidemic Sound / Artlist / Musicbed offer creator+client licensing. Free/YouTube Audio Library often does NOT cover paid-ad usage.
- Fonts: confirm commercial license for any non-system font baked into deliverables.
- LUTs/plugins: verify redistribution rights before bundling into any resold product.
- **If this workflow is ever packaged as sellable software: DO NOT bundle Adobe-dependent steps as a product feature.** The defensible layer is the decision layer (shot list → timeline markers, caption/music selection). Final render hands off to the shooter's own Premiere/CapCut. See [[SAAS_CONVERSION_PLAN|SaaS Conversion Plan]].

## 10. EXPORT
Verified specs by destination:

| Destination | Resolution | Aspect | Codec | Notes |
|---|---|---|---|---|
| IG Reel / TikTok / Shorts | 1080x1920 | 9:16 | H.264, ~10–15 Mbps | Burned-in captions |
| IG Feed | 1080x1350 | 4:5 | H.264 | |
| Client full-res delivery | source res | source | H.264 high bitrate or ProResHQ (.MOV) | ProRes stays in MOV container, NOT MP4 |
| Archive master | source res | source | ProRes 422 HQ or 4444 (.MOV) | See [[ARCHIVE|Archive Workflow]] |

- Export presets are saved in the **Export dialog / Media Encoder preset browser** — NOT in Preferences (v1 stated a path that doesn't exist).
- Version control: Git + Syncthing on the vault (NOT Adobe Team Projects — that's a cloud team-collab product, irrelevant for solo).

## CONNECTED FILES
- [[INGEST|Ingest Workflow]]
- [[ARCHIVE|Archive Workflow]]
- [[UGC_DELIVERY|UGC Delivery]]
- [[EXPORT|Export Workflow]]
- [[SAAS_CONVERSION_PLAN|SaaS Conversion Plan]]
