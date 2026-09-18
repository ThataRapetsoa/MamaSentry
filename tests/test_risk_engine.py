from app.services.risk_engine import RiskEngine, RiskSignal, ThreatLevel


def test_risk_engine_applies_matrix_and_thresholds() -> None:
    assessment = RiskEngine().assess(
        [
            RiskSignal("suspicious_url", "The link is not trusted."),
            RiskSignal("urgent_language", "The message creates pressure."),
        ]
    )

    assert assessment.score == 40
    assert assessment.level is ThreatLevel.SUSPICIOUS
    assert [signal.weight for signal in assessment.signals] == [25, 15]


def test_unknown_signals_are_explainable_without_affecting_score() -> None:
    assessment = RiskEngine().assess([RiskSignal("new_signal", "Needs review")])

    assert assessment.score == 0
    assert assessment.level is ThreatLevel.SAFE
    assert assessment.signals[0].weight == 0
