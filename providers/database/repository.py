import json
from providers.database.connection import get_connection
from pathlib import Path
from datetime import datetime, timezone, timedelta

INSERT_FILE = Path(__file__).parent / "schema" / "insert_result.sql"

def list_scans(limit: int = 50, offset: int = 0) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT url, score, risk_level, verdict, scan_id, timestamp, url_hash FROM scans ORDER BY timestamp DESC LIMIT ? OFFSET ?",
            (limit, offset)
        ).fetchall()
    return [dict(row) for row in rows]

def get_scan(identifier: str) -> tuple[dict, dict] | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT payload FROM scans WHERE scan_id = ? OR url_hash = ?",
            (identifier, identifier)
        ).fetchone()
    if row:
        data = json.loads(row["payload"])
        if "scan" in data:
            return data["scan"], data["target"]
        return data, {}
    return None

def save_scan(scan: dict, target: dict) -> None:
    url_hash = scan["meta"]["url_hash"]
    payload = json.dumps({"scan": scan, "target": target})

    with get_connection() as conn:
        with open(INSERT_FILE, "r", encoding="utf-8") as f:
            query = f.read()
        conn.execute(
            query,
            (
                url_hash,
                scan["meta"].get("url", ""),
                scan["result"]["score"],
                scan["result"]["risk_level"],
                scan["result"]["verdict"],
                scan["meta"]["scan_id"],
                scan["meta"]["timestamp"],
                payload
            )
        )
        conn.commit()

def find_by_hash(url_hash: str, ttl_seconds: int = 3600) -> tuple[dict, dict] | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT payload, timestamp FROM scans WHERE url_hash = ?", (url_hash,)
        ).fetchone()

    if not row:
        return None

    data = json.loads(row["payload"])
    scan = data.get("scan", data)
    score = scan.get("result", {}).get("score", 0)

    if score >= 40:
        ttl_seconds = 900
    
    ts = datetime.fromisoformat(row["timestamp"])
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)

    if datetime.now(timezone.utc) - ts > timedelta(seconds=ttl_seconds):
        return None

    if "scan" in data:
        return data["scan"], data["target"]
    return data, {}