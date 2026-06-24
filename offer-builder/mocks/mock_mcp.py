"""
mock_mcp.py — fixture-backed MCP tool responses for local enterprise offer development.

Usage in tests or offline demos:
    from mocks.mock_mcp import MockMCPServer
    server = MockMCPServer()
    server.call("crm.opportunity.get", {"opportunity_id": "006xx000004T2Q9"})
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_FIXTURES = Path(__file__).resolve().parent / "fixtures"


class MockMCPServer:
    """Returns canned JSON for enterprise offer-director tool names."""

    def __init__(self, fixtures_dir: Path | None = None) -> None:
        self.fixtures_dir = fixtures_dir or _FIXTURES

    def call(self, tool_name: str, tool_input: dict[str, Any] | None = None) -> dict[str, Any]:
        tool_input = tool_input or {}
        handlers = {
            "crm.opportunity.get": self._crm_opportunity,
            "crm.account.get": self._crm_account,
            "crm.activity.search": self._crm_activity,
            "catalog.product.search": self._catalog_search,
            "pricing_engine.get_rates": self._pricing_rates,
            "gong.transcript.search": self._gong_search,
        }
        handler = handlers.get(tool_name)
        if handler is None:
            return {"_mock": True, "tool": tool_name, "status": "not_implemented", "input": tool_input}
        return handler(tool_input)

    def _load(self, name: str) -> dict[str, Any]:
        path = self.fixtures_dir / name
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return {}

    def _crm_opportunity(self, inp: dict) -> dict:
        d = self._load("dossier-example.json")
        return {
            "_mock": True,
            "opportunity_id": inp.get("opportunity_id", "006xx000004T2Q9"),
            "stage": d.get("opportunity", {}).get("stage", "Discovery"),
            "amount": d.get("opportunity", {}).get("amount_estimate", 75000),
            "account_name": d.get("account", {}).get("name", "Acme Corp"),
        }

    def _crm_account(self, inp: dict) -> dict:
        d = self._load("dossier-example.json")
        return {"_mock": True, "account": d.get("account", {})}

    def _crm_activity(self, inp: dict) -> dict:
        return {
            "_mock": True,
            "activities": [
                {"type": "email", "subject": "SSO timeline concern", "date": "2026-06-10"},
            ],
        }

    def _catalog_search(self, inp: dict) -> dict:
        return {
            "_mock": True,
            "products": [
                {"sku": "ENT-PLATFORM", "name": "Enterprise Platform", "list_price": 50000},
                {"sku": "ENT-SSO", "name": "SSO Accelerator", "list_price": 15000},
            ],
        }

    def _pricing_rates(self, inp: dict) -> dict:
        return {
            "_mock": True,
            "currency": "USD",
            "rates": {"ENT-PLATFORM": 50000, "ENT-SSO": 15000},
            "floor_prices": {"ENT-PLATFORM": 40000, "ENT-SSO": 12000},
        }

    def _gong_search(self, inp: dict) -> dict:
        return {
            "_mock": True,
            "transcripts": [
                {"snippet": "We lose deals when SSO takes 90 days", "meeting_id": "abc123"},
            ],
        }
