import sqlite3
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent  # raiz do projeto

DB_PATH = Path(os.getenv("SCURL_DB_PATH", BASE_DIR / "providers" / "database" / "storage" / "scurl.db"))
SCHEMA_FILE = BASE_DIR / "providers" / "database" / "schema" / "scans.sql"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_connection() as conn:
        with open(SCHEMA_FILE, "r") as f:
            conn.executescript(f.read())
        conn.execute("CREATE INDEX IF NOT EXISTS idx_url_hash ON scans(url_hash)")
        conn.commit()