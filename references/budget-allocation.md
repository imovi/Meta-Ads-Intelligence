# Budget Allocation Simulator

Use this module for planning and scenario analysis only.

## Inputs

- total available daily budget
- campaign performance
- target CPA and/or target ROAS when known
- conversion volume
- creative fatigue signals
- test budget percentage

## Recommendation classes

- **Scale** — target efficiency is met with meaningful conversion volume
- **Hold** — insufficient evidence for a material change
- **Reduce** — efficiency is materially below the stated target with enough conversion volume to judge
- **Test** — insufficient evidence or fatigue suggests experimentation

## Simulation

The simulator allocates budget directionally using evidence-weighted performance. It is not a forecast and does not guarantee future results.

A small testing pool is reserved so the account can continue learning rather than allocating 100% of budget to existing winners.

## Example

For a $1,000/day planning scenario:

- $900 deployment pool
- $100 testing pool
- scale campaigns receive more weight when both efficiency and conversion volume support scaling
- hold campaigns retain budget according to evidence
- test campaigns share the testing pool
- reduce campaigns receive no proposed incremental budget in this scenario

## Safety

This module never changes a real campaign budget. A user must explicitly request an account action, and the Action Guard must validate the exact campaign, current budget, proposed budget, authorization, and confirmation before any write.

## Limitations

Do not treat the simulation as a financial guarantee. Consider attribution changes, learning phase, audience overlap, auction conditions, creative fatigue, seasonality, and business constraints before acting.
