# B2B firmographics reference

Use when building ICP for B2B funnels. Pair with `voc-mining.md` for evidence.

## Core firmographic dimensions

| Dimension | Questions to answer |
|-----------|---------------------|
| Company size | Employees, revenue band, eng headcount |
| Industry / vertical | NAICS, sub-vertical nuance |
| Geography | HQ, operating regions, compliance zones |
| Tech stack | Integrations required (Slack, Salesforce, etc.) |
| Growth stage | Seed, growth, enterprise |
| Budget band | Tool spend authority, procurement process |

## Economic buyer vs champion

| Role | Typical title | Cares about |
|------|---------------|-------------|
| Champion | IC, team lead | Daily workflow, time saved |
| Economic buyer | Manager, VP, Director | ROI, team adoption, risk |
| Blocker | IT, Legal, Finance | Security, compliance, contracts |

**Funnel implication:** TOFU may target champion; BOFU copy must speak to economic buyer.

## Firmographic scoring (simple)

Score 0–2 per dimension; threshold for MQL:

```
Industry fit + Size fit + Stack fit + Intent signal ≥ 5 → qualified
```

## Segment labels (avoid fluff)

Bad: "Mid-market innovators"  
Good: "Engineering managers, 10–50 eng, Series A–C SaaS, Slack-native"

## Trigger events (B2B)

- New hire in role (EM, RevOps, CMO)
- Funding round
- Tool contract renewal
- Team growth / reorg
- Compliance or audit event
- Competitor price change

## Objection patterns by firmographic

| Segment | Common objection |
|---------|------------------|
| SMB | Price, time to implement |
| Mid-market | Team adoption, integration |
| Enterprise | Security, vendor risk, procurement |

## Output for Funnel Spec

```markdown
**ICP:** [role] at [company type], [size], [geo]. Buyer: [title]. User: [title].
**Trigger:** [event]. **Alternative:** [incumbent]. **Top objection:** [one line].
```
