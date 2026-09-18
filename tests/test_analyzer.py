from app.services.analyzer import MessageAnalyzer


def test_analyzer_exposes_score_reasons_and_action_for_bank_phishing() -> None:
    result = MessageAnalyzer().analyze(
        "URGENT: Your FNB account is suspended. Verify your PIN immediately at "
        "https://fnb-secure-login.example/verify"
    )

    assert result.level == "critical"
    assert result.score >= 60
    assert len(result.assessment.signals) >= 4
    assert "Do not click" in result.recommendation
    assert result.urls[0].suspicious is True


def test_analyzer_catches_linkless_family_impersonation() -> None:
    result = MessageAnalyzer().analyze(
        "Hi Mom, this is me from my new number. Please send money to this bank account."
    )

    assert result.level == "suspicious"
    assert any(signal.name == "impersonation" for signal in result.assessment.signals)
    assert result.urls == ()