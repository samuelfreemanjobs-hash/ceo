"""
preferences_store.py
====================
Production-ready PreferencesStore implementations for the Scheduler Agent.

SQLitePreferencesStore — zero-infra dev/small deploy (default for getting started)
PostgresPreferencesStore — production multi-tenant (requires psycopg2-binary)
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from scheduler_agent import PreferencesStore, UserPreferences

DEFAULT_DB_PATH = Path(__file__).resolve().parent / "data" / "preferences.db"

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id TEXT PRIMARY KEY,
    timezone TEXT NOT NULL DEFAULT 'UTC',
    working_hours_start INTEGER NOT NULL DEFAULT 9,
    working_hours_end INTEGER NOT NULL DEFAULT 17,
    working_days TEXT NOT NULL DEFAULT '[0,1,2,3,4]',
    default_meeting_duration_minutes INTEGER NOT NULL DEFAULT 30,
    buffer_minutes_between_meetings INTEGER NOT NULL DEFAULT 15,
    max_meetings_per_day INTEGER NOT NULL DEFAULT 6,
    focus_block_minimum_minutes INTEGER NOT NULL DEFAULT 90,
    no_meeting_days TEXT NOT NULL DEFAULT '[]',
    preferred_meeting_times TEXT NOT NULL DEFAULT '[]'
);
"""

