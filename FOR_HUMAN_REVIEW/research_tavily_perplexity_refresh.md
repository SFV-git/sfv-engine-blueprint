# Research Refresh: Tavily Search API vs Perplexity API — Pricing & Rate Limits (2026)

**Date compiled:** 2026-07-01
**Purpose:** Refresh current (2026) entry-tier pricing and rate limits for the Tavily Search API and the Perplexity (Sonar) API, for a **low-volume, occasional automated research route** inside an n8n workflow.
**Status:** Informational only. This document **informs, but does not decide**, whether to proceed with the existing Tavily-based `RESEARCH_ROUTE_SPEC.md` plan.
**Scope note:** No n8n, Docker, git, live service, or API key was touched in producing this. Figures below are read from vendor docs where possible; secondary aggregators are flagged as such.

---

## TL;DR for the n8n research route

- **Tavily** has a genuine, indefinite **free tier of 1,000 API credits/month, no credit card required.** For an occasional/low-volume route this may cost **$0/month**. Basic search = 1 credit, advanced = 2 credits. Dev rate limit is **100 requests/min** — far above a low-volume route's needs.
- **Perplexity Sonar** has **no permanent free tier**: you must add a payment method to get an API key, and pay per-token **plus** a per-request search fee. Cheapest model (`sonar`) is **$1 / $1 per 1M tokens** with a **$5–$12 per 1,000 requests** search fee on top. Tier 0 (no spend) allows **50 RPM** for `sonar`/`sonar-pro`.
- For genuinely low volume, **Tavily is the cheaper and simpler entry option** (free tier covers occasional use). Perplexity's strength is that each call returns a synthesized, cited answer rather than raw search results — a different output shape, not just a price difference. This supports (does not mandate) staying with the existing Tavily-based plan.

---

## Tavily Search API

### Free tier
- **1,000 free API credits every month. No credit card required.** Indefinite (not a time-limited trial).
- **Credits do not roll over** month to month (per secondary sources).

### Credit cost per search
- **Basic Search:** 1 credit / request
- **Advanced Search:** 2 credits / request
- (Other endpoints: Extract 1–2 credits per 5 URLs; Map 1–2 credits per 10 pages; Research endpoint 4–250 credits/request depending on mini vs pro model.)

### Paid plans (from official docs)
| Plan | Monthly credits | Price/mo | Approx. $/credit |
|------|-----------------|----------|------------------|
| (Free) | 1,000 | $0 | — |
| Project | 4,000 | $30 | ~$0.0075 |
| Bootstrap | 15,000 | $100 | ~$0.0067 |
| Startup | 38,000 | $220 | ~$0.0058 |
| Growth | 100,000 | $500 | ~$0.005 |

- **Pay-as-you-go:** $0.008 per credit once the free/plan allotment is exhausted.

> Note: A secondary aggregator (costbench) listed slightly different plan names/prices ("Researcher $30", "Startup $100"). The table above follows Tavily's own docs pages, which should be treated as authoritative. Vendors do rename/re-tier plans, so **verify against tavily.com/pricing at implementation time.**

### Rate limits
- **Development environment: 100 requests/minute** (testing/free-tier dev use).
- **Production environment: 1,000 requests/minute.**

### Recent changes / notes
- No major pricing/API breaking change surfaced for Tavily in 2026 search results. Plan tiers and per-credit pricing appear to be the main variables; confirm at build time.

---

## Perplexity API (Sonar)

### Free tier / credits
- **No permanent free tier.** Free (non-paying) accounts get **zero API credits** and must add a payment method to generate an API key.
- New accounts may receive a **one-time ~$25–$50 trial credit** (per secondary sources; not stated on the official rate-limits page). Treat as promotional, not guaranteed.
- **2026 change:** Perplexity **Pro subscriptions no longer bundle the recurring ~$5/month API credit** — this perk ended **February 2026**. A Pro plan no longer subsidizes API usage.

