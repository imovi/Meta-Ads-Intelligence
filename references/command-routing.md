# Natural-Language Command Routing

Use this reference to map ordinary user requests to the correct Meta Ads Intelligence mode.

## Available modes

- **analyze** — performance/KPI questions and diagnosis
- **audit** — full account health audit
- **competitor** — public competitor/ad-library research
- **creative** — copy, image, video, Reel and hook analysis
- **strategy** — optimization, scaling, budget allocation and next-step planning
- **report** — daily/weekly/monthly reporting
- **monitor** — anomaly checks and alerts
- **action** — explicit account-changing requests

## Routing examples

| User request | Mode |
|---|---|
| "Why is my CPA high?" | analyze |
| "Check my ads" | analyze |
| "Audit my whole ad account" | audit |
| "Analyze my competitor's ads" | competitor |
| "Break down this Reel ad" | creative |
| "Should I scale this campaign?" | strategy |
| "Give me a weekly report" | report |
| "Watch my ROAS and alert me if it drops" | monitor |
| "Pause campaign ABC" | action |
| "Increase campaign ABC to $100/day" | action |

## Ambiguity rule

If the request could be interpreted as either analysis or action, choose analysis and ask a concise clarification if needed.

Examples:

> "What should I do with campaign ABC?"

Route to strategy, not action.

> "Can you change campaign ABC?"

The user has expressed an action-oriented intent, but the exact change is unclear. Ask what change they want before executing anything.

## Action safety

The presence of an action verb is not enough to invent missing parameters.

Before an account-changing operation, identify:

- account
- target object
- exact operation
- current state
- requested state
- expected impact

Then follow the Action Guard and confirmation policy.

## Mixed requests

A user may combine analysis and action:

> "Analyze these campaigns and pause anything that is clearly losing money."

First analyze. Then produce the proposed list of changes. Do not automatically execute the resulting list unless the action policy and available authorization support it; consequential changes should be explicitly confirmed.

## Safe default

When intent is uncertain, do not write to the Meta account. Default to analysis.
