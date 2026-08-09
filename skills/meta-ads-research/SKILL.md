---
name: meta-ads-research
description: Run a browser-first autonomous Meta Ads research workflow across public ads, competitor creatives, offers, messaging, public destination pages, patterns, gaps, and testable opportunities, while clearly separating observed evidence from inference.
metadata:
  origin: Meta-Ads-Intelligence
---

# Meta Ads Research

Use this skill for broad research requests where the user wants the agent to investigate a product, market, competitor set, or advertising opportunity rather than analyze only one supplied ad.

## Invocation

```text
/Meta-Ads-Intelligence research this market
/Meta-Ads-Intelligence research my competitors
/Meta-Ads-Intelligence find Meta ad opportunities for this product
```

## Research Principle

Prefer browser-based public research when browser access is available. Do not require an API token for public research when the browser can access the relevant public pages.

Never claim private competitor metrics from public ads.

## Workflow

### 1. Define Scope

Identify:

- product/category
- market/geography
- competitors
- customer segment
- research period when relevant
- decision the research should support

If critical scope is missing, make a reasonable public-research plan and state the assumption rather than inventing facts.

### 2. Public Ad Research

Use available browser access to inspect public ad surfaces such as Meta Ad Library and public brand pages.

Capture, when visible:

- advertiser
- ad status
- first/last seen dates when available
- format
- hook
- angle
- offer
- proof
- CTA
- copy themes
- visible creative structure
- destination URL when publicly visible

Record the source and distinguish `observed`, `inferred`, and `unknown`.

### 3. Creative Pattern Analysis

Group observed ads by:

- hook type
- angle
- format
- offer
- proof
- CTA
- message theme

Identify recurring patterns without calling them proven winners unless performance evidence is available.

### 4. Public Destination Research

When a public landing page is available, inspect:

- headline
- offer
- pricing presentation
- proof
- CTA
- product positioning
- message match with the ad

Do not attempt to access private dashboards or restricted data.

### 5. Competitor Comparison

Compare competitors on observed public behavior:

| Dimension | Competitor A | Competitor B | Competitor C |
|---|---|---|---|
| Formats | | | |
| Hooks | | | |
| Angles | | | |
| Offers | | | |
| Proof | | | |
| CTA | | | |

### 6. Opportunity Detection

Look for:

- overused market patterns
- under-observed angles
- positioning differences
- offer gaps
- format gaps
- message gaps
- audience/problem opportunities

Use language such as:

> “Not observed in this sample; worth testing.”

Never say:

> “No competitor does this.”

unless the research scope actually supports that claim.

### 7. Creative Opportunities

Generate original test hypotheses from the research.

Do not copy competitor ads verbatim, reuse their testimonials, or imitate protected branding/identity.

### 8. Final Report

Return:

1. Executive summary
2. Research scope
3. Competitors researched
4. Public evidence
5. Creative patterns
6. Offer/messaging patterns
7. Destination-page observations
8. Market saturation
9. Opportunity gaps
10. Recommended creative tests
11. Confidence
12. Limitations

## Browser Rules

- Use the existing authenticated browser session when available.
- Do not ask the user to paste passwords, cookies, session tokens, or 2FA codes.
- Do not navigate into private competitor accounts.
- Public research remains read-only.

## Action Boundary

Research does not authorize publishing ads, changing budgets, pausing campaigns, editing targeting, or modifying an account.

If the user asks to execute a recommendation, switch to the explicit Action workflow.
