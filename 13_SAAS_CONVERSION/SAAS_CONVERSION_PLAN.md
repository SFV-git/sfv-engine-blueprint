---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-06-28
TYPE: STRATEGY / VIABILITY ANALYSIS
RATIFICATION: NONE — nothing here is CANON. Will ratifies or rejects.
---

# SFV ENGINE → SaaS — CONVERSION VIABILITY PLAN

> In-depth assessment of turning the SFV Engine into a SaaS product, with focus
> on (a) managing editing/post-production at multi-tenant scale, (b) overall
> viability, (c) whether it is worth pursuing further. All findings FHR.

---

## 0. BOTTOM LINE (read this, then decide if the rest is worth your time)

**[INFERENCE / RECOMMENDATION]** Licensable, multi-tenant SaaS is **low-viability**
for SFV as currently built and currently resourced (solo operator, two local nodes).
The engine's entire advantage is *local, near-zero-marginal-cost compute on hardware
you already own*. That advantage **inverts the moment you go SaaS** — you start paying
other people's compute, storage, and bandwidth out of your margin. Post-production is
the single most compute-and-storage-heavy stage of the pipeline, so "manage editing/post
as a SaaS" is the **worst** part of the stack to put on your own P&L.

This re-confirms the conclusion the vault already reached twice (productize the *service*,
keep the engine as a private moat) — but now with fresh 2026 market data behind it.

**There is one narrow software path that is not dead** (§7). It is not "the engine as SaaS."
It is a thin, BYO-compute orchestration tool for a specific niche. Small TAM, real support
burden, distribution problem. Worth a 2-week paid-discovery probe **only** if you actually
want to be a software vendor. If you want to grow SFV, §6 Path A (productized service +
operators) dominates on every axis.

---

## 1. WHAT THE ENGINE ACTUALLY IS (grounds the whole analysis)

The SFV Engine is an **orchestration + classification + logistics** layer. Concretely it:
- watches folders / `CURRENT_DIRECTIVE.md`, routes tasks by `task_type` (n8n WF1)
- classifies/summarizes/labels via local Ollama (qwen3:14b etc.) at ~$0 marginal cost
- logs decisions, writes back status, escalates low-confidence work to a human/HANDOFFS
- moves files through ingest → branch sort → delivery (Zenfolio/Pixieset)

**What the engine does NOT do:** it does not *edit*. It does not cut video, grade, retouch,
or render. It coordinates the work *around* editing. This is the crux of your main concern —
see §4.

**Source of advantage today:** fixed cost (electricity + already-owned RTX 5080 / RTX 3060) and
**~$0 per-job marginal cost** because inference runs locally. That is the moat. It is a *cost*
moat, not a *technology* moat — nothing in the routing logic is proprietary or hard to copy.

---

## 2. THE COGS INVERSION (the central reason SaaS is hard here)

| | Internal engine (today) | Multi-tenant SaaS |
|---|---|---|
| Compute | Local Ollama, ~$0/job | You rent GPU OR you eat it on your 2 nodes |
| Storage | Your own drives (D:/E:) | You host customers' media — recurring $/GB/mo |
| Bandwidth | LAN, free | Egress billed per GB — video is huge |
| Failure domain | Your shoots only | Every customer's deadline is now your outage |
| Marginal cost/customer | n/a | **Positive and storage/egress-dominated** |

**[INFERENCE — order-of-magnitude, verify before any commitment]** A single 4K shoot is
tens-to-hundreds of GB. Object storage (~$0.02/GB/mo) + egress (~$0.05–0.09/GB) on a handful
of active video customers can **exceed a $20–40/mo subscription per seat** before you've paid
yourself a cent. SaaS video economics only work when the **customer brings their own storage
and editing** (BYO-compute), or when you have the volume to negotiate infra and a margin model
that survives it. A solo operator has neither.

**Running it on your own two nodes instead of cloud does not save you** — it makes your shoots
compete with paying strangers for the same GPU, turns one box into a single point of failure for
other people's businesses, and caps you at a few tenants. Non-starter.

---

## 3. YOUR MAIN CONCERN — "MANAGING EDITING & POST-PRODUCTION" AT SCALE

