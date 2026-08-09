# Reporting

Use this reference to turn Meta Ads data and the other intelligence modules into concise decision-ready reports.

## Report types

### Daily

Focus on anomalies and urgent changes:

- spend
- conversions
- CPA/ROAS
- major KPI movement
- delivery/tracking issues
- actions requiring attention

### Weekly

Focus on decisions:

1. Executive summary
2. KPI snapshot
3. Period-over-period change
4. Best performers
5. Weakest performers
6. Creative findings
7. Competitor observations
8. Problems and likely causes
9. Recommended actions
10. Next 7-day plan

### Monthly

Focus on trends and strategy:

- month-over-month performance
- account/campaign contribution
- creative fatigue
- audience/placement patterns when available
- offer/positioning insights
- budget allocation
- strategic tests for the next month

## Standard report structure

```text
# Meta Ads Report

Date range:
Account:
Objective:

## Executive Summary
## KPI Overview
## Best Performers
## Weakest Performers
## Change vs Baseline
## Diagnosis
## Recommended Actions
## Risks / Data Limitations
```

## KPI rules

Prefer aggregate metrics calculated from totals rather than averaging row-level ratios when appropriate.

For example:

- CTR = total clicks / total impressions
- CPC = total spend / total clicks
- CPA = total spend / total conversions
- ROAS = total revenue / total spend
- CPM = total spend / total impressions × 1,000

Always state the date range and data scope.

## Comparison

When a previous period is supplied, show both absolute and percentage change where meaningful.

Avoid misleading comparisons when:

- date ranges have different lengths
- attribution settings changed
- conversion tracking changed
- campaigns were launched/paused during only one period
- spend volume is materially different

## Top performers

A top performer should not be selected from a single metric without considering spend and conversion volume. Flag small-sample winners.

## Client-ready writing

Lead with:

- what happened
- why it likely happened
- what should happen next

Avoid dumping every available metric into the executive summary.

## Recommendations

Prioritize actions:

### High
Likely to materially affect business performance.

### Medium
Useful optimization or test.

### Low
Nice-to-have improvement.

Each recommendation should include evidence and confidence when possible.

## Competitor report

For competitor research use:

- competitors reviewed
- observed ad count/presence where available
- recurring creative angles
- offer patterns
- messaging patterns
- creative formats
- market gaps
- original opportunities
- unknown/private metrics

Never report estimated competitor ROAS or spend as fact.

## Trend reporting

When historical data exists, show:

- current period
- previous comparable period
- absolute change
- percentage change
- likely explanation

Call out data-quality issues before drawing strong conclusions.

## Data integrity

Clearly distinguish:

- calculated metrics
- API-provided metrics
- user-provided data
- public competitor observations
- model inference

Never fabricate missing values.
