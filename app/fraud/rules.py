from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class FraudRule:
    name: str
    category: str
    pattern: str
    weight: int = 0
    description: str = ""


DEFAULT_FRAUD_RULES: List[FraudRule] = [
    FraudRule("urgent_action", "urgency", "urgent", 2, "Urgent language used to pressure the reader."),
    FraudRule("verify_account", "identity", "verify account", 3, "Account verification language."),
    FraudRule("send_money", "payment", "send money", 3, "Request to send funds."),
    FraudRule("claim_prize", "reward", "claim prize", 4, "Reward scam wording."),
    FraudRule("winner_alert", "reward", "winner", 3, "Winner notification language used in scams."),
    FraudRule("click_now", "action", "click now", 2, "Action request designed to trigger impulse behavior."),
    FraudRule("win_money", "reward", "win money", 4, "Claims of money win or payout."),
    FraudRule("confirm_identity", "identity", "confirm identity", 3, "Identity confirmation pressure."),
    FraudRule("act_now", "urgency", "act now", 2, "Immediate action demanded."),
    FraudRule("bank_account", "identity", "bank account", 2, "Bank account detail pressure."),
]


def build_rule_index() -> dict[str, FraudRule]:
    return {rule.name: rule for rule in DEFAULT_FRAUD_RULES}
