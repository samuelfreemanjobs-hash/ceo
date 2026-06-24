"""Validate offer-builder JSON schemas and sample instances."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

jsonschema = pytest.importorskip("jsonschema")

SCHEMAS_DIR = Path(__file__).resolve().parents[1] / "offer-builder" / "schemas"
MOCKS_DIR = Path(__file__).resolve().parents[1] / "offer-builder" / "mocks" / "fixtures"


@pytest.fixture
def schema_dir():
    return SCHEMAS_DIR


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("schema_file", list(SCHEMAS_DIR.glob("*.json")))
def test_schema_files_are_valid_json_schema(schema_file):
    schema = _load_json(schema_file)
    jsonschema.Draft202012Validator.check_schema(schema)


def test_brief_schema_accepts_minimal_brief(schema_dir):
    schema = _load_json(schema_dir / "brief.v1.json")
    instance = {
        "mode": "flagship",
        "icp": "B2B founders",
        "outcome": "Clear GTM plan",
    }
    jsonschema.validate(instance, schema)


def test_dossier_fixture_validates(schema_dir):
    schema = _load_json(schema_dir / "dossier-schema.json")
    instance = _load_json(MOCKS_DIR / "dossier-example.json")
    jsonschema.validate(instance, schema)