Split this into two things that get conflated. They have very different answers.

### 3a. Post-production *coordination / review / approval* (the Frame.io layer)
This is: ingest the cut, route it to a reviewer/client, collect frame-accurate notes, version,
approve, deliver. **This is a saturated, mature market in 2026.** Direct incumbents found:
Frame.io, Wipster, KROCK, Ziflow, Filestage, PageProof, Timeliner, Dropbox Replay, Vimeo
Review, SyncSketch, plus DAM/asset layers (Air, Iconik, Tagbox). Most have free tiers,
unlimited-reviewer plans, and native Premiere/After Effects/Final Cut panels.
**[FINDING]** There is **no moat** for a solo operator to enter this category. Pricing pressure
is brutal (per-seat races to zero, "unlimited reviewers" is table stakes), and the AI features
you'd lead with (auto-tagging, transcript search, auto-assembly of variants) are **already
shipped** by these tools and by Adobe itself.

**Correct posture:** do NOT rebuild this. **Integrate** with it. The engine should *orchestrate
the handoff* (ingest → assign → notify → track status → trigger delivery) and let the cut live
in Frame.io / a Premiere panel / Pixieset. That is an orchestration layer, not an editing SaaS.

### 3b. Actual *editing / rendering* (the creative + GPU-render layer)
This is human creative labor (decisions, retouch, grade, cut) plus GPU render. Two hard walls:
- **It's labor, not software.** The engine can prep, assemble rough strings, and chase
  approvals, but the editorial judgment is the product clients pay for. You can't SaaS-ify the
  judgment without the operator.
- **The AI-assembly layer has no moat.** [UNCONFIRMED — was logged in memory as Adobe "Quick
  Cut", Feb 2026; treat the exact product name as unverified, but the *capability* — shot-list-
  driven rough-cut assembly inside Premiere for all subscribers — is real and now broadly
  available.] Building "AI rough-cut assembly" as your wedge means competing with the tool your
  customers already pay for.
- **Hosting render/storage for tenants = the §2 COGS inversion at its worst.**

**Net answer to "how would we manage editing/post as a SaaS":** you realistically *don't* host
it. The only sane version is BYO-editing/BYO-storage: the customer keeps their footage and their
NLE; your product only orchestrates state and handoffs. The moment you try to *own* the editing
or the storage, the economics and the moat both collapse.

---

## 4. MARKET REALITY (2026, web-grounded this session)

- **Post-prod review/management:** saturated (see §3a). Crowded enough that the *content
  marketing* is now "best Frame.io alternatives" listicles — a tell that the category is
  commoditized and competing on price/onboarding, not capability.
- **Pre-production / shoot ops:** also crowded and increasingly AI-native — StudioBinder,
  Studiovity, Boords, Celtx, Shot Lister, Scriptation, plus photographer CRMs (HoneyBook /
  Dubsado / Táve / Studio Ninja class) and Notion as the generic hub. Several now auto-generate
  shot lists/storyboards/call sheets from a script. This matches the vault's prior finding that
  **Notion covers ~70% of the pre-production-manager spec for free.**
- **Synthetic-UGC SaaS (Arcads / Creatify / HeyGen class):** [from memory, not re-verified this
  session] the funded UGC-SaaS money has gone to AI-generated avatars, i.e. *replacing* real
  shoots. That is a **different market** from yours (real athletes/clients on retainer, actual
  filming). They are not your competitors and you are not theirs — but it also means there is no
  VC tailwind behind "software for people who run real shoots." You'd be building into a niche
  the funded market has walked away from.

**Implication:** every layer of the pipeline you might productize already has multiple
established players. A new entrant needs either (a) a real moat or (b) a sharp niche the
incumbents serve badly. The engine gives you neither *as generic SaaS* — its moat (free local
compute) doesn't transfer to customers.

---

## 5. VIABILITY SCORECARD

Scored 1 (bad) – 5 (good) for SFV-as-it-is. **[INFERENCE — directional, not precise.]**

