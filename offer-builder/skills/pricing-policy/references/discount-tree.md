# Discount decision tree

```
START: scope received from Solution Architect
  │
  ├─► pricing_engine.get_rates(scope)
  │
  ├─► pricing_engine.segment_discount(segment)
  │     └─► Record rule + amount per SKU
  │
  ├─► Strategic adder eligible?
  │     ├─ competitive? → dossier.competitors_mentioned non-empty
  │     ├─ multi-year?  → term_months ≥ 24
  │     ├─ logo?        → CRM strategic_logo_flag
  │     └─ volume?      → qty ≥ threshold
  │     └─► Pick ONE adder (no stack with multi-year + logo)
  │
  ├─► Compute aggregate_discount_pct
  │     ├─ > 40% → requires_approval=true, approver_role=CRO
  │     ├─ > 25% → requires_approval=true, approver_role=VP-Sales
  │     └─ else  → requires_approval=false
  │
  └─► floor_check: all net_price ≥ floor_price[SKU]
        ├─ fail → floor_check_passed=false, flag Director
        └─ pass → emit pricing-schema.json
```

## Edge cases

- **Renewal with uplift:** apply renewal rate table, not new-logo segment discount
- **Pilot:** use pilot rate card; no multi-year adder on term < 12
- **Currency mismatch:** stop — flag Director unless billing override documented
