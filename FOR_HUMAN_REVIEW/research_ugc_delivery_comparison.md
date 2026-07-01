# Client-Delivery Platform Comparison — UGC Creative Agency

**Purpose:** Compare options for delivering finished video/photo assets to paying clients.
**Scope:** Dedicated client-portal tools (Frame.io, Dropbox), plain Google Drive, and Pixieset.
**Date compiled:** 2026-07-01
**Note:** This is decision-support research. **No winner is picked** — tradeoffs are presented for Will to decide. Pricing changes frequently; verify current numbers on each vendor's page before committing.

---

## Quick comparison table

| Criteria | **Frame.io** (Adobe) | **Dropbox** | **Google Drive** | **Pixieset** |
|---|---|---|---|---|
| **Category** | Purpose-built creative review/delivery | General cloud storage + file requests | General cloud storage | Photographer/creative client-gallery delivery |
| **Entry price** | Free (2 members, 2 projects, ~2GB); Pro $15/member/mo (2TB); Team $25/member/mo (3TB) | Free 2GB; Plus ~$9.99/mo (2TB, 1 user); Business plans from ~$9.99–$15+/user/mo (annual, 3+ users) | Free 15GB (shared across Google account); Google One / Workspace paid tiers add storage | Free (3GB, 15% sale commission); Basic $10/mo (10GB); Plus $20/mo (100GB); Pro $50/mo (1TB) |
| **Video-oriented?** | Yes — built for video review | Storage only (previews, no review layer) | Storage only (basic in-browser preview) | Yes on paid plans (video upload minutes: Basic 30min, Plus 1hr, Pro 2hr) |
| **Client access — account required?** | **No** — Share links let anyone view without signing up/logging in | Shared links / File Requests work **without** a recipient account; a true "portal" experience is not native | **No** for public/link-shared files; download without login if set to "Anyone with link" | **No** — clients open gallery via link; can download whole gallery or single photos without an account |
| **Revision / approval workflow** | Strong — time-stamped comments, threaded replies, frame-accurate annotations, in-app approvals | None native — no built-in review/approval; would need add-on tooling | None native — comments exist on Docs, not a media approval flow | Proofing via **Favorites** lists (clients mark/select, add notes, limits per list); geared to photo selection, not video markup/approval |
| **API for automation?** | **Yes** — V4 REST API + webhooks + Custom Actions (beta); OAuth 2.0 via Adobe IMS / Adobe Developer Console | **Yes** — mature public Dropbox API (files, sharing, file requests) | **Yes** — Google Drive API (sharing, upload, download); API key works for public files, OAuth for private | **No public/native API**; **not** on Zapier natively — automation only via workarounds (e.g. Google Sheets bridge + Make/Zapier) or Lightroom plugin |
| **Branding** | Custom-branded shares on Pro+ | Limited on standard; more on higher business tiers | Minimal / none (Google-branded UI) | Custom branding + remove Pixieset branding on paid plans |
| **Best-fit signal** | Video review + client sign-off is central | You already live in Dropbox; simple hand-off | Cheapest/simplest; you/clients already use Google | Polished photo galleries + light proofing + optional selling |

---

## Tradeoffs by platform

### Frame.io (Adobe)
- **Strengths:** The only option here built specifically for *creative review*. Frame-accurate comments, annotations, and approvals are native — ideal if client sign-off on video is a real step in your workflow. Share links require **no client account**. Full **V4 REST API + webhooks + Custom Actions** make it the most automation-friendly for programmatic pipelines (push to storage, trigger renders, notify on status change).
- **Weaknesses:** Per-seat pricing adds up as the team grows; reviewers note storage caps feel tight on lower tiers. API auth runs through **Adobe IMS / Adobe Developer Console** and requires a provisioned V4 account — more setup friction than a plain API key, and third-party connectors (Make/n8n) have hit OAuth hurdles.
- **UGC angle:** Great when deliverables are video and the client actually leaves feedback/approval. Overkill if you just need a download link.

### Dropbox
- **Strengths:** Familiar, reliable storage. Shared links and **File Requests** work for recipients **without a Dropbox account**. Mature, well-documented **public API** for automation. Good if your team already stores everything in Dropbox.
- **Weaknesses:** **No native client-portal or review/approval layer** — sources note there's no seamless portal inside Dropbox and DIY setups are "cumbersome." File Request is a single upload box, not a structured delivery/approval space. Storage counts uploads against your quota. Delivering a *branded, professional* client experience needs third-party layers (Foyer, Softr, etc.).
- **UGC angle:** Fine as a plumbing/handoff layer; weak as a client-facing delivery + approval experience on its own.

