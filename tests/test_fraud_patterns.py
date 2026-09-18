from app.fraud.patterns import detect_fraud


def test_detect_fraud_flags_scam_message():
    result = detect_fraud("URGENT!!! Send 5000 now to verify your account.")

    assert result["suspicious"] is True
    assert result["risk_score"] >= 5
    assert "urgent" in result["matches"]
    assert "verify" in result["matches"]


def test_detect_fraud_ignores_normal_message():
    result = detect_fraud("hello friend, how are you doing today")

    assert result["suspicious"] is False
    assert result["risk_score"] == 0


def test_detect_fraud_flags_reward_scam_pattern():
    result = detect_fraud("Congratulations winner! Claim your prize now and verify your bank account.")

    assert result["suspicious"] is True
    assert result["risk_score"] >= 8
    assert "claim" in result["matches"] or "prize" in result["matches"] or "winner" in result["matches"]
