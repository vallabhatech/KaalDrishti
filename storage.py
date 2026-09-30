"""Small SQLite event store for local defensive lab use."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path


class EventStore:
    def __init__(self, path: str = "data/kaaldrishti.db") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    received_at TEXT NOT NULL,
                    client TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    technique TEXT,
                    payload TEXT NOT NULL
                )"""
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def save(self, event: dict, detection: dict, received_at: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    event["event_id"], received_at, event["client"], event["event_type"],
                    detection["severity"], detection["confidence"], detection["technique"],
                    json.dumps(event, separators=(",", ":")),
                ),
            )

    def recent(self, limit: int = 50) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT event_id, received_at, client, event_type, severity, confidence, technique "
                "FROM events ORDER BY received_at DESC LIMIT ?", (limit,)
            ).fetchall()
        keys = ("event_id", "received_at", "client", "event_type", "severity", "confidence", "technique")
        return [dict(zip(keys, row)) for row in rows]
