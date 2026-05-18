import sqlite3
import os
from pathlib import Path
import threading

BASE_DIR = Path(__file__).parent.parent.parent
DB_PATH = Path(os.getenv("SCURL_DB_PATH", BASE_DIR / "providers" / "database" / "storage" / "scurl.db"))
SCHEMA_FILE = BASE_DIR / "providers" / "database" / "schema" / "scans.sql"
_local = threading.local()

def get_connection() -> sqlite3.Connection:
    if not hasattr(_local, "conn"):
        conn = sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        _local.conn = conn
    return _local.conn

def init_db() -> None:
    schema = SCHEMA_FILE.read_text()
    with get_connection() as conn:
        conn.executescript(schema)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_url_hash ON scans(url_hash)")