"""Transparent weighted risk scoring for MamaSentry detections."""

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class ThreatLevel(str, Enum):
    SAFE = "safe"
    SUSPICIOUS = "suspicious"
    CRITICAL = "critical"


SIGNAL_WEIGHTS: dict[str, int] = {
    "url_domain_mismatch": 30,
    "credential_or_otp_request": 25,
    "suspicious_url": 25,
    "financial_pressure": 20,
    "impersonation": 20,
    "fake_payment_notification": 20,
    "urgent_language": 15,
}


@dataclass(frozen=True)
class RiskSignal:
    """A detected threat signal and its user-facing explanation."""

    name: str
    explanation: str
    weight: int | None = None


@dataclass(frozen=True)
class RiskAssessment:
    score: int
    level: ThreatLevel
    signals: tuple[RiskSignal, ...]


class RiskEngine:
    """Convert detections into a bounded score and transparent threat tier."""

    def assess(self, signals: Iterable[RiskSignal]) -> RiskAssessment:
        normalized_signals = tuple(
            self._with_weight(signal) for signal in signals
        )
        score = sum(signal.weight or 0 for signal in normalized_signals)
        return RiskAssessment(
            score=score,
            level=self._level_for(score),
            signals=normalized_signals,
        )

    @staticmethod
    def _with_weight(signal: RiskSignal) -> RiskSignal:
        weight = signal.weight
        if weight is None:
            weight = SIGNAL_WEIGHTS.get(signal.name, 0)
        if weight < 0:
            raise ValueError("Risk signal weights cannot be negative")
        return RiskSignal(signal.name, signal.explanation, weight)

    @staticmethod
    def _level_for(score: int) -> ThreatLevel:
        if score >= 60:
            return ThreatLevel.CRITICAL
        if score >= 25:
            return ThreatLevel.SUSPICIOUS
        return ThreatLevel.SAFE
