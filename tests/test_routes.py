from app.routes.fraud import analyze_message_route
from app.schemas.fraud import FraudCheckRequest, FraudCheckResponse


def test_analyze_message_route_returns_schema():
    payload = FraudCheckRequest(message="URGENT!!! Send 5000 now to verify your account.")
    result = analyze_message_route(payload)

    assert isinstance(result, FraudCheckResponse)
    assert result.suspicious is True
    assert result.risk_score >= 5
    assert "urgent" in result.matches


def test_analyze_message_route_handles_clean_message():
    payload = FraudCheckRequest(message="hello friend how are you today")
    result = analyze_message_route(payload)

    assert result.suspicious is False
    assert result.risk_score == 0
