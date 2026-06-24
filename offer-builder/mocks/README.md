# Enterprise offer mocks

Fixture-backed MCP responses for **offline** `offer-director` development and tests.

## Usage

```python
from mocks.mock_mcp import MockMCPServer

server = MockMCPServer()
server.call("crm.opportunity.get", {"opportunity_id": "006xx000004T2Q9"})
server.call("catalog.product.search", {"query": "enterprise"})
```

## Fixtures

| File | Used by |
|------|---------|
| `fixtures/dossier-example.json` | Discovery / CRM tools |

## Production

Replace `MockMCPServer` with real MCP connections to CRM, catalog, pricing engine, CLM, Gong.

Spec: `../OFFER-BUILDER-SPEC.md`
