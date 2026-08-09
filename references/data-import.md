# Data Import & Normalization

Use this reference when the user supplies a Meta Ads Manager export, CSV, JSON, or API-shaped dataset.

## Supported sources

- Meta Ads Manager CSV exports
- JSON exports
- Meta Graph/Marketing API responses
- user-provided spreadsheets converted to rows

## Normalization

Map common aliases into the internal schema, including:

- Amount Spent → `spend`
- Impressions → `impressions`
- Reach → `reach`
- Link Clicks → `clicks`
- CTR → `ctr`
- CPC → `cpc`
- CPM → `cpm`
- Purchases/Results → `conversions`
- Purchase Conversion Value/Revenue → `revenue`
- Campaign Name → `campaign_name`
- Ad Set Name → `adset_name`
- Ad Name → `ad_name`

Preserve unknown fields instead of discarding them.

## Validation

Before analysis:

1. Confirm rows were imported.
2. Check whether spend exists.
3. Check whether impressions/clicks exist for traffic metrics.
4. Check whether conversions/revenue exist for outcome metrics.
5. Check date scope when provided.
6. Check for obviously invalid numeric relationships.

## Missing fields

Missing data should reduce the scope of the analysis, not be filled with invented values.

Example:

> Spend and impressions are available, but conversion data is missing. I can analyze delivery and traffic efficiency, but I cannot reliably assess CPA or ROAS.

## Currency

Do not silently convert currency. Preserve the source currency and state it when known.

## Aggregation

When aggregating rows, calculate ratio metrics from totals where appropriate instead of averaging row-level ratios.

## Data provenance

The report should identify whether data came from:

- live API
- Ads Manager export
- user-provided file
- mock/test data

Never claim a dataset is live when it is an uploaded/exported snapshot.
