---
name: funnel-visualization
description: Use when producing visual funnel representations — diagrams, flowcharts, journey maps. Triggers on "diagram", "visualize", "map", "flowchart", or implicitly after funnel design (always include a visual in the Funnel Spec).
---

# Funnel Visualization

**Used by:** Funnel Architect (Phase 3 — Map)

## Default outputs

1. **Mermaid flowchart** — linear, looped, or multi-entry
2. **Stage table** — Stage | Buyer state | Channels | Assets | KPI | Current | Target
3. **Optional:** customer journey map (actions, thoughts, touchpoints, pain, opportunities)

## Mermaid templates

### Linear funnel

```mermaid
flowchart LR
    A[Stage 1<br/>volume] -->|rate%| B[Stage 2]
    B -->|rate%| C[Stage 3]
    style D fill:#fee,stroke:#900
```

Highlight leak stage with `style` (red) and expansion with green.

### PLG loop

```mermaid
flowchart LR
    A[Acquire] --> B[Activate]
    B --> C[Retain]
    C --> D[Revenue]
    D --> E[Refer]
    E -.-> A
```

## Sankey-style (complex multi-channel)

Describe channel → stage flows in table if Mermaid Sankey unsupported; note volumes at each merge.

## Rendering rules

- Include **volumes and rates** on edges when data available
- Don't diagram 15 nodes — simplify to decision-relevant stages
- Pair every diagram with the stage table (diagram alone is insufficient)

## References

- `references/mermaid-templates.md`
- `references/journey-map-templates.md`
- `references/rendering-rules.md`
