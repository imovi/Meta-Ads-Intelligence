# Campaign Diagnosis

Use this reference when the user asks why Meta Ads performance changed, which campaign/ad set/ad is best, what to optimize, or whether to scale.

## Diagnostic order

Do not jump straight to a recommendation. Follow:

1. Scope and objective
2. Date range
3. Primary business result
4. Spend and conversion volume
5. Efficiency metrics
6. Trend versus baseline
7. Campaign → Ad Set → Ad drill-down
8. Creative/audience/placement breakdowns where available
9. Tracking/data-quality checks
10. Diagnosis
11. Prioritized action plan

## Core metrics

Use the metrics relevant to the campaign objective:

- Spend
- Impressions
- Reach
- Frequency
- CPM
- Clicks
- CTR
- CPC
- Landing page views
- Leads
- Purchases
- Conversion rate
- CPA / cost per result
- Revenue
- ROAS

Do not treat every metric as equally important. Tie the analysis to the user's business objective.

## Baseline selection

Prefer a meaningful baseline:

- previous comparable period
- previous 7/14/30 days
- campaign historical average
- ad set average
- account average
- explicit business target

Keep date ranges comparable where possible.

## Common patterns

### High CPM

Investigate:

- audience competition
- creative relevance
- placement mix
- geography
- seasonality/auction conditions
- frequency

Do not automatically conclude that high CPM is bad; it depends on downstream conversion economics.

### High CPM + low CTR

Possible issue areas:

- weak hook
- poor creative relevance
- audience mismatch
- placement mismatch
- offer/message mismatch

### Good CTR + poor conversion rate

Investigate:

- landing page
- checkout flow
- offer
- product-market fit
- tracking
- message continuity between ad and landing page
- traffic quality

### Rising CPA

Compare:

- CPM
- CTR
- CPC
- conversion rate
- frequency
- spend/conversion volume

This helps isolate whether the deterioration is happening before the click or after the click.

### Rising frequency + falling CTR

Treat as a fatigue hypothesis. Check whether the same creative has been exposed repeatedly and whether newer creatives perform better.

### Good ROAS with very low spend

Mark as promising but low-confidence if conversion volume is small. Avoid aggressive scaling solely from a tiny sample.

### Good ad, weak campaign

Inspect:

- budget allocation
- ad set delivery
- audience overlap
- other ads consuming spend
- campaign objective/optimization
- placement mix

## Statistical humility

Do not call a winner just because one ad has a better percentage.

Consider:

- spend
- number of conversions
- impression volume
- time in market
- volatility
- attribution window

If evidence is insufficient, say "promising," "directionally better," or "insufficient data" instead of declaring a definitive winner.

## Scaling decision

Use three outcomes:

### Scale

Evidence is strong enough and performance is stable.

### Test before scaling

Performance is promising but sample size, stability, or creative diversity is insufficient.

### Do not scale

Performance is deteriorating, tracking is uncertain, or economics do not support more spend.

## Action recommendation format

```text
Finding:
Evidence:
Likely cause:
Recommended action:
Priority:
Confidence:
```

Keep observed evidence separate from hypotheses.
