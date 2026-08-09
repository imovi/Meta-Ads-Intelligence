# Scripts

The scripts are small, dependency-light building blocks for the Meta Ads Intelligence skill.

## `meta_api_client.py`

Runtime adapter for Meta Graph/Marketing API requests.

Environment variables:

- `META_ACCESS_TOKEN` — access token supplied by the runtime secret manager.
- `META_GRAPH_API_BASE_URL` — optional API base URL override.

No token is stored in the repository.

The adapter intentionally does not guess a Graph API version. The integration layer should supply the currently supported path/base URL.

### Read example

```bash
export META_ACCESS_TOKEN="..."
python scripts/meta_api_client.py act_123 --fields name,account_status,currency
```

For production integrations, prefer a secure secret store rather than shell history or committed `.env` files.

## `action_guard.py`

Creates and validates proposed changes before account writes. The agent/skill must establish explicit user intent first. High-impact operations should always use the proposal/confirmation workflow.

## Design rule

These scripts do not decide whether the user has authorized an action. That decision belongs to the Skill's conversational safety layer.
