# Meta Marketing API Reference

This reference covers how Meta Ads Intelligence should reason about live Meta account data and account-changing operations.

## Scope

Use the Meta Marketing API when a supported connector, MCP server, local integration, or API client is actually available and authenticated.

The current official Meta Postman workspace demonstrates the main Marketing API data model and workflows for Campaigns, Ad Sets, Ad Creatives, Ads, and Insights. It also shows retrieval of account, campaign, ad set, and ad information. citeturn0search0turn0search8

Do not hardcode a specific Graph API version into the skill's general reasoning. The integration layer should determine the currently supported API version.

## Data hierarchy

Think in this hierarchy:

```text
Ad Account
  └── Campaign
       └── Ad Set
            └── Ad
                 └── Creative
```

An Ad Set groups ads that share budget/schedule/bid/targeting characteristics. Meta's current official collection documents this relationship. citeturn0search2turn0search5

## Read operations

For analysis, prefer read-only operations such as:

- account details
- campaign list/details
- ad set list/details
- ad list/details
- creative details
- insights
- relevant breakdowns

Official examples show campaign, ad set, and ad-level Insights requests and fields such as impressions, clicks, spend, reach, frequency, CTR, CPC, CPM, actions, action values, and conversion-related fields. citeturn0search1turn0search3turn0search6

## Insight collection

When requesting insights:

1. Resolve the object and account scope.
2. Define the exact date range.
3. Request only the metrics needed for the question.
4. Add breakdowns only when they answer a specific question.
5. Preserve the currency and attribution/reporting context.
6. Handle pagination and API limits.
7. Record the source and retrieval time when practical.

Do not mix incompatible breakdowns or dimensions without checking API support.

## Recommended analysis fields

For a general performance audit, consider:

- date_start/date_stop
- account_id/account_name
- campaign_id/campaign_name
- adset_id/adset_name
- ad_id/ad_name
- impressions
- reach
- frequency
- clicks
- outbound clicks
- unique outbound clicks
- spend
- CPM
- CPC
- CTR
- actions
- action_values
- conversions
- conversion_values
- cost per result/action where available
- video metrics when relevant

The exact field availability depends on the API version, object, attribution/reporting setup, and request.

## Write operations

Write operations include creating or editing campaign, ad set, creative, and ad objects. Meta's current official collection demonstrates campaign creation, ad set creation, creative creation, and ad creation workflows. citeturn0search8

Never execute a write simply because the user asked for analysis.

Before a consequential write:

- resolve the exact object
- fetch current state if possible
- validate the requested change
- show old and new values
- obtain confirmation when required by the core skill rules
- execute
- verify the returned state

## Action examples

### Budget change

```text
Target: Campaign ABC / ID 123
Current daily budget: $50
Requested daily budget: $75
Reason: CPA and conversion volume remain stable over the selected period.
Status: Awaiting confirmation
```

### Pause

```text
Target: Ad XYZ / ID 456
Current status: ACTIVE
Requested status: PAUSED
Reason: CPA is materially above the user's threshold.
Status: Awaiting confirmation
```

## Authentication and secrets

Never place access tokens, app secrets, client secrets, or long-lived credentials in:

- SKILL.md
- README.md
- source files
- examples
- Git commits
- chat output
- logs

Use the environment's secure secret mechanism.

The official Meta collection requires an account ID and token for its examples and points developers to Meta's authentication documentation. citeturn0search0

## No-live-access fallback

If API access is unavailable:

- ask the user for an Ads Manager export, screenshot, or relevant data
- analyze the supplied data
- clearly state that the analysis is not live
- do not invent API responses

## Important distinction

The Marketing API can expose the user's authorized advertising data. It does not magically expose a competitor's private Ads Manager metrics.

Competitor research belongs in `competitor-analysis.md` and should use public sources or user-provided evidence.
