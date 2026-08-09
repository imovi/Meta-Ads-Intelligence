---
name: meta-ads-monitor
description: Monitor Meta Ads performance for material anomalies such as ROAS drops, CPA spikes, CTR declines, spend spikes, conversion drops, and creative fatigue, using browser-observed or supplied time-series data and remaining read-only.
metadata:
  origin: Meta-Ads-Intelligence
---

# Meta Ads Monitoring

Use this skill when the user asks to monitor an account/campaign, detect anomalies, watch ROAS/CPA, or identify meaningful performance changes.

## Invocation

```text
/Meta-Ads-Intelligence monitor my account
/Meta-Ads-Intelligence watch my ROAS and CPA
/Meta-Ads-Intelligence check for anomalies
```

## Browser-first

When browser access is available and requested:

1. Open/use the existing logged-in Ads Manager session.
2. Read the requested date range and comparison period.
3. Collect only the metrics needed for monitoring.
4. Record source and timestamp/context when available.
5. Compare like-for-like periods.

Do not ask for passwords, cookies, session tokens, or 2FA codes.

## Alerts

Monitor meaningful changes in:

- ROAS
- CPA
- CTR
- spend
- conversions
- frequency
- creative fatigue

Prioritize alerts:

- **Critical** — material ROAS or conversion deterioration
- **High** — material CPA/CTR deterioration or strong fatigue signal
- **Medium** — unusual spend movement or weaker secondary signal

Thresholds are configurable. Do not present them as universal industry standards.

## Multi-signal diagnosis

An alert is a prompt to investigate, not proof of cause.

For example, a CPA spike may be caused by:

- conversion tracking changes
- attribution changes
- audience/delivery changes
- placement mix
- creative fatigue
- offer/landing-page changes
- auction conditions

Check context before recommending action.

## Output

```text
Status
Highest priority alert
What changed
Magnitude
Likely areas to investigate
Evidence
Recommended next check
```

If there are no material alerts, say so and provide the comparison period used.

## Action Boundary

Monitoring is read-only. Never automatically pause ads, change budgets, edit targeting, or publish creatives because an alert fired.

If the user explicitly asks for a change, route to the Action workflow and verify the exact requested change.
