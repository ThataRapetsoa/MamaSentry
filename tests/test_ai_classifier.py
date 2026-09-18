from app.services.ai_classifier import MessageCategory, MessageClassifier


def test_classifier_detects_phishing_terms_case_insensitively() -> None:
    result = MessageClassifier().classify("Please VERIFY YOUR ACCOUNT and confirm your OTP")

    assert result.category is MessageCategory.PHISHING
    assert result.confidence > 0.5
    assert "verify your account" in result.matched_terms


def test_classifier_returns_safe_for_neutral_text() -> None:
    result = MessageClassifier().classify("See you at the shop after lunch")

    assert result.category is MessageCategory.SAFE
    assert result.matched_terms == ()
