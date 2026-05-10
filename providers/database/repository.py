import json
from providers.database.connection import get_connection

def list_scans(limit: int = 50, offset: int = 0) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT url, score, risk_level, verdict, scan_id, timestamp, url_hash FROM scans ORDER BY timestamp DESC LIMIT ? OFFSET ?",
            (limit, offset)
        ).fetchall()
    return [dict(row) for row in rows]

def get_scan(identifier: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT payload FROM scans WHERE scan_id = ? OR url_hash = ?",
            (identifier, identifier)
        ).fetchone()
    if row:
        return json.loads(row["payload"])
    return None

def find_by_hash(url_hash: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT payload FROM scans WHERE url_hash = ?", (url_hash,)
        ).fetchone()
    if row:
        return json.loads(row["payload"])
    return None

def save_scan(result: dict) -> None:
    url_hash = result["meta"]["url_hash"]
    payload  = json.dumps(result)

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO scans (url_hash, url, score, risk_level, verdict, scan_id, timestamp, payload)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(url_hash) DO UPDATE SET
                payload    = excluded.payload,
                score      = excluded.score,
                risk_level = excluded.risk_level,
                verdict    = excluded.verdict,
                scan_id    = excluded.scan_id,
                timestamp  = excluded.timestamp
        """, (
            url_hash,
            result["target"]["url"],
            result["result"]["score"],
            result["result"]["risk_level"],
            result["result"]["verdict"],
            result["meta"]["scan_id"],
            result["meta"]["timestamp"],
            payload
        ))
        conn.commit()