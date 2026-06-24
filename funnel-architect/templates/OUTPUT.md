# Funnel Spec — output template

Agent fills this structure. Save to: `docs/marketing/funnels/{slug}-funnel-spec-{YYYY-MM-DD}.md`

---

## 1. Brief recap

≤4 lines: audience, offer, goal, constraints.

---

## 2. Funnel diagram

```mermaid
flowchart LR
    %% Replace with stage-specific diagram
```

---

## 3. Stage table

| Stage | Buyer state | Channels | Assets | KPI | Current | Target |
|-------|-------------|----------|--------|-----|---------|--------|
| | | | | | | |

---

## 4. Per-stage deliverables

### Stage: {name}

**Headline / hero**  
(copy)

**Email / sequence** (if applicable)  
(copy)

**Page structure** (if applicable)  
- Section bullets

**Ad angles** (if applicable)  
- Angle 1…

*(Repeat per stage — collapse in doc if long)*

---

## 5. Metrics & instrumentation

| Event / KPI | Tool | Stage |
|-------------|------|-------|
| | | |

**Attribution note:** (which model and why)

---

## 6. Projected unit economics

- Assumptions listed explicitly
- Current vs target projection (from code_execution)
- Sensitivity on weakest stage

---

## 7. Top 3 tests (ICE)

| # | Test | Impact | Confidence | Ease | ICE | Run order |
|---|------|--------|------------|------|-----|-----------|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

---

## 8. Open questions

- What would change this recommendation?
- Assumptions to validate first

---

## Trace (optional)

`trace_id:` · `skills_invoked:` · `tools_called:` — see `observability/trace-schema.json`
