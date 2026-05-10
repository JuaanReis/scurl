import sqlite3
import os

DB_PATH = os.getenv("SCURL_DB_PATH", "./datasets/scurl.db")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                url_hash    TEXT NOT NULL UNIQUE,
                url         TEXT NOT NULL,
                score       REAL,
                risk_level  TEXT,
                verdict     TEXT,
                scan_id     TEXT,
                timestamp   TEXT,
                payload     TEXT NOT NULL
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_url_hash ON scans(url_hash)")
        conn.commit()