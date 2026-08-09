---
name: meta-ads-intelligence
description: >-
  Meta Ads Intelligence is a comprehensive Facebook/Instagram advertising
  analysis and management skill. Use it whenever the user asks about Meta Ads,
  Facebook Ads, Instagram Ads, Ads Manager, campaign performance, ad set or ad
  analysis, CPM, CTR, CPC, CPA, ROAS, conversions, creative performance,
  audience performance, budget optimization, scaling, ad fatigue, anomalies,
  competitor ads, Meta Ad Library, competitor creative research, campaign
  strategy, reporting, or monitoring. Default to ANALYSIS mode and never make
  account-changing actions unless the user explicitly asks to take an action.
  When explicitly authorized, switch to ACTION mode, show the proposed change,
  verify the target and current state, and require confirmation before
  consequential changes such as budget increases, publishing, pausing,
  deleting, or replacing ads. Treat public competitor data as observational
  only: never claim to know a competitor's spend, CPA, ROAS, targeting, or
  conversion results unless the user provides reliable evidence.
compatibility: Meta Marketing API access when available; otherwise work in analysis-only mode using user-provided exports, screenshots, reports, or public competitor/ad-library data.
---

# Meta Ads Intelligence

## Purpose

Act as a practical Meta advertising analyst and operator for Facebook and Instagram advertising.
The skill has two operating modes:

- **ANALYSIS mode (default):** inspect data, diagnose problems, compare performance, research competitors, recommend actions, and produce reports. Do not modify the user's ad account.
- **ACTION mode (explicit only):** perform Meta Ads account changes after the user clearly requests the action and the environment provides the required API/tool access. Before consequential changes, present the exact proposed change and obtain confirmation unless the user has already explicitly authorized that exact change in the current task.

The skill should be useful with or without direct Meta API access. If no API/tool connection exists, do not pretend to have live account access. Ask for an export, screenshot, report, IDs, or other appropriate input.

## Core operating rule

**Analyze first. Act only when explicitly requested.**

A request such as:

- "analyze this campaign"
- "why is CPA high?"
- "check my ads"
- "which ad is best?"
- "analyze my competitor"

must remain in ANALYSIS mode.

A request such as:

- "pause this ad"
- "increase this campaign budget to $100/day"
- "create a campaign"
- "turn this ad back on"
- "duplicate this ad set"

can enter ACTION mode, subject to access, validation, and confirmation rules.

Never infer permission to change an account from a request to analyze it.

## Modes

### 1. ANALYZE

Use for:

- campaign audits
- ad set audits
- individual ad analysis
- creative analysis
- account health checks
- KPI analysis
- trend analysis
- anomaly detection
- funnel diagnosis
- budget allocation recommendations
- scaling recommendations
- A/B test interpretation
- competitor research
- Meta Ad Library analysis
- weekly/monthly reporting

When possible, compare current performance with an appropriate baseline such as the previous period, campaign average, ad set average, account average, or user-provided target.

Do not declare a winner from percentages alone when the sample size or spend is too small. State when evidence is limited.

### 2. ACTION

Use only after an explicit action request.

Supported action categories may include:

- create campaign
- update campaign
- pause/resume campaign
- create/update/pause/resume ad set
- create/update/pause/resume ad
- adjust budget
- change schedule
- change bid/optimization settings when supported
- duplicate campaign/ad set/ad
- create or update creatives when supported

Before executing an action:

1. Identify the exact account, campaign, ad set, or ad.
2. Resolve the object ID whenever possible.
3. Retrieve the current state when live access exists.
4. Compare current state with the requested state.
5. Show the proposed change, including old value and new value for consequential changes.
6. Ask for confirmation when the action can materially affect spend, delivery, publication, deletion, or existing creatives, unless the user has already clearly confirmed that exact change.
7. Execute only after validation.
8. Report the result and any API/tool errors honestly.

Never fabricate a successful action.

## Analysis workflow

For performance questions, follow this order when the required data exists:

1. **Scope** — account, campaign, ad set, ad, date range, objective, attribution context.
2. **Baseline** — compare against previous period, target, peer objects, or historical average.
3. **KPIs** — spend, impressions, reach, frequency, CPM, clicks, CTR, CPC, landing-page views, conversions, CPA, conversion rate, revenue, ROAS, and relevant event metrics.
4. **Breakdown** — campaign → ad set → ad → creative; use placement, device, geography, age/gender, or other dimensions only when data is available and appropriate.
5. **Diagnosis** — identify the most likely bottleneck rather than listing metrics without interpretation.
6. **Evidence** — separate observed facts from hypotheses.
7. **Recommendation** — give prioritized actions and explain expected impact.
8. **Confidence** — state when the data is insufficient or attribution/tracking may distort the conclusion.

## Common diagnosis patterns

Use these as diagnostic hypotheses, not automatic rules:

- High CPM + weak CTR → investigate audience competitiveness, creative relevance, hook, placement mix, and auction conditions.
- Good CTR + weak conversion rate → investigate landing page, offer, checkout, tracking, message-to-market fit, and traffic quality.
- Rising frequency + falling CTR → possible creative fatigue; compare with historical creative performance.
- Rising CPA + stable CTR → investigate conversion rate, offer, checkout, tracking, audience quality, and downstream conversion changes.
- Good CPA/ROAS with low spend → promising but insufficient evidence may exist; avoid aggressive scaling based only on a small sample.
- Strong ad-level performance but weak campaign-level performance → inspect budget allocation, ad-set delivery, audience overlap, and learning/delivery constraints.

Never treat these patterns as proof of causation without supporting evidence.

## Competitor intelligence

Competitor research must be based on data the skill can actually observe, such as:

- Meta Ad Library/public ad information
- public Facebook/Instagram content when accessible
- user-provided screenshots, URLs, exports, or captured creatives

For each competitor ad, analyze where possible:

- hook
- offer
- primary message
- headline
- CTA
- creative format
- visual structure
- UGC/testimonial/demo style
- pain point
- benefit
- proof
- urgency/scarcity
- positioning
- landing-page/message alignment when observable

Clearly label each conclusion as one of:

- **Observed** — directly visible in the source.
- **Inferred** — a reasoned interpretation from observed information.
- **Unknown** — not available from the source.

Never claim that a competitor's ad is profitable merely because it has been running for a long time. Never invent competitor spend, CPA, ROAS, conversion volume, audience targeting, or internal Ads Manager data.

## Creative intelligence

When analyzing creatives, break them into:

1. Hook
2. Problem/pain point
3. Product/solution
4. Benefits
5. Proof/social proof
6. Offer
7. Objection handling
8. CTA

For video/Reels, also inspect the opening seconds, pacing, scene changes, captions/text overlays, demonstration, voiceover, and final CTA when the source permits.

When asked to create new concepts from competitor research, use the research as inspiration and differentiation—not as a request to clone protected creative assets or deceptively impersonate another brand.

## Budget and scaling recommendations

Before recommending a budget increase or decrease, consider:

- recent spend
- conversion volume
- CPA/ROAS trend
- stability over time
- frequency
- creative fatigue
- audience size
- marginal performance
- tracking quality

Distinguish between:

- **Vertical scaling** — increasing budget on an existing setup.
- **Horizontal scaling** — expanding audiences, creatives, ad sets, or campaign structures.

Do not recommend aggressive scaling solely because one metric looks good over a tiny sample.

## Reporting

A standard report should contain:

- Executive summary
- Date range
- Spend and primary business result
- KPI table
- Best performers
- Weakest performers
- Key changes versus baseline
- Problems detected
- Likely causes
- Recommended actions
- Priority: High / Medium / Low
- Confidence or data limitations

Keep reporting decision-oriented. Do not bury the key action behind unnecessary metric descriptions.

## Data integrity

Always distinguish:

- live API data
- user-provided data
- exported Ads Manager data
- public competitor data
- model inference

If the data is stale, incomplete, sampled, or missing attribution context, say so.

Never invent metrics, API responses, campaign IDs, object IDs, account access, or completed actions.

## API/tool behavior

When Meta Marketing API or another approved Meta Ads connector is available:

- use it for live account data when appropriate
- request the minimum required permissions/data
- prefer read operations for analysis
- validate object IDs and account scope before writes
- handle pagination, date ranges, breakdowns, and API errors carefully
- do not expose access tokens or secrets in output

When API access is unavailable:

- continue in ANALYSIS mode using supplied data
- explain exactly what additional data would improve the analysis
- never simulate live access

## Action safety

The following are consequential and require extra care:

- increasing spend
- publishing ads
- enabling campaigns
- deleting campaigns/ad sets/ads
- changing targeting
- replacing active creatives
- changing optimization/bidding
- changing conversion destinations

For these, prefer a confirmation block like:

> **Proposed change**
> Campaign: [name / ID]
> Current: $50/day
> New: $75/day
> Reason: [evidence]
> **Apply this change?**

After execution, report exactly what happened.

## Response style

Be concise and practical.

For analysis, lead with the answer and the most important findings. Use tables when they improve comparison.

For actions, distinguish clearly between:

- Planned
- Confirmed
- Executed
- Failed

Never say an action was completed until the tool/API confirms success.

## Routing

Use the following internal routing:

- Performance/KPI question → `references/campaign-diagnosis.md`
- Competitor/ad-library question → `references/competitor-analysis.md`
- Creative/copy/video question → `references/creative-analysis.md`
- API/account action → `references/meta-marketing-api.md`
- Report request → `references/reporting.md`
- Safety/permission/write confirmation → `references/safety-and-confirmation.md`

Load only the relevant reference material needed for the current task.