| Dimension | Score | Note |
|---|---:|---|
| Moat / defensibility | 1 | Cost moat is local; doesn't transfer. Logic is copyable. |
| Gross margin at scale | 2 | Storage/egress/compute eat video SaaS margins (§2). |
| TAM (real-shoot ops niche) | 2 | Small; funded market moved to synthetic avatars. |
| Competitive whitespace | 1 | Every layer has multiple incumbents (§3a, §4). |
| Build cost to genericize | 2 | Engine is bespoke to your branches/vault; big rebuild. |
| Solo-operator support load | 1 | SaaS = 24/7 uptime + support for strangers' deadlines. |
| Distribution / GTM | 2 | No audience, no channel, no sales motion yet. |
| Fit with SFV's real goal | 4 | Engine as *internal* advantage is already the right call. |

**Weighted read:** as **multi-tenant SaaS**, this is a 1–2. As an **internal operating
advantage that powers a productized service**, it's a 4 — which is the path you already have.

---

## 6. THREE HONEST PATHS

### Path A — Engine as private moat → productized service + operators  **[RECOMMENDED]**
Don't sell software. Sell *faster, more consistent output* that the engine lets you deliver,
then scale via trained field operators (your existing ~40%-rev-share, no-equity model). The
engine stays internal — it never has to be hardened, multi-tenant, supported, or genericized.
- **COGS:** stays ~$0 marginal (local compute). Margin is your time + operator share.
- **Moat:** the engine + your craft + your delivery system, none of it exposed to copy.
- **Risk:** low. This is the Halifax → Maritime → Midwest plan already in the vault.
- **Downside:** revenue scales with operators/shoots, not with seats. Slower ceiling than a
  hypothetical hit SaaS — but a *real* ceiling vs a speculative one.

### Path B — Thin BYO-compute orchestration tool (the one non-dead software path)  **[PROBE ONLY]**
A narrow product that does ONE painful thing incumbents do badly, for ONE niche, where the
**customer brings their own storage + NLE + review tool** so you never eat media COGS. Best-fit
niche = the workflow you already operate and understand cold: **on-site event/sports photo
delivery** (your SFV_EVENTS QR system — Cam-prefix sorting, same-day delivery, multi-day fresh
stacks). Sell the *logistics spine*, integrate Zenfolio/Pixieset/Frame.io rather than replace
them. See §7.
- **COGS:** low if strictly BYO-compute. **Moat:** weak (workflow knowledge, not tech).
- **Risk:** medium-high. Small TAM, solo support burden, distribution unsolved.

### Path C — Full multi-tenant "Engine as a Service"  **[NOT RECOMMENDED]**
Host editing/post/storage/compute for tenants. This is the §2 inversion + §3 saturation +
solo-operator uptime burden, all at once. Don't.

---

## 7. IF YOU INSIST ON SOFTWARE — THE ONLY WEDGE WORTH TESTING

**Product:** "Shoot-to-Delivery spine for on-site event photographers." Not an editor, not a
review tool, not storage. A thin orchestration layer that:
1. ingests by camera-prefix convention, auto-sorts by your filename rules (your locked logic),
2. tracks each subject/QR card → gallery state,
3. fires delivery via the customer's *own* Zenfolio/Pixieset account,
4. chases approvals / flags missing deliverables, end-to-end status in one view.

**Why this and not "manage editing":** it deliberately **avoids** the editing/post layer (no
moat, all COGS). It sells logistics, the thing you've actually solved and that StudioBinder/
Notion/CRMs do *generically* but not *for the same-day on-site delivery* edge case.

**Constraints that keep it viable:** strictly BYO-storage + BYO-gallery (zero media on your
infra); single sharp niche before any expansion; price for a solo operator's support ceiling.

**Validation gate before ANY build (cheap, ~2 weeks):**
- 5–8 problem interviews with on-site event/sports shooters (Brandon Bellotti is the logged
  first design-partner candidate — start there).
- Confirm they currently lose real time/money on this *specific* handoff, and that Notion + a
  CRM + Zenfolio don't already cover it for them.
- One pre-sell / LOI before a line of product code. No LOIs → don't build. Blueprint Lock applies:
  no build until validated AND Will ratifies.

---

## 8. WHAT WOULD HAVE TO BE TRUE TO CHANGE THE RECOMMENDATION

