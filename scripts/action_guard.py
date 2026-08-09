"""Safety helpers for explicit Meta Ads account actions.

This module never decides whether the user wants an action. The skill layer must
establish explicit intent first. It provides a consistent proposal/confirmation
representation and conservative validation helpers.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict


HIGH_IMPACT = {
    "publish", "activate", "delete", "budget_increase", "major_targeting_change",
    "replace_creative", "change_bid", "change_optimization",
}


@dataclass
class ProposedChange:
    account: str
    target_type: str
    target_id: str
    target_name: str
    operation: str
    current: Dict[str, Any]
    requested: Dict[str, Any]
    reason: str = ""

    @property
    def high_impact(self) -> bool:
        return self.operation in HIGH_IMPACT

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["high_impact"] = self.high_impact
        return result


def validate_proposal(proposal: ProposedChange) -> list[str]:
    errors: list[str] = []
    if not proposal.account:
        errors.append("Missing account scope.")
    if not proposal.target_id:
        errors.append("Missing target object ID.")
    if not proposal.operation:
        errors.append("Missing operation.")
    if not proposal.requested:
        errors.append("Missing requested state.")
    return errors


def confirmation_text(proposal: ProposedChange) -> str:
    level = "HIGH-IMPACT" if proposal.high_impact else "ACCOUNT CHANGE"
    return (
        f"⚠️ Proposed Meta Ads change ({level})\n\n"
        f"Account: {proposal.account}\n"
        f"Target: {proposal.target_name or proposal.target_id} ({proposal.target_type})\n"
        f"Current: {proposal.current}\n"
        f"New: {proposal.requested}\n"
        f"Reason: {proposal.reason or 'Not specified'}\n\n"
        "Apply this change?"
    )


if __name__ == "__main__":
    example = ProposedChange(
        account="act_123",
        target_type="campaign",
        target_id="123",
        target_name="Example Campaign",
        operation="budget_increase",
        current={"daily_budget": 50},
        requested={"daily_budget": 75},
        reason="Stable CPA over the selected period.",
    )
    print(confirmation_text(example))
