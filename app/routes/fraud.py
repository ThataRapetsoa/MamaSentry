from __future__ import annotations

from app.db import save_detection
from app.fraud.patterns import detect_fraud
from app.schemas.fraud import FraudCheckRequest, FraudCheckResponse
from app.utils.text_cleaner import clean_text


def analyze_message_route(payload: FraudCheckRequest) -> FraudCheckResponse:
    """Validate an incoming message and return fraud classification data."""
    if payload is None:
        raise ValueError("payload cannot be None")

    message = payload.message or ""
    cleaned = clean_text(message)
    result = detect_fraud(cleaned)

    save_detection(
        raw_message=message,
        cleaned_message=cleaned,
        risk_score=result["risk_score"],
        suspicious=1 if result["suspicious"] else 0,
        matches=result["matches"],
        source="api",
    )

    return FraudCheckResponse(
        suspicious=result["suspicious"],
        risk_score=result["risk_score"],
        matches=result["matches"],
        cleaned_message=cleaned,
    )
