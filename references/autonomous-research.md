# Autonomous Research

This workflow turns a broad request into a structured public research pass.

## Example

User:

> `/Meta-Ads-Intelligence research the skincare market in Malaysia and find Meta ad opportunities.`

The agent should:

1. define the research scope
2. identify relevant competitors/public advertisers
3. inspect public Meta ads
4. capture creative/offer/message patterns
5. inspect public destination pages
6. compare recurring patterns
7. identify gaps in the observed sample
8. generate original creative hypotheses
9. produce a report with evidence and limitations

## Evidence discipline

### Observed

Directly visible on a public page or supplied by the user.

### Inferred

A reasoned interpretation from observed evidence.

### Unknown

Not supported by available evidence.

## Public competitor boundaries

Do not infer private:

- spend
- CPA
- ROAS
- conversion volume
- targeting
- audience lists
- internal account structure

Public ad longevity can be an observable signal when first/last-seen information is available, but it is not proof of profitability.

## Opportunity language

Prefer:

> “This angle was not observed in the captured sample and could be tested.”

Avoid:

> “The market does not use this angle.”

## Browser failure

If browser access is unavailable, report that limitation and continue with user-supplied/publicly accessible data that the environment can legitimately access. Never pretend to have browsed pages that were not actually observed.
