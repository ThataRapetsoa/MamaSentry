from __future__ import annotations

from typing import Any, List

from app.fraud.rules import DEFAULT_FRAUD_RULES
from app.utils.text_cleaner import clean_text


def _match_rule(normalized_text: str, rule_pattern: str) -> bool:
    tokens = normalized_text.split()
    required_tokens = clean_text(rule_pattern).split()
    if not required_tokens:
        return False

    if len(required_tokens) == 1:
        return required_tokens[0] in tokens

    return all(token in tokens for token in required_tokens)


def find_fraud_patterns(text: str) -> List[str]:
    """Return the matched terms and phrases to make fraud output easy to read."""
    normalized = clean_text(text or "")
    matches: List[str] = []

    for rule in DEFAULT_FRAUD_RULES:
        if _match_rule(normalized, rule.pattern):
            for token in clean_text(rule.pattern).split():
                if token and token not in matches:
                    matches.append(token)

    return matches


def score_fraud_risk(text: str) -> int:
    """Calculate a risk score based on weighted fraud rules."""
    normalized = clean_text(text or "")
    score = 0

    for rule in DEFAULT_FRAUD_RULES:
        if _match_rule(normalized, rule.pattern):
            score += rule.weight

    return score


def detect_fraud(text: str) -> dict[str, Any]:
    """Return a small fraud-analysis payload for route handlers and services."""
    matches = find_fraud_patterns(text)
    risk_score = score_fraud_risk(text)

    return {
        "suspicious": bool(matches) or risk_score >= 5,
        "matches": matches,
        "risk_score": risk_score,
    }
