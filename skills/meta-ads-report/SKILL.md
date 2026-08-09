---
name: meta-ads-report
description: Create client-facing and executive Meta Ads reports from supplied or browser-observed evidence, with KPI snapshots, wins, problems, recommendations, next-7-day priorities, and clear source/limitation notes.
metadata:
  origin: Meta-Ads-Intelligence
---

# Meta Ads Client Reporting

Use this skill when the user asks for a client report, weekly report, executive summary, performance report, or presentation-ready Meta Ads summary.

## Invocation

```text
/Meta-Ads-Intelligence make a client report
/Meta-Ads-Intelligence make a weekly report
/Meta-Ads-Intelligence summarize this account for my client
```

## Source

Prefer current browser-observed Ads Manager data when browser access is available and the user asks to use the browser. Otherwise use the supplied export/API-shaped dataset.

Always state the data source and reporting period when known.

## Report Structure

1. Executive Summary
2. KPI Snapshot
3. What Worked
4. What Needs Attention
5. Campaign/Creative Highlights
6. Recommendations
7. Next 7 Days
8. Evidence & Limitations

## KPI Rules

Calculate aggregate ratio metrics from aggregate totals where possible:

- ROAS = total revenue / total spend
- CPA = total spend / total conversions
- CTR = total clicks / total impressions

Do not average row-level CPA/ROAS/CTR when totals are available.

## Executive Summary

Write for a business stakeholder. Explain:

- what changed
- why it matters
- what is working
- what needs attention
- what should happen next

Avoid unexplained platform jargon.

## Recommendations

Prioritize recommendations by business impact and evidence strength.

Separate:

- observation
- interpretation
- recommendation

Do not imply an action was executed unless it actually was.

## Next 7 Days

Provide a practical prioritized plan, for example:

- protect current winners
- refresh fatigued creatives
- launch controlled tests
- review budget allocation
- verify tracking/attribution
- re-check performance after sufficient data

## Client Tone

Use concise, professional language. Avoid overwhelming clients with every available metric. Put supporting technical detail below the executive summary.

## Action Boundary

A report is read-only. Creating a report does not change campaigns, budgets, targeting, creatives, or account settings.
