"""Tests for preferences_store implementations."""

import tempfile
from pathlib import Path

import pytest

from preferences_store import SQLitePreferencesStore


def test_sqlite_preferences_get_creates_default():
    with tempfile.TemporaryDirectory() as tmp:
        store = SQLitePreferencesStore(Path(tmp) / "prefs.db")
        p = store.get("user_1")
        assert p.user_id == "user_1"
        assert p.timezone == "UTC"
        assert p.working_hours_start == 9


def test_sqlite_preferences_update_persists():
    with tempfile.TemporaryDirectory() as tmp:
        db = Path(tmp) / "prefs.db"
        store = SQLitePreferencesStore(db)
        store.update("user_1", {"timezone": "America/New_York", "working_hours_end": 18})
        store2 = SQLitePreferencesStore(db)
        p = store2.get("user_1")
        assert p.timezone == "America/New_York"
        assert p.working_hours_end == 18
