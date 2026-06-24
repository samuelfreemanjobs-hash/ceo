# Funnel diagram rendering rules

## When a diagram helps

- 3–7 stages with known or estimated conversion rates
- Multi-entry or looped motions (PLG, enterprise)
- User needs to align team on "where the leak is"
- Handoff from Scout GTM teardown → visual map

## When it's noise

- Single-stage copy refresh
- Metrics-only request with no structural change
- User already has accurate diagram (update table only)

## Required pairing

Every Mermaid diagram **must** ship with the stage table (Stage | Buyer state | Channels | Assets | KPI | Current | Target). Diagram alone is insufficient for execution.

## Visual encoding

| Signal | Mermaid technique |
|--------|-------------------|
| Leak stage | `style NODE fill:#fee,stroke:#900,stroke-width:3px` |
| Expansion / growth | `style NODE fill:#efe,stroke:#090` |
| Optional path | dashed edge `-.->` |
| Multi-channel merge | subgraph or table fallback |

## Data labeling

- Include **volume** on nodes when known: `~12K/mo`
- Include **rate** on edges: `-->|35%|`
- Unknown: `?` + list assumption in open questions

## Complexity limits

- Max ~7 nodes on primary path; collapse micro-conversions
- For 10+ channel sources, use **channel attribution table** instead of mega-diagram
- Sankey: describe in table if renderer unsupported

## ASCII fallback

Use only when Mermaid unavailable:

```
[Visit 12K] --8%--> [Trial 960] --35%--> [Activated 336] --55%--> [Paid 185]
                              ^^^ leak
```

## Customer journey map

Use full journey grid (see `journey-map-templates.md`) only for 3+ stakeholders or 60d+ cycles.
