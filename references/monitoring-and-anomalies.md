# Monitoring & Anomaly Detection

Use this reference when checking whether Meta Ads performance has changed materially.

## Purpose

Monitoring should surface **signals**, not pretend to know causation.

Compare the current period with a comparable baseline whenever possible.

## Signals to monitor

- CPA increase
- ROAS decrease
- CTR decrease
- CPM increase
- frequency increase
- conversion decrease
- unusual spend movement
- data-integrity inconsistencies

## Thresholds

Default screening thresholds are configurable. A 25% relative movement can be used as a starting point, but it is not a universal definition of an anomaly.

For CTR, use an absolute percentage-point movement as well as relative movement when appropriate.

Always consider:

- spend volume
- conversion volume
- campaign launch/learning changes
- attribution window/settings
- seasonality
- audience size
- placement changes
- creative changes
- tracking changes

## Anomaly language

Prefer:

> CPA increased 32% versus the previous comparable period. This is a screening signal; investigate delivery, audience, creative, conversion rate, and tracking before attributing the cause.

Avoid:

> CPA increased because the audience is bad.

The second statement is causal and unsupported without additional evidence.

## Tracking/data integrity

Flag impossible or suspicious relationships such as:

- negative spend
- negative conversions
- negative revenue without an understood adjustment/refund context
- clicks greater than impressions

These are validation warnings, not automatic proof that the API data is wrong.

## Alert priority

### Critical

Potential tracking break, conversions collapsing with meaningful spend, or severe business-impact movement.

### High

Material CPA/ROAS movement or multiple correlated signals.

### Medium

Single meaningful KPI movement requiring investigation.

### Low

Small movement or weak evidence worth watching.

## Monitoring output

Each alert should contain:

- metric
- current value
- baseline value
- change
- signal type
- confidence
- likely investigation areas
- recommended next step

Never execute an account change from an anomaly alert automatically unless a separate, explicitly authorized automation policy exists.
