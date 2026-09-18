"""Explainable, dependency-free message classification heuristics."""

from dataclasses import dataclass
from enum import Enum
import re


class MessageCategory(str, Enum):
    SAFE = "safe"
    PHISHING = "phishing"
    IMPERSONATION = "impersonation"
    PAYMENT_SCAM = "payment_scam"
    URGENT_REQUEST = "urgent_request"


@dataclass(frozen=True)
class Classification:
    category: MessageCategory
    confidence: float
    matched_terms: tuple[str, ...]


_PATTERNS: tuple[tuple[MessageCategory, tuple[str, ...]], ...] = (
    (MessageCategory.PHISHING, ("verify your account", "confirm your otp", "click here")),
    (MessageCategory.IMPERSONATION, ("hi mom", "hi dad", "this is me", "new number")),
    (MessageCategory.PAYMENT_SCAM, ("proof of payment", "eft", "payment received")),
    (MessageCategory.URGENT_REQUEST, ("urgent", "immediately", "right now", "send money")),
)


class MessageClassifier:
    """Classify messages using auditable phrase matches.

    This is intentionally a deterministic baseline that can later be replaced by
    a trained model while preserving the same result contract.
    """

    def classify(self, message: str) -> Classification:
        normalized = re.sub(r"\s+", " ", message.casefold()).strip()
        matches: list[tuple[MessageCategory, str]] = []
        for category, phrases in _PATTERNS:
            matches.extend(
                (category, phrase)
                for phrase in phrases
                if phrase in normalized
            )

        if not matches:
            return Classification(MessageCategory.SAFE, 0.5, ())

        category_counts: dict[MessageCategory, int] = {}
        matched_terms: list[str] = []
        for category, phrase in matches:
            category_counts[category] = category_counts.get(category, 0) + 1
            matched_terms.append(phrase)
        category = max(category_counts, key=category_counts.get)
        confidence = min(0.55 + (category_counts[category] * 0.15), 0.95)
        return Classification(category, confidence, tuple(matched_terms))
