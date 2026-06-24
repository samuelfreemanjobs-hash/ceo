# Mermaid funnel templates

Copy and replace placeholders: `{stage}`, `{volume}`, `{rate}`.

## Linear funnel with leak highlight

```mermaid
flowchart LR
    A["{stage1}<br/>~{volume1}/mo"] -->|"{rate1}%"| B["{stage2}<br/>~{volume2}/mo"]
    B -->|"{rate2}%"| C["{stage3}<br/>~{volume3}/mo"]
    C -->|"{rate3}%"| D["{stage4}<br/>~{volume4}/mo"]
    style C fill:#fee,stroke:#900,stroke-width:3px
```

Use `style` red on leak stage, green on expansion.

## PLG loop (AARRR)

```mermaid
flowchart LR
    A[Acquire] --> B[Activate]
    B --> C[Retain]
    C --> D[Revenue]
    D --> E[Refer]
    E -.-> A
```

## Multi-entry enterprise

```mermaid
flowchart TB
    IN[Inbound] --> MQL
    OUT[Outbound] --> MQL
    PT[Partner] --> MQL
    MQL --> SQL --> OPP --> WIN
```

## Marketplace (two-sided)

```mermaid
flowchart TB
    subgraph Supply
        S1[List] --> S2[First txn]
    end
    subgraph Demand
        D1[Visit] --> D2[Purchase]
    end
    S2 -. liquidity .- D2
```

## Stage table (always pair with diagram)

| Stage | Buyer state | Channels | Assets | KPI | Current | Target |
|-------|-------------|----------|--------|-----|---------|--------|
| | | | | | | |

## Rendering rules

- Max 7 nodes on main path (collapse micro-steps)
- Show volumes **and** rates on edges when known
- If data unknown, label `?` and list in open questions
