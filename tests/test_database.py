import os

from app.db import get_db_connection, init_db, save_detection


def test_init_db_creates_tables():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "test_mamasentry.db"))
    if os.path.exists(db_path):
        os.remove(db_path)

    init_db(db_path)

    conn = get_db_connection(db_path)
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='message_reports'"
    ).fetchall()
    conn.close()

    assert len(tables) == 1


def test_save_detection_persists_record():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "test_mamasentry_insert.db"))
    if os.path.exists(db_path):
        os.remove(db_path)

    init_db(db_path)
    record_id = save_detection(
        raw_message="URGENT!!! Send 5000 now to verify your account.",
        cleaned_message="urgent send 5000 now to verify your account",
        risk_score=8,
        suspicious=1,
        matches=["urgent", "send", "verify", "account"],
        source="api",
        db_path=db_path,
    )

    conn = get_db_connection(db_path)
    row = conn.execute(
        "SELECT raw_message, risk_score, suspicious, source FROM message_reports WHERE id = ?",
        (record_id,),
    ).fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "URGENT!!! Send 5000 now to verify your account."
    assert row[1] == 8
    assert row[2] == 1
    assert row[3] == "api"