### Pricing (cheapest model = `sonar`)
- **Token price:** $1.00 / 1M input tokens, $1.00 / 1M output tokens.
- **Per-request search fee (on top of tokens), by context depth:**
  - Low context: **$5 per 1,000 requests** (~$0.005/request)
  - Medium context: **$8 per 1,000 requests** (~$0.008/request)
  - High context: **$12 per 1,000 requests** (~$0.012/request)
- **Sonar Pro** (flagship): **$3 / $15 per 1M tokens** (in/out), plus higher per-request fees.
- **2026 cost change:** **Citation tokens are no longer billed** for standard Sonar and Sonar Pro, lowering effective cost per response vs prior years.

### Rate limits (Tier 0 = no spend / entry)
| Model | Tier 0 RPM |
|-------|-----------|
| `sonar` | 50 RPM |
| `sonar-pro` | 50 RPM |
| `sonar-deep-research` | 5 RPM |

- Tiers advance by **cumulative lifetime spend**: Tier 0 = $0, Tier 1 = $50+, Tier 2 = $250+, Tier 3 = $500+, Tier 4 = $1,000+, Tier 5 = $5,000+. Tiers are permanent (no downgrade) and raise RPM limits.

---

## Cost comparison for a low-volume route (illustrative)

Assume the n8n route makes an **occasional** research call — say **~100 basic searches/month**.

| Option | Monthly cost estimate | Notes |
|--------|----------------------|-------|
| **Tavily (free tier)** | **$0** | 100 basic searches = 100 of 1,000 free credits. No card required. |
| **Perplexity `sonar`** | **~$0.50–$1.20 + token cost** | 100 requests × $0.005–$0.012 search fee, plus ~$1/1M tokens. No free tier; card required. Likely **a few dollars/month** in practice. |

For occasional/low-volume use, **Tavily's free tier makes it effectively free**, while Perplexity has an unavoidable (small) floor cost and requires billing setup. This is a **capability vs cost** trade, not purely cost: Perplexity returns a synthesized, cited answer; Tavily returns search results (optionally with an LLM-generated answer field). Whether the route needs raw results or a finished answer should drive the choice as much as price.

---

## Implication for `RESEARCH_ROUTE_SPEC.md` (informational)

- Nothing found here **contradicts** an existing Tavily-based plan for a low-volume route; Tavily's free tier and generous dev rate limit remain well-suited to occasional queries.
- The main **watch-items** if revisiting: (a) Tavily plan names/prices may have shifted since these docs — re-check `tavily.com/pricing` before committing; (b) credits **don't roll over**, so bursty usage could exceed the monthly 1,000 free credits; (c) if the route ever needs finished, cited prose rather than search hits, Perplexity Sonar becomes worth its small per-call cost.
- **No change to the plan is asserted here.** Human review decides.

---

## Sources

Tavily:
- https://www.tavily.com/pricing
- https://docs.tavily.com/documentation/api-credits
- https://docs.tavily.com/documentation/rate-limits
- https://help.tavily.com/articles/3240802908-rate-limits
- (secondary/aggregator, flagged) https://costbench.com/software/web-scraping/tavily/
- (secondary/aggregator, flagged) https://www.firecrawl.dev/blog/tavily-pricing

Perplexity:
- https://docs.perplexity.ai/docs/getting-started/pricing
- https://docs.perplexity.ai/docs/admin/rate-limits-usage-tiers
- (secondary/aggregator, flagged) https://www.cloudzero.com/blog/perplexity-api-pricing/
- (secondary/aggregator, flagged) https://suprmind.ai/hub/perplexity/pricing/
- (secondary/aggregator, flagged) https://www.getaiperks.com/en/ai/perplexity-api-free-credits-2026

> Vendor pricing changes frequently. Where secondary aggregators disagreed with vendor docs, vendor docs were preferred and discrepancies flagged inline. Re-verify against the official pages before implementation.

## CONNECTED FILES
- [[DASHBOARD|Dashboard]]
- [[SESSION_STATE|Session State]]