The call flips toward software ONLY if several of these become true (they are not, today):
- You stop being a solo operator (a cofounder/hire owns product + support uptime).
- A niche emerges that is in real pain AND underserved AND reachable by you (validate, don't assume).
- The model is strictly BYO-compute so gross margin survives (§2).
- You have or can build a distribution channel (audience, partner, or community) — currently absent.
- You're willing to trade SFV growth focus for vendor focus. These compete for the same you.

If you can't check most of these, Path A is not a consolation prefix — it's the better business.

---

## 9. RECOMMENDATION + DECISION GATE  [FOR HUMAN REVIEW]

**Recommended:** **Path A** (engine as private moat → productized service + operators) as the
primary line. Optionally run the **Path B §7 validation probe** in parallel — it is *discovery,
not development*, so it doesn't violate Blueprint Lock and costs ~2 weeks of conversations, no code.

**Decisions for Will (answer to advance):**
- **S1.** Kill, shelve, or probe the SaaS idea? (recommend: **probe Path B, commit to Path A**)
- **S2.** If probing: approve reaching out to Brandon Bellotti as design-partner #0 for discovery?
- **S3.** Confirm the hard constraint: any future tool is **BYO-storage + BYO-editing**, engine
  never hosts tenant media. (recommend: **yes — non-negotiable**)
- **S4.** Should I write a follow-on `PATH_B_DISCOVERY.md` (interview script + 5 kill-criteria
  questions) so the probe is ready to run, or hold until S1?

Nothing here is CANON. No build, no live-system change was made. This doc is additive and FHR.

---

## CONNECTED FILES
- [[SESSION_STATE|Session State]]
- [[UGC_PRE_PRODUCTION|UGC Pre-Production Manager Spec]]
- [[BLUEPRINT_COVERAGE_MAP|Blueprint Coverage Map]]
- [[PROPOSALS|Proposals for Human Review]]
- [[DELIVERY|Delivery Workflow]]
- [[EVENTS_ZENFOLIO_DELIVERY|Events Zenfolio Delivery]]

---

## 10. THE OPERATOR-TOOL REFRAME (script → edit → schedule → analytics loop)

**Concept (Will, 2026-06-28):** one tool that generates scripts/shot lists, ingests the operator's
footage and **edits it**, writes captions + schedules posts, then pulls last month's per-reel
analytics and feeds that back to optimize next month's content. **Buyer = the operators Will
would otherwise subcontract.**

This is a stronger framing than §7 in two ways: it's an *integrated loop*, and selling to the
operator network **partly solves the distribution problem** that killed the generic-SaaS case.
But the components have very different economics, and the buyer choice creates a strategic trap.

### 10a. Component-by-component verdict (web-grounded, 2026-06-28)

| Component | Moat | COGS | 2026 reality |
|---|---|---|---|
| Script / shot-list gen | low | ~$0 (LLM) | StudioBinder/Studiovity/Boords/Celtx auto-gen this; Notion ~70%. |
| **Upload → it edits** | **none** | **high** | **Commoditized.** OpusClip, Submagic, Reap, Bytecap, Descript, CapCut, Captions/Mirage all do clip-detect + reframe + B-roll + render. APIs exist. |
| Captions + scheduling | none | low-med | Submagic ships publishing + AI titles/hashtags + Brand Kit since Mar 2026; schedulers (Later/Metricool/Buffer) own this. |
| **Analytics → next-month optimization loop** | **medium** | low | **The one piece that isn't a packaged product.** Tools have per-clip virality scores; a true roster-level monthly perf→strategy loop is thin in market. |

**Headline:** the COGS-heavy middle ("it edits") is exactly the part with **zero moat** and a
field of **funded incumbents already selling to agencies/operators** at $12–80/mo with n8n/Zapier
APIs. Submagic case studies cite agencies saving 24 hrs/wk and +300% revenue *without hiring
editors* — i.e. your target buyer can already buy this today. Rebuilding it is a losing race.

The **bookends** are cheaper and the **analytics loop is the actual differentiator** — but that
loop is a *strategy/service* advantage, not a render pipeline.

### 10b. The strategic trap in "sell it to the operators I'd subcontract"

This is the part to slow down on. Selling the SFV system to your own operator pool **works
against the model the vault already locked in** (engine = *private* competitive advantage;
operators on ~40% rev-share, no equity):

1. **It hands your edge to your labor pool / future competitors.** The rev-share works because
   SFV brings the system + the clients + the brand. If an operator can buy the system for $X/mo,
   the obvious next question is "why give SFV 60%?" You'd be financing your own disintermediation.
2. **The buyer can already self-assemble it.** Submagic Business ($41) + a scheduler + ChatGPT
   covers most of what you'd sell. You'd compete with funded tools, on price, for a tiny audience.
3. **Thin TAM + solo support burden** still apply (§5).

### 10c. The version of this instinct that is actually good  [RECOMMENDED REDIRECT]

Don't sell it as open-market SaaS. Build it as an **internal enablement layer for the SFV
operator network** — the connective tissue that makes any operator produce *SFV-quality,
SFV-branded* output on the SFV playbook. Then:
- **Wrap best-of-breed, don't rebuild.** Orchestrate OpusClip/Submagic + a scheduler via their
  APIs for the edit/caption/post middle. Your engine already does routing/handoff — point it at
  those APIs. You pay pass-through cost, you own none of the no-moat plumbing.
- **Build the proprietary layer = (a) the SFV playbook/templates + (b) the analytics→next-month
  loop.** That loop is the real wedge and it's where your domain taste compounds. Keep it internal.
- **Monetize via the rev-share, not seats.** The tool is the *reason the rev-share is worth it*
  (operators produce more, faster, on-brand), which **raises** SFV's take and **strengthens** the
  moat — the opposite of selling the moat for $41/mo. This is Path A with better tooling, not SaaS.

**If you still want to test open-market SaaS:** the only piece worth probing standalone is the
**analytics→optimization loop** (the one medium-moat component), sold to people who already run
real shoots and already use OpusClip/Submagic — i.e. a thin strategy layer *on top of* the tools
they keep. Validate with the §7 gate (interviews + LOI) before any build. Everything else: buy, don't build.

### 10d. Decision update
- **S5.** Accept the redirect — internal enablement layer wrapping 3rd-party edit/schedule tools,
  proprietary = playbook + analytics loop, monetized via rev-share (recommend: **yes**)?
- **S6.** If anything ships standalone, restrict scope to the **analytics→optimization loop** only?

---

## 11. CONSUMER / TIERED REFRAME — vendor economics vs the render-COGS firehose

**Concept (Will, 2026-06-28):** go broader, not gatekept. Tiered subs incl. a cheap consumer tier:
app gives you the content idea → built-in teleprompter → you shoot in-app → a finished reel pops
out later → analytics feed next month. Sell across provinces; modest profit is enough. Buyer is no
longer just operators — it's "anyone trying to do social media."

### 11a. What Will is RIGHT about  [CONCEDED]
- **Vendor pivot is a real strategy.** Becoming a tooling vendor genuinely offloads client-finding,
  agency overhead, and per-client churn. That's a legitimate trade, not a cope.
- **Modest-profit bar is legitimate.** Not every business must be VC-scale. A lifestyle software
  business clearing a low bar across a few provinces is a valid goal. The earlier analysis implicitly
  judged against a "big business" bar; against a "enough to be profitable" bar the question changes.

These two points apply cleanly to a **pro/operator tier**. They do **not** rescue the consumer tier —
for three structural reasons below.

### 11b. The consumer flow Will described already ships FREE from the platform  [DECISIVE]
**Instagram Edits** (Meta, free, mobile, **no paid tier, watermark-free**, 7M downloads first week,
130+ features in year 1, weekly updates) already does the *entire* described loop:
idea boards + trending sounds, **built-in teleprompter** (record AND voiceover), full in-app camera
(to 10 min), auto-captions, AI restyle / cut-silences / object tracking, **direct Reels publishing**,
and a built-in **analytics/insights tab** (skip rate, retention, watch time, share rate). CapCut covers
the same ground. Competing on the consumer tier = competing against **the destination platform's own
free first-party app**, for the same workflow. That is the hardest position in consumer software.

### 11c. "A reel pops out later" is a COGS firehose on a free/cheap tier  [DECISIVE]
"Shoot in app → reel pops out" means **Will renders every user's video** — on his GPU or via a paid
API (Submagic ~$0.69/min; OpusClip credits). That cost **scales with usage, not revenue**. A free or
cheap tier is exactly where usage is highest and revenue lowest. The business can **lose money fastest
precisely when it 'succeeds.'** The only configs that survive at modest revenue are **BYO-render**
(user shoots/exports in Edits/CapCut themselves) — which means Will is *not* building the render app.

### 11d. "Shoot in app" = a real mobile app = NOT low-overhead  [INFERENCE]
A cross-platform capture app (iOS+Android camera, teleprompter UI, upload, processing queue, billing,
support, app-store review/compliance, ongoing updates vs Meta's weekly cadence) is a heavy, permanent
solo-operator burden. The agency overhead Will wants to escape gets **replaced by software-company
overhead that is heavier, not lighter.** Churn doesn't vanish either — agency client-churn becomes
consumer-subscription churn, which in creator tools is notoriously high (try once, post twice, cancel).

### 11e. The distribution edge only exists for the PRO tier  [KEY]
Will's one real advantage — a warm channel to operators — reaches operators, **not** "anyone doing
social media." For the consumer tier he has no channel and would compete with Meta's distribution.
So the broad consumer move *gives up the single thing that made any software path viable.*

### 11f. The version that actually gets Will what he wants  [RECOMMENDED]
Goal restated from Will: low-overhead, recurring, modest-profit-is-fine, not gatekept, helps normal
people. The shape that delivers that **without** the Edits collision, the render firehose, or a mobile
build:

**Don't build the capture/edit/render app — that's free from Meta and a cost firehose.** Build the
**idea + optimization brain**, BYO-capture:
- App/site hands the user a **content idea + script + shot plan + posting schedule**.
- User shoots it **free in Instagram Edits / CapCut** (their teleprompter, their render — zero COGS to Will).
- User connects or pastes their **per-reel analytics**; the **monthly optimization loop** (Will's one
  medium-moat component) learns what works for *that* account and writes next month's ideas.
- Proprietary = the **idea engine + the analytics→strategy loop + SFV playbook**. Ongoing, not one-time-copyable.
- COGS ≈ LLM calls only (cheap, local Ollama possible). Overhead ≈ low. Tiers: cheap consumer (idea+loop),
  pro/operator (adds the SFV network + rev-share). **Not gatekept**, fits the modest-profit bar, and
  arms no one with the part that matters because the value is the compounding loop, not a feature.

Even here, Meta's idea boards + insights are adjacent — so the wedge is **personalized monthly
optimization across a roster**, which Edits' raw insights tab does not do. Validate that gap is real
(§7 gate) before any build.

### 11g. Decision update
- **S7.** Split the tiers correctly: **pro/operator** = vendor model (Will's 11a points apply);
  **consumer** = idea+optimization brain only, **BYO-capture**, no render on Will's infra (recommend: **yes**)?
- **S8.** Kill "shoot-in-app + reel-pops-out" as a build target (free from Meta + COGS firehose +
  mobile burden); deliver that step via Instagram Edits/CapCut instead (recommend: **yes**)?
- **S9.** Confirm the standalone wedge to validate = **personalized monthly optimization loop**, not editing?

---

## 12. REFINED B2B CONCEPT — style-intake + production planning for reel shooters

**Concept (Will, 2026-06-28):** specialized B2B service for people who already make reels *for others* —
freelance/contracted shooters, in-house camera ops / media teams, marketing agencies (enterprise).
Two style inputs: (a) **learn from the company's existing content**, or (b) **guided website intake
form** detailing desired content styles, **with AI suggestions during signup/intake**. Niche-agnostic
engine; **beachhead niche = contracted IG-reel shooters** who'd save real time. **Teams feature**
(enterprise): agencies bring their own teams, in-site comms + per-member work overview.

**This is the defensible shape.** It clears the three traps that killed the earlier framings:
B2B not consumer (no Meta Edits collision — that's a *creation* tool for the poster; this is a
*production-ops* layer for people producing for others), BYO-capture (no render firehose), and a
time-is-money buyer with legible ROI. Credit also: intake-form-with-suggestions is good UX *and*
solves the style engine's cold-start; the beachhead-niche instinct is correct.

### 12a. Competitive map (web-grounded 2026-06-28) — where NOT to fight
The **team / multi-client / approval / per-member-overview** layer is a **mature, saturated** category:
Planable (collaboration/approval-first, workspace-per-client, unlimited users, in-context comments,
multi-level approval, version history, AI post creation; $33–49/workspace + custom enterprise),
plus Metricool, Sprout, Hootsuite, SocialPilot, Agorapulse, Sendible, Loomly, Later, Buffer, Vista
Social, Statusbrew, Zoho. They have AI ideation bolted on now too.
**[FINDING]** Do **not** rebuild the approval/seat/calendar machinery — you will not out-build Planable
as a solo dev, and "manage your social team's posts" is DOA against it.

### 12b. The actual wedge — UPSTREAM of those tools
Every incumbent starts at *"you already have a post → route it for approval/scheduling."* They treat the
**front of the pipeline thinly.** Will starts one step earlier: *"you have a client/brand → here's
exactly what to shoot, in their style, as ideas + scripts + shot lists for the shooter."* That
**style-intake → on-brand production planning for video shooters** is a real seam the scheduling/approval
tools don't own. Position there. The team feature should be **lightweight + in service of the shoot
workflow** (who's assigned which client's shoot, status of each shooter's deliverables) and ideally
**export/integrate** into whatever scheduler the agency already runs — not a Planable clone.

### 12c. Three honest guardrails (independent of competition)

1. **Style-learning OUTPUT QUALITY is the make-or-break — not the team feature.** Pros pay for taste
   and differentiation; their whole value is not-being-generic. If the ideas/scripts/shot lists read
   like default LLM mush, they churn in week one. "Learn from existing content" + "guided intake" are
   the right *inputs*, but the bar on the *output* is brutal and is the central product risk. Build and
   **validate this first**, before a line of team-feature code. If it can't beat what a good shooter
   produces in 20 min, nothing else matters.

2. **"Reapplicable to all niches" is a positioning trap.** Horizontal = hard to sell, easy to be
   out-focused. Build the engine niche-agnostic *under the hood*, but **sell ONE sharp niche**
   (contracted IG-reel shooters). "Works for everyone" is a phase-2 expansion story, never the launch
   pitch. (Will already senses this — reinforce it.)

3. **Enterprise/teams vs. low-overhead-solo pull in opposite directions.** Enterprise = SSO, security,
   SLAs, high-touch sales, support load — the opposite of "modest overhead." **Resolution:** launch
   **self-serve SMB/prosumer** (individual shooters + small teams), add the enterprise/teams tier only
   *after* the ideation engine is proven and a real buyer is pulling for it. Don't lead with enterprise.

   Minor residual: a tool that makes contracted shooters more self-sufficient slightly loosens agency
   lock-in. That's just the nature of being a vendor — acceptable, not a blocker.

### 12d. Positioning one-liner (draft, FHR)
"The production brain for reel shooters: tell us the brand (or drop their best reels), get a month of
on-brand ideas, scripts, and shot lists — then track every shoot and shooter in one place."
Sits **upstream** of Planable/Metricool, not against them.

### 12e. Decision update
- **S10.** Endorse the upstream positioning — own **style-intake + production planning**, keep team
  feature lightweight, integrate with (not rebuild) schedulers/approval tools? (recommend: **yes**)
- **S11.** Sequence: validate **ideation/style output quality** FIRST; build teams/enterprise LAST? (recommend: **yes**)
- **S12.** Launch motion = **self-serve, contracted-IG-reel-shooter niche**; enterprise/teams = phase 2? (recommend: **yes**)
- **S13.** Want me to draft `PRODUCTION_BRAIN_SPEC.md` (intake schema + style-ingestion approach +
  validation test that pits engine output against a real shooter's manual output) once S10–S12 are set?
