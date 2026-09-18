import json
import os
import sqlite3
from typing import Iterable, List, Optional

DEFAULT_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "mamasentry.db"))


def get_db_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    conn = get_db_connection(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS message_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_message TEXT NOT NULL,
            cleaned_message TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            suspicious INTEGER NOT NULL,
            matches TEXT NOT NULL,
            source TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def save_detection(
    raw_message: str,
    cleaned_message: str,
    risk_score: int,
    suspicious: int,
    matches: Iterable[str],
    source: str,
    db_path: str = DEFAULT_DB_PATH,
) -> int:
    init_db(db_path)
    conn = get_db_connection(db_path)
    payload = json.dumps(list(matches))
    cursor = conn.execute(
        """
        INSERT INTO message_reports (raw_message, cleaned_message, risk_score, suspicious, matches, source)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (raw_message, cleaned_message, risk_score, suspicious, payload, source),
    )
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id


def list_recent_reports(limit: int = 20, db_path: str = DEFAULT_DB_PATH) -> List[dict]:
    conn = get_db_connection(db_path)
    rows = conn.execute(
        """
        SELECT id, raw_message, cleaned_message, risk_score, suspicious, matches, source, created_at
        FROM message_reports
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
