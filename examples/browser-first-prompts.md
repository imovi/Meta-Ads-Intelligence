# Browser-First Usage Examples

These examples are intended to work with a host that exposes browser/computer-use access, such as Claude in Chrome.

## Analysis

> Open my Meta Ads Manager in the browser and analyze yesterday's campaigns. Don't ask me for an API token. Use the already logged-in browser session. Give me the top 5 problems and what I should test next.

Expected behavior:

- use browser access if available
- inspect the visible account and date range
- collect relevant metrics
- run analysis modules
- do not change the account

## Full account audit

> Use my logged-in Meta Ads Manager browser session and run a full account audit for the last 7 days. Check campaigns, ad sets, ads, creatives, CPA, ROAS, CTR, CPM, frequency, anomalies, and budget allocation. Don't make any changes.

## Competitor research

> Open Meta Ad Library in the browser and analyze the active ads for [brand]. Break down hooks, offers, angles, formats, CTAs, proof, and recurring creative patterns. Only report what you can observe publicly.

## Creative analysis

> Open the ads in my Meta Ads Manager and compare the active creatives. Tell me which hooks and angles are performing best based on the visible performance data. Flag small samples.

## Action

> Analyze campaign ABC first. If I explicitly approve the proposed change, increase its daily budget from the current value to $100/day.

Expected behavior:

1. analyze first
2. read current state
3. propose exact change
4. ask for confirmation
5. only then perform the browser action
6. verify the resulting state

## Important

The Skill cannot create browser access by itself. Claude/Claude in Chrome (or another host) must provide the browser/computer-use capability and the user must already have the necessary access in that browser session. Anthropic describes Claude in Chrome as a browser agent that can navigate websites and complete tasks in the user's Chrome browser. citeturn0search7
