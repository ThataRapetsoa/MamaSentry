"""End-to-end message analysis for the MamaSentry demo and API."""

from dataclasses import dataclass
import re

from .ai_classifier import MessageCategory, MessageClassifier
from .risk_engine import RiskAssessment, RiskEngine, RiskSignal
from .url_checker import UrlCheckResult, UrlChecker


@dataclass(frozen=True)
class AnalysisResult:
    assessment: RiskAssessment
    explanation: str
    recommendation: str
    classification_confidence: float
    urls: tuple[UrlCheckResult, ...]

    @property
    def level(self) -> str:
        return self.assessment.level.value

    @property
    def score(self) -> int:
        return self.assessment.score


class MessageAnalyzer:
    """Combine deterministic indicators with contextual classification."""

    _url_pattern = re.compile(r"https?://[^\s<>()]+", re.IGNORECASE)
    _trusted_domains = {"absa.co.za", "capitecbank.co.za", "fnb.co.za", "standardbank.co.za"}

    def __init__(
        self,
        classifier: MessageClassifier | None = None,
        risk_engine: RiskEngine | None = None,
        url_checker: UrlChecker | None = None,
    ) -> None:
        self.classifier = classifier or MessageClassifier()
        self.risk_engine = risk_engine or RiskEngine()
        self.url_checker = url_checker or UrlChecker(self._trusted_domains)

    def analyze(self, message: str) -> AnalysisResult:
        classification = self.classifier.classify(message)
        urls = tuple(self.url_checker.check(url) for url in self._url_pattern.findall(message))
        signals = self._signals_for(message, classification.category, urls)
        assessment = self.risk_engine.assess(signals)
        return AnalysisResult(
            assessment=assessment,
            explanation=self._explanation(assessment),
            recommendation=self._recommendation(assessment),
            classification_confidence=classification.confidence,
            urls=urls,
        )

    @staticmethod
    def _signals_for(
        message: str,
        category: MessageCategory,
        urls: tuple[UrlCheckResult, ...],
    ) -> tuple[RiskSignal, ...]:
        normalized = message.casefold()
        signals: list[RiskSignal] = []

        phrase_signals = (
            ("urgent_language", ("urgent", "immediately", "right now"), "The message creates time pressure."),
            ("financial_pressure", ("send money", "pay r", "transfer", "bank account"), "The message involves money or a financial transfer."),
            ("credential_or_otp_request", ("pin", "password", "otp", "verify your account", "banking details"), "The message requests credentials or sensitive information."),
        )
        for name, phrases, explanation in phrase_signals:
            if any(phrase in normalized for phrase in phrases):
                signals.append(RiskSignal(name, explanation))

        category_signals = {
            MessageCategory.IMPERSONATION: RiskSignal("impersonation", "The sender may be impersonating a trusted person or organisation."),
            MessageCategory.PAYMENT_SCAM: RiskSignal("fake_payment_notification", "The message uses payment or proof-of-payment language."),
            MessageCategory.PHISHING: RiskSignal("credential_or_otp_request", "The message uses account-verification or phishing language."),
        }
        category_signal = category_signals.get(category)
        if category_signal and not any(signal.name == category_signal.name for signal in signals):
            signals.append(category_signal)

        for url in urls:
            if url.suspicious:
                signals.append(RiskSignal("suspicious_url", "The message contains a URL with suspicious structural or domain indicators."))
                if "untrusted_domain" in url.reasons and any(
                    brand in normalized for brand in ("absa", "capitec", "fnb", "standard bank")
                ):
                    signals.append(RiskSignal("url_domain_mismatch", "The message mentions a bank, but the link is not on its trusted domain."))
                break
        return tuple(signals)

    @staticmethod
    def _explanation(assessment: RiskAssessment) -> str:
        if not assessment.signals:
            return "No major social-engineering indicators were detected."
        names = ", ".join(signal.name.replace("_", " ") for signal in assessment.signals)
        return f"Detected {len(assessment.signals)} risk indicator(s): {names}."

    @staticmethod
    def _recommendation(assessment: RiskAssessment) -> str:
        if assessment.level.value == "critical":
            return "Do not click, reply, pay, or share information. Contact the organisation through an independently verified channel."
        if assessment.level.value == "suspicious":
            return "Pause before acting. Do not click links or send money until you verify the sender independently."
        return "No immediate action is needed. Still verify unexpected requests through a trusted channel."