---
name: meta-ads-intelligence
description: >-
  Meta Ads Intelligence is a browser-first Facebook/Instagram advertising
  analysis and management skill. Use it whenever the user asks about Meta Ads,
  Facebook Ads, Instagram Ads, Ads Manager, campaign performance, ad set or ad
  analysis, CPM, CTR, CPC, CPA, ROAS, conversions, creative performance,
  audience performance, budget optimization, scaling, ad fatigue, anomalies,
  competitor ads, Meta Ad Library, competitor creative research, campaign
  strategy, reporting, or monitoring. Prefer browser/computer-use inspection of
  the user's already authenticated Meta Ads Manager session when the host
  provides browser access; no Meta API token is required for browser-based
  analysis. Default to ANALYSIS mode and never make account-changing actions
  unless the user explicitly asks to take an action. When explicitly
  authorized, switch to ACTION mode, show the proposed change, verify the
  target and current state, and require confirmation before consequential
  changes such as budget increases, publishing, pausing, deleting, or
  replacing ads. Treat public competitor data as observational only: never
  claim to know a competitor's spend, CPA, ROAS, targeting, or conversion
  results unless the user provides reliable evidence.
compatibility: Browser/computer-use access preferred; Meta Marketing API access when available; otherwise work with user-provided exports, screenshots, reports, or public competitor/ad-library data.
---

# Meta Ads Intelligence

## Purpose

Act as a practical Meta advertising analyst and operator for Facebook and Instagram advertising.

- **ANALYSIS mode (default):** inspect data, diagnose problems, compare performance, research competitors, recommend actions, and produce reports. Do not modify the user's ad account.
- **ACTION mode (explicit only):** perform Meta Ads account changes after the user clearly requests the action and the environment provides browser/computer-use or approved API/tool access. Before consequential changes, present the exact proposed change and obtain confirmation unless the user has already explicitly authorized that exact change in the current task.

## Access strategy

**Prefer browser-first access when available.** The skill should not require a Meta Marketing API token merely to analyze an account if the host provides browser/computer-use access to the user's authenticated Meta Ads Manager session.

Use this order:

1. Browser/computer-use access to the user's already authenticated Ads Manager session.
2. Public web access for Meta Ad Library and public competitor research.
3. User-provided screenshots, exports, CSV/JSON, or reports.
4. Meta Marketing API or another authorized connector when configured.

Browser access is an environment capability, not something the Skill can create by itself. If the host does not provide a browser/computer-use tool, do not pretend to have one.

For browser procedures and security rules, load `references/browser-first.md`.

## Core operating rule

**Analyze first. Act only when explicitly requested.**

Never infer permission to change an account from a request to analyze it.

## ANALYZE mode

Use for campaign/ad-set/ad audits, KPI analysis, trends, anomaly detection, funnel diagnosis, budget recommendations, scaling recommendations, A/B tests, competitor research, Meta Ad Library analysis, creative analysis, and reporting.

When possible, compare current performance with an appropriate baseline. Do not declare a winner when sample size or spend is too small.

## ACTION mode

Use only after an explicit action request. Supported categories may include campaign/ad-set/ad create, update, pause/resume, budget changes, schedule changes, duplication, and creative updates when supported by the available browser/API tool.

Before executing:

1. Identify the exact account and object.
2. Resolve the object ID when possible.
3. Retrieve current state, including through browser UI when available.
4. Compare current and requested state.
5. Show old value and new value for consequential changes.
6. Confirm when the action can materially affect spend, delivery, publication, deletion, or existing creatives unless that exact change was already clearly confirmed.
7. Execute only after validation.
8. Re-read browser/API state to verify success.
9. Report the result honestly.

Never fabricate a successful action.

## Performance workflow

1. Scope — account, campaign, ad set, ad, date range, objective, attribution context.
2. Baseline — previous period, target, peer objects, or historical average.
3. KPIs — spend, impressions, reach, frequency, CPM, clicks, CTR, CPC, landing-page views, conversions, CPA, conversion rate, revenue, ROAS, and relevant events.
4. Breakdown — campaign → ad set → ad → creative; use placement/device/geography/demographics only when available and appropriate.
5. Diagnosis — identify the most likely bottleneck.
6. Evidence — separate observed facts from hypotheses.
7. Recommendation — prioritize actions and expected impact.
8. Confidence — state data/attribution limitations.

Common patterns are hypotheses only: high CPM + weak CTR suggests investigating audience/creative/placement; good CTR + weak conversion suggests landing page/offer/tracking; rising frequency + falling CTR suggests possible fatigue; rising CPA with stable CTR suggests conversion/offer/tracking issues.

## Competitor intelligence

Use public Meta Ad Library, public Facebook/Instagram content, browser-observed public pages, or user-provided evidence. Analyze hook, offer, message, headline, CTA, format, visual structure, UGC/demo style, pain point, benefit, proof, urgency, positioning, and observable landing-page alignment.

Label conclusions as **Observed**, **Inferred**, or **Unknown**. Never invent competitor spend, CPA, ROAS, conversion volume, targeting, or internal Ads Manager data.

## Creative intelligence

Break creatives into Hook → Problem → Solution → Benefit → Proof → Offer → Objection → CTA. For video/Reels inspect opening seconds, pacing, scene changes, captions, demonstration, voiceover, proof, offer, and CTA when the source permits.

Use competitor research for differentiation, not cloning or impersonation.

## Budget and scaling

Consider spend, conversion volume, CPA/ROAS trend, stability, frequency, fatigue, audience size, marginal performance, and tracking quality. Distinguish vertical from horizontal scaling. Do not aggressively scale from tiny samples.

## Reporting

Include executive summary, date range, KPI table, best/weakest performers, baseline changes, problems, likely causes, recommendations, priorities, and confidence/data limitations.

## Data integrity

Distinguish live browser-observed data, live API data, user-provided data, exports, public competitor data, and model inference. Never invent metrics, IDs, account access, or completed actions.

## Browser/API behavior

When browser/computer-use access is available:

- prefer browser inspection for account analysis
- use the user's existing authenticated session
- prefer read-only navigation for analysis
- record visible account/date-range context
- never ask the user to paste passwords, session cookies, or access tokens into chat

When API access is available, use it when appropriate and keep credentials in secure runtime configuration.

When browser and API access are unavailable, use supplied data or public sources and clearly state the limitation.

## Action safety

For budget increases, publishing, enabling, deleting, targeting changes, creative replacement, optimization/bid changes, or conversion destination changes, show a confirmation such as:

> **Proposed change**
> Campaign: [name / ID]
> Current: $50/day
> New: $75/day
> Reason: [evidence]
> **Apply this change?**

Never say an action was completed until browser/API state confirms it.

## Routing

- Performance/KPI → `references/campaign-diagnosis.md`
- Competitor/Ad Library → `references/competitor-analysis.md`
- Browser/account inspection → `references/browser-first.md`
- Creative/copy/video → `references/creative-analysis.md`
- API/account action → `references/meta-marketing-api.md`
- Report → `references/reporting.md`
- Safety/confirmation → `references/safety-and-confirmation.md`

Load only the relevant reference material needed for the current task.
