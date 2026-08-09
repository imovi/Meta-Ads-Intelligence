# Account Audit

Use this reference when the user asks for a full Meta Ads account audit.

## Scope

An account audit should inspect available data across:

- account
- campaigns
- ad sets
- ads
- creatives
- performance metrics
- tracking/data integrity
- anomalies
- budget allocation
- creative fatigue signals
- competitor context when supplied

If some layers are unavailable, state exactly what was not audited.

## Audit workflow

1. Confirm account and date range.
2. Load campaign/ad set/ad structure.
3. Calculate aggregate KPIs.
4. Evaluate health against user targets or a defensible baseline.
5. Check data integrity and tracking warnings.
6. Check anomaly signals.
7. Check creative completeness/fatigue signals.
8. Rank objects by priority.
9. Produce top findings.
10. Produce recommended tests/actions.
11. Keep all account changes behind the explicit ACTION workflow.

## Health score

A directional score may summarize the audit, but it must never be presented as a Meta account-quality metric.

The detailed findings are more important than the score.

Suggested labels:

- healthy
- needs_attention
- at_risk
- critical

If data for a dimension is unavailable, mark it unknown instead of inventing a negative finding.

## Priority

### High / P0

Likely material business impact, tracking concern, or severe performance issue.

### Medium / P1

Meaningful optimization opportunity with reasonable evidence.

### Low / P2

Monitoring or incremental improvement.

## Evidence discipline

Separate:

- **Observed** — directly visible or supplied.
- **Inferred** — reasoned interpretation.
- **Unknown** — not supported by available data.

Do not infer causality from a single metric.

## Output

### Account Health

- Date range:
- Objects audited:
- Overall directional score:
- Main risk:
- Main opportunity:

### Top Findings

| Priority | Object | Finding | Evidence | Recommendation |
|---|---|---|---|---|

### Structure

Summarize campaign → ad set → ad relationships and identify concentration or weak spots.

### Performance

Show spend, conversions, CPA, ROAS, CTR, CPM and other relevant metrics when available.

### Creative

Identify strongest observable creative patterns and fatigue signals.

### Tracking/Data Quality

List warnings separately from performance findings.

### Next Steps

Give the top 3–7 actions/tests, ordered by impact and confidence.

## Action boundary

An audit is analysis. It does not authorize pausing, deleting, publishing, changing budgets, or modifying targeting. If the user asks to execute a recommendation, switch to ACTION mode and follow the confirmation guard.
