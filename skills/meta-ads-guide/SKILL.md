---
name: meta-ads-guide
description: Guide users through the current Meta Ads Intelligence skills, modes, browser workflows, analysis modules, reports, monitoring, and safe action boundaries by reading the live repository surface before answering.
metadata:
  origin: Meta-Ads-Intelligence
---

# Meta Ads Intelligence Guide

Use this skill when the user wants to understand what Meta Ads Intelligence can do, which workflow to use, how to invoke it, or how analysis and action modes differ.

## Core Principle

Answer from the current repository surface, not memory. The project evolves frequently, so inspect relevant `SKILL.md`, references, examples, and scripts before making concrete claims about available capabilities.

## Primary Invocation

The canonical user-facing invocation is:

```text
/Meta-Ads-Intelligence <request>
```

Examples:

```text
/Meta-Ads-Intelligence use my browser and analyze this ad
/Meta-Ads-Intelligence audit my account
/Meta-Ads-Intelligence find my winning creatives
/Meta-Ads-Intelligence check creative fatigue
/Meta-Ads-Intelligence analyze my competitors
/Meta-Ads-Intelligence create A/B tests from my winners
/Meta-Ads-Intelligence should I scale this campaign?
/Meta-Ads-Intelligence make a weekly report
```

## Mode Selection

Route requests to the narrowest appropriate mode:

- `analyze` — performance/KPI diagnosis
- `audit` — full account audit
- `competitor` — public competitor research
- `creative` — ad/creative analysis and generation
- `strategy` — optimization/scaling/budget planning
- `report` — reporting and summaries
- `monitor` — anomaly/fatigue monitoring
- `action` — explicit account-changing request

When intent is ambiguous, default to analysis rather than changing an account.

## Browser-First Analysis

When browser access is available and the user asks to use the browser:

1. Use the existing authenticated browser session.
2. Do not ask the user to paste passwords, cookies, session tokens, or 2FA codes.
3. If the relevant Meta Ads page is already open, use the current page as the starting context.
4. Record the source as browser-observed data.
5. Separate observed facts from inferences and unknowns.
6. Do not make account changes during analysis.

Browser capability depends on the host agent. This skill defines the workflow; it does not grant browser permissions itself.

## Analysis Modules

Before claiming a module is available, inspect the repository. Relevant modules may include:

- browser vision
- deep ad analysis
- winning creative detection
- creative fatigue
- controlled creative testing
- competitor intelligence
- budget allocation
- scaling intelligence
- account audit
- anomaly detection
- reporting

## Action Boundary

Analysis is read-only by default.

An explicit action request must identify the target and requested operation. Do not invent missing parameters. Before a consequential write:

1. identify account
2. identify target object
3. read current state
4. describe proposed change
5. obtain required confirmation/authorization
6. execute through the approved action layer
7. re-read the UI/API state and verify the result

## Response Style

Lead with the answer and give the next concrete command. Avoid dumping the entire module catalog unless requested.

### Short Recommendation

```text
Use <mode/module>. It fits because <reason>.

Invoke: /Meta-Ads-Intelligence <request>
```

### Capability Discovery

```text
Best fit: <module>
Why: <reason>
Browser needed: <yes/no>
Action required: <yes/no>
Next: /Meta-Ads-Intelligence <request>
```

## Safety and Evidence

Never present private competitor performance as known from public ads. Never fabricate missing metrics. For browser-observed data, preserve the distinction between visible evidence and inference.

## Related Skills

- `meta-ads-scout` — search existing skills/modules and inspect the repository before adding new functionality.
