---
name: meta-ads-audit
description: Run a read-only account-level Meta Ads health audit across campaigns and available ad data, prioritizing performance, tracking, creative, strategy, fatigue, and risk findings into a directional health score and fix plan.
metadata:
  origin: Meta-Ads-Intelligence
---

# Meta Ads Account Audit

## Invocation

```text
/Meta-Ads-Intelligence audit my account
/Meta-Ads-Intelligence run a full account audit
/Meta-Ads-Intelligence find the biggest problems in my Meta Ads account
```

## Scope

Audit available account data across:

- campaign performance
- conversion volume
- CPA and ROAS vs targets
- trend/anomaly signals
- tracking warnings
- creative completeness/fatigue signals
- strategy/scaling readiness
- budget and delivery context when available

## Browser-first

If browser/computer-use access is available and the user requests browser analysis:

1. Use the existing authenticated Ads Manager session.
2. Identify the account and selected date range.
3. Collect the minimum required visible data.
4. Compare with an appropriate prior period when available.
5. Feed observations into the audit modules.

Do not request passwords, cookies, session tokens, or 2FA codes.

## Health Score

Provide a directional health score with a clear disclaimer that it is an internal decision-support score, not a Meta platform score.

Suggested labels:

- `healthy`
- `needs_attention`
- `at_risk`
- `critical`

The score must never hide the underlying findings.

## Prioritization

Each issue should have:

- severity
- affected object
- evidence
- likely area to investigate
- recommended next step
- confidence/limitations when material

Prioritize issues that can materially affect spend, conversions, tracking accuracy, or creative performance.

## Output

```text
ACCOUNT HEALTH: 72/100 — NEEDS ATTENTION

Top issues
1. ...
2. ...
3. ...

What is working
- ...

What needs attention
- ...

Fix plan
P0 — ...
P1 — ...
P2 — ...

Evidence / limitations
- ...
```

## Safety

Audit is read-only. It does not pause campaigns, edit budgets, change targeting, publish creatives, or otherwise modify the account.

If the user asks to execute a fix, switch to the explicit Action workflow and follow confirmation/verification requirements.
