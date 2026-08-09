# End-to-End Pipeline

The pipeline connects the intelligence modules while preserving a strict read/write boundary.

## Flow

```text
User request
    ↓
Command Router
    ↓
Mode selection
    ↓
Data acquisition / supplied dataset
    ↓
Metric normalization
    ↓
Performance + Creative + Anomaly analysis
    ↓
Account Audit
    ↓
Strategy / 7-day plan
    ↓
Report
```

For an explicit action request:

```text
User request
    ↓
Command Router → ACTION
    ↓
Resolve account + target + current state
    ↓
Build proposed change
    ↓
Action Guard / confirmation
    ↓
Meta API write
    ↓
Verify result
```

## Important boundary

The analysis pipeline must never execute Meta writes.

This separation prevents a recommendation, anomaly, or audit result from becoming an accidental account change.

## Data sources

The pipeline can consume:

- live Meta API data when a valid connector is available
- Ads Manager exports
- user-provided CSV/JSON data
- mock data for testing

The pipeline must identify which source was used.

## Mixed requests

If a user asks for analysis and action together, complete the analysis first, produce the proposed changes, then use the explicit action workflow for execution.

## Missing data

If a requested analysis needs unavailable data:

1. state what is missing
2. continue with what is defensible
3. do not fabricate live values
4. explain what additional data would improve confidence
