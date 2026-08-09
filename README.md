# Meta Ads Intelligence

A portable, analysis-first skill for Facebook and Instagram advertising.

## What it does

Meta Ads Intelligence helps an AI agent:

- analyze Meta Ads performance
- diagnose campaign, ad set, and ad problems
- compare creatives
- detect fatigue and anomalies
- recommend budget/scaling decisions
- analyze public competitor ads
- break down hooks, offers, messaging, and CTAs
- generate decision-oriented reports
- perform account actions when the user explicitly asks and the environment has the required Meta API/tool access

## Operating model

**Analysis is the default. Actions require explicit intent.**

For example:

> Analyze my campaign

stays read-only.

But:

> Pause this campaign

can enter action mode, subject to access and confirmation rules.

## Repository structure

```text
Meta-Ads-Intelligence/
├── SKILL.md
├── README.md
├── references/
│   ├── meta-marketing-api.md
│   ├── campaign-diagnosis.md
│   ├── competitor-analysis.md
│   ├── creative-analysis.md
│   ├── reporting.md
│   └── safety-and-confirmation.md
├── scripts/
├── schemas/
├── examples/
└── evals/
```

## Data sources

The skill can work with:

- live Meta Marketing API/connector data when actually connected
- Ads Manager exports
- screenshots and reports supplied by the user
- public competitor/ad-library information

It must never pretend to have live access when no connection exists.

## Competitor analysis boundary

Public competitor research is observational. The skill must not present a competitor's private spend, CPA, ROAS, revenue, exact targeting, or conversion results as known facts unless reliable evidence is supplied.

## Action safety

Consequential changes such as publishing, deleting, budget increases, pausing, targeting changes, and creative replacement are handled through an explicit proposal/confirmation workflow.

## Portability

The core skill is platform-agnostic. The repository separates reasoning instructions from API/tool adapters so it can be adapted to Claude Code, agentic IDEs, and other compatible skill systems without embedding credentials or vendor-specific secrets.

## Status

Early development — core routing, analysis rules, competitor intelligence, reporting, API guidance, and action-safety rules are implemented. Tool adapters, reusable analysis scripts, schemas, examples, and evaluation cases are added incrementally.
