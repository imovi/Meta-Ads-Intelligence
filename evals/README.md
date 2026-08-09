# Evaluation Suite

The eval suite checks the most important behavioral contracts of Meta Ads Intelligence.

## What is covered

- KPI/performance diagnosis
- evidence-aware winner selection
- competitor private-metric boundaries
- analysis vs action routing
- consequential-action confirmation
- creative analysis
- fatigue diagnosis
- reporting quality

## How to use

Run each prompt against the skill in an environment that supports the skill, then inspect the output against the assertions in `evals.json`.

For stronger evaluation, run each case:

1. With the current skill.
2. Against a baseline without the skill, where practical.
3. With identical inputs and date ranges.
4. With human review for subjective creative/report quality.

## Important behavioral contracts

### Analysis-first

A request to analyze, inspect, compare, or recommend must not silently modify an ad account.

### Explicit action

A direct request to pause, publish, change budget, delete, or otherwise modify an account may enter action mode, but consequential changes require the safety/confirmation workflow.

### Competitor boundaries

Public competitor information is observational. Private spend, CPA, ROAS, conversion volume, and exact targeting must not be fabricated.

### Evidence quality

A better percentage on a tiny sample is not automatically a winner. The agent should consider spend, conversion volume, time, and the user's primary business KPI.