### Google Drive
- **Strengths:** Cheapest path (15GB free, then Google One/Workspace). Clients can open/download **without an account** when links are set to "Anyone with the link." Robust **Drive API** (API key for public files, OAuth for private) for automation. Nearly everyone already has Google access.
- **Weaknesses:** **No review/approval/proofing workflow** for media. Unbranded, generic UI — least "premium" client experience. Public-link sharing and direct-download URLs have quirks (short-lived download URLs; owner-only download edge cases) that complicate automated hand-off. Sharing settings are easy to misconfigure.
- **UGC angle:** Best when you want dirt-simple, low-cost delivery and don't need feedback/approval or branding.

### Pixieset
- **Strengths:** Purpose-built **client galleries** with a polished, branded, client-facing experience. Clients access via link **without an account** and can download full gallery or single files. **Proofing via Favorites** lets clients select/mark images (with notes and per-list limits) — a lightweight approval flow. Generous free tier; paid tiers add video minutes, custom branding, commission-free sales/store.
- **Weaknesses:** Photo-centric; video is supported but capped by upload-minute limits per tier (Basic 30min → Pro 2hr). Proofing is *selection*-oriented, **not** frame-accurate video markup/approval. Biggest gap for automation: **no public/native API and no native Zapier app** — integrations rely on workarounds (Google Sheets + Make/Zapier) or the Lightroom plugin. Free tier takes a 15% sale commission.
- **UGC angle:** Strong for polished photo delivery and light proofing/selling; weaker for video-heavy review and for any automated/programmatic pipeline.

---

## Things to weigh for a UGC agency specifically
- **Video vs photo mix:** Heavier video review favors Frame.io; polished photo galleries favor Pixieset; simple mixed hand-off favors Drive/Dropbox.
- **Do clients actually approve/comment, or just download?** Real approval loops → Frame.io (video) or Pixieset Favorites (photo selection). Pure download → Drive/Dropbox are cheaper.
- **Automation ambitions (n8n/Make/Zapier pipelines):** Frame.io, Dropbox, and Google Drive all have real APIs. **Pixieset does not** — that's a hard constraint if programmatic delivery matters.
- **Client experience / branding:** Pixieset and Frame.io feel premium/branded; Drive feels generic; Dropbox is in-between.
- **Cost scaling:** Frame.io and Dropbox Business scale *per seat*; Pixieset and Google scale on *storage/features*. Model this against team size and asset volume.

---

## Sources
- Frame.io pricing (G2): https://www.g2.com/products/frame-io/pricing
- Frame.io pricing (official): https://frame.io/pricing
- Frame.io pricing analysis (xpay): https://www.xpay.sh/saas-pricing/frame-io/
- Frame.io pricing/alternatives (playpause): https://playpause.io/blogs/frame-io-pricing
- Frame.io Developer / V4 API docs (Adobe): https://developer.adobe.com/frameio
- Frame.io V4 API Getting Started: https://developer.adobe.com/frameio/guides/
- Frame.io ecosystem & integrations (blog): https://blog.frame.io/2025/06/03/frame-io-ecosystem-and-integrations-powering-creative-workflows-across-apis/
- Frame.io V4 Public API (Postman): https://www.postman.com/adobe/frame-io-v4-public-api/overview
- Frame.io + S2S automation (Adobe enterprise): https://helpx.adobe.com/enterprise/using/automate-using-frame-io.html
- Pixieset Client Gallery pricing: https://pixieset.com/pricing/
- Pixieset Client Gallery (features): https://pixieset.com/client-gallery/
- Pixieset pricing/alternatives 2026 (Picflow): https://picflow.com/compare/client-gallery/pixieset
- Pixieset proofing with Favorites (Help Center): https://help.pixieset.com/hc/en-us/articles/115003733131-How-does-proofing-with-Favorites-work
- Pixieset Zapier integrations (status): https://zapier.com/apps/pixieset/integrations
- Pixieset + Zapier connection guide (Snappr): https://www.snappr.com/workflows/connect/pixieset/zapier
- Dropbox review/pricing 2026 (Cloudwards): https://www.cloudwards.net/review/dropbox/
- Dropbox client portal features (Foyer): https://usefoyer.com/blog/dropbox-client-portal
- Dropbox file request review (Clustdoc): https://clustdoc.com/blog/dropbox-file-request/
- Dropbox File Request vs File Request Pro (FileRequestPro): https://filerequestpro.com/articles/dropbox-file-request-vs-file-request-pro
- Google Drive — manage sharing (Google for Developers): https://developers.google.com/drive/api/guides/manage-sharing
- Google Drive public access without auth via API (Medium): https://medium.com/@patrabiswajit133/use-google-drive-public-folder-without-authentication-using-api-8ea71ad90dcd
- Accessing public Google Drive files via API without login (Latenode community): https://community.latenode.com/t/accessing-public-google-drive-files-via-api-without-login/32858

_Compiled from web search on 2026-07-01. Verify live pricing/feature details on vendor pages before deciding._