_POSTGRES_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id TEXT PRIMARY KEY,
    timezone TEXT NOT NULL DEFAULT 'UTC',
    working_hours_start INT NOT NULL DEFAULT 9,
    working_hours_end INT NOT NULL DEFAULT 17,
    working_days INT[] NOT NULL DEFAULT '{0,1,2,3,4}',
    default_meeting_duration_minutes INT NOT NULL DEFAULT 30,
    buffer_minutes_between_meetings INT NOT NULL DEFAULT 15,
    max_meetings_per_day INT NOT NULL DEFAULT 6,
    focus_block_minimum_minutes INT NOT NULL DEFAULT 90,
    no_meeting_days INT[] NOT NULL DEFAULT '{}',
    preferred_meeting_times TEXT[] NOT NULL DEFAULT '{}'
);
"""


def _row_to_prefs(user_id: str, row: dict[str, Any]) -> UserPreferences:
    working_days = row["working_days"]
    if isinstance(working_days, str):
        working_days = json.loads(working_days)
    no_meeting_days = row["no_meeting_days"]
    if isinstance(no_meeting_days, str):
        no_meeting_days = json.loads(no_meeting_days)
    preferred = row["preferred_meeting_times"]
    if isinstance(preferred, str):
        preferred = json.loads(preferred)
    elif isinstance(preferred, list) and preferred and not isinstance(preferred[0], str):
        preferred = [str(p) for p in preferred]

    return UserPreferences(
        user_id=user_id,
        timezone=row["timezone"],
        working_hours_start=row["working_hours_start"],
        working_hours_end=row["working_hours_end"],
        working_days=list(working_days),
        default_meeting_duration_minutes=row["default_meeting_duration_minutes"],
        buffer_minutes_between_meetings=row["buffer_minutes_between_meetings"],
        max_meetings_per_day=row["max_meetings_per_day"],
        focus_block_minimum_minutes=row["focus_block_minimum_minutes"],
        no_meeting_days=list(no_meeting_days),
        preferred_meeting_times=list(preferred),
    )


def _prefs_to_row(p: UserPreferences) -> dict[str, Any]:
    return {
        "user_id": p.user_id,
        "timezone": p.timezone,
        "working_hours_start": p.working_hours_start,
        "working_hours_end": p.working_hours_end,
        "working_days": json.dumps(p.working_days),
        "default_meeting_duration_minutes": p.default_meeting_duration_minutes,
        "buffer_minutes_between_meetings": p.buffer_minutes_between_meetings,
        "max_meetings_per_day": p.max_meetings_per_day,
        "focus_block_minimum_minutes": p.focus_block_minimum_minutes,
        "no_meeting_days": json.dumps(p.no_meeting_days),
        "preferred_meeting_times": json.dumps(p.preferred_meeting_times),
    }


class SQLitePreferencesStore(PreferencesStore):
    """File-backed preferences — good for dev and single-node deploy."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        self.db_path = Path(db_path or DEFAULT_DB_PATH)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(_SCHEMA_SQL)
            conn.commit()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get(self, user_id: str) -> UserPreferences:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM user_preferences WHERE user_id = ?",
                (user_id,),
            ).fetchone()
            if row is None:
                prefs = UserPreferences(user_id=user_id)
                self._insert(conn, prefs)
                conn.commit()
                return prefs
            return _row_to_prefs(user_id, dict(row))

    def update(self, user_id: str, changes: dict[str, Any]) -> UserPreferences:
        p = self.get(user_id)
        for k, v in changes.items():
            if hasattr(p, k):
                setattr(p, k, v)
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO user_preferences (
                    user_id, timezone, working_hours_start, working_hours_end,
                    working_days, default_meeting_duration_minutes,
                    buffer_minutes_between_meetings, max_meetings_per_day,
                    focus_block_minimum_minutes, no_meeting_days,
                    preferred_meeting_times
                ) VALUES (
                    :user_id, :timezone, :working_hours_start, :working_hours_end,
                    :working_days, :default_meeting_duration_minutes,
                    :buffer_minutes_between_meetings, :max_meetings_per_day,
                    :focus_block_minimum_minutes, :no_meeting_days,
                    :preferred_meeting_times
                )
                ON CONFLICT(user_id) DO UPDATE SET
                    timezone = excluded.timezone,
                    working_hours_start = excluded.working_hours_start,
                    working_hours_end = excluded.working_hours_end,
                    working_days = excluded.working_days,
                    default_meeting_duration_minutes = excluded.default_meeting_duration_minutes,
                    buffer_minutes_between_meetings = excluded.buffer_minutes_between_meetings,
                    max_meetings_per_day = excluded.max_meetings_per_day,
                    focus_block_minimum_minutes = excluded.focus_block_minimum_minutes,
                    no_meeting_days = excluded.no_meeting_days,
                    preferred_meeting_times = excluded.preferred_meeting_times
                """,
                _prefs_to_row(p),
            )
            conn.commit()
        return p

    def _insert(self, conn: sqlite3.Connection, p: UserPreferences) -> None:
        conn.execute(
            """
            INSERT INTO user_preferences (
                user_id, timezone, working_hours_start, working_hours_end,
                working_days, default_meeting_duration_minutes,
                buffer_minutes_between_meetings, max_meetings_per_day,
                focus_block_minimum_minutes, no_meeting_days,
                preferred_meeting_times
            ) VALUES (
                :user_id, :timezone, :working_hours_start, :working_hours_end,
                :working_days, :default_meeting_duration_minutes,
                :buffer_minutes_between_meetings, :max_meetings_per_day,
                :focus_block_minimum_minutes, :no_meeting_days,
                :preferred_meeting_times
            )
            """,
            _prefs_to_row(p),
        )


class PostgresPreferencesStore(PreferencesStore):
    """Postgres-backed preferences for production multi-tenant deploy."""

    def __init__(self, dsn: str) -> None:
        try:
            import psycopg2
            import psycopg2.extras
        except ImportError as e:
            raise ImportError(
                "psycopg2-binary not installed. "
                "Run: pip install psycopg2-binary"
            ) from e
        self._psycopg2 = psycopg2
        self._extras = psycopg2.extras
        self.dsn = dsn
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(_POSTGRES_SCHEMA_SQL)
            conn.commit()

    def _connect(self):
        return self._psycopg2.connect(self.dsn)

    def get(self, user_id: str) -> UserPreferences:
        with self._connect() as conn:
            with conn.cursor(cursor_factory=self._extras.RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM user_preferences WHERE user_id = %s",
                    (user_id,),
                )
                row = cur.fetchone()
                if row is None:
                    prefs = UserPreferences(user_id=user_id)
                    self._insert(cur, prefs)
                    conn.commit()
                    return prefs
                return _row_to_prefs(user_id, dict(row))

    def update(self, user_id: str, changes: dict[str, Any]) -> UserPreferences:
        p = self.get(user_id)
        for k, v in changes.items():
            if hasattr(p, k):
                setattr(p, k, v)
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO user_preferences (
                        user_id, timezone, working_hours_start, working_hours_end,
                        working_days, default_meeting_duration_minutes,
                        buffer_minutes_between_meetings, max_meetings_per_day,
                        focus_block_minimum_minutes, no_meeting_days,
                        preferred_meeting_times
                    ) VALUES (
                        %(user_id)s, %(timezone)s, %(working_hours_start)s,
                        %(working_hours_end)s, %(working_days)s,
                        %(default_meeting_duration_minutes)s,
                        %(buffer_minutes_between_meetings)s,
                        %(max_meetings_per_day)s,
                        %(focus_block_minimum_minutes)s,
                        %(no_meeting_days)s, %(preferred_meeting_times)s
                    )
                    ON CONFLICT (user_id) DO UPDATE SET
                        timezone = EXCLUDED.timezone,
                        working_hours_start = EXCLUDED.working_hours_start,
                        working_hours_end = EXCLUDED.working_hours_end,
                        working_days = EXCLUDED.working_days,
                        default_meeting_duration_minutes = EXCLUDED.default_meeting_duration_minutes,
                        buffer_minutes_between_meetings = EXCLUDED.buffer_minutes_between_meetings,
                        max_meetings_per_day = EXCLUDED.max_meetings_per_day,
                        focus_block_minimum_minutes = EXCLUDED.focus_block_minimum_minutes,
                        no_meeting_days = EXCLUDED.no_meeting_days,
                        preferred_meeting_times = EXCLUDED.preferred_meeting_times
                    """,
                    {
                        "user_id": p.user_id,
                        "timezone": p.timezone,
                        "working_hours_start": p.working_hours_start,
                        "working_hours_end": p.working_hours_end,
                        "working_days": p.working_days,
                        "default_meeting_duration_minutes": p.default_meeting_duration_minutes,
                        "buffer_minutes_between_meetings": p.buffer_minutes_between_meetings,
                        "max_meetings_per_day": p.max_meetings_per_day,
                        "focus_block_minimum_minutes": p.focus_block_minimum_minutes,
                        "no_meeting_days": p.no_meeting_days,
                        "preferred_meeting_times": p.preferred_meeting_times,
                    },
                )
            conn.commit()
        return p

    def _insert(self, cur, p: UserPreferences) -> None:
        cur.execute(
            """
            INSERT INTO user_preferences (
                user_id, timezone, working_hours_start, working_hours_end,
                working_days, default_meeting_duration_minutes,
                buffer_minutes_between_meetings, max_meetings_per_day,
                focus_block_minimum_minutes, no_meeting_days,
                preferred_meeting_times
            ) VALUES (
                %(user_id)s, %(timezone)s, %(working_hours_start)s,
                %(working_hours_end)s, %(working_days)s,
                %(default_meeting_duration_minutes)s,
                %(buffer_minutes_between_meetings)s,
                %(max_meetings_per_day)s,
                %(focus_block_minimum_minutes)s,
                %(no_meeting_days)s, %(preferred_meeting_times)s
            )
            """,
            {
                "user_id": p.user_id,
                "timezone": p.timezone,
                "working_hours_start": p.working_hours_start,
                "working_hours_end": p.working_hours_end,
                "working_days": p.working_days,
                "default_meeting_duration_minutes": p.default_meeting_duration_minutes,
                "buffer_minutes_between_meetings": p.buffer_minutes_between_meetings,
                "max_meetings_per_day": p.max_meetings_per_day,
                "focus_block_minimum_minutes": p.focus_block_minimum_minutes,
                "no_meeting_days": p.no_meeting_days,
                "preferred_meeting_times": p.preferred_meeting_times,
            },
        )
