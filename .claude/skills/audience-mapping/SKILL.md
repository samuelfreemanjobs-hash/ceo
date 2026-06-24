---
name: audience-mapping
description: Use this skill any time the user needs to define, refine, or interrogate the audience for a funnel. Triggers on "who is this for", "target customer", "ICP", "persona", "audience research", "jobs to be done", "customer interview", "JTBD", "buyer", "who buys vs who uses", or whenever the user describes a business without specifying who they sell to. This is the foundation skill — invoke BEFORE funnel-frameworks, conversion-copywriting, or channel-playbooks if the audience isn't crisply defined. Forces specifics (firmographics, psychographics, triggers, objections, alternatives). Do NOT use for funnel structure alone, channel selection, or metric modeling.
---

# Audience Mapping

**Phase:** Discovery (1), Optimize (6) · **Run first** when audience is vague

## Purpose

Produce an **evidence-based audience definition** that every downstream skill can execute against. No "Marketing Mary." No build until minimum viable audience context exists.

## Minimum viable discovery (6 questions)

If user resists full interview, get these before any funnel build:

1. **Offer** — what they buy, price band
2. **Audience** — who buys vs who uses
3. **Primary goal** — one conversion metric
4. **Current state** — rough funnel or "net new"
5. **Constraint** — budget, timeline, team
6. **Alternative** — what they use today (including nothing)

## Full ICP interview (15 questions, prioritized)

### Tier 1 — Must have (ask first)

1. Who **signs the check** vs who **uses** the product daily?
2. **Firmographics/demographics:** company size, industry, geo, role/title
3. What **triggered** them to look for a solution *now*?
4. What were they using **before** (competitor, DIY, manual)?
5. Top **3 objections** to buying (rational + emotional)
6. What does **success** look like 90 days after purchase?

### Tier 2 — Sharpen copy and channels

7. Where do they **hang out** (communities, events, media)?
8. How do they **search** for solutions (Google queries, peer ask)?
9. What **language** do they use for the problem (verbatim if possible)?
10. Who else must **approve** the purchase (IT, legal, finance)?
11. What's the **urgency** level (hair on fire vs nice-to-have)?
12. **Budget authority** — band and who holds it?

### Tier 3 — Optimize and expand

13. What **alternatives** did they seriously evaluate?
14. What would make them **switch back** to the old way?
15. What **proof** do they trust (peers, analysts, reviews, demos)?

## JTBD framework

Capture three job types per segment:

| Job type | Prompt | Example (async standup tool) |
|----------|--------|-------------------------------|
| **Functional** | What task must get done? | Run standups without live meetings |
| **Emotional** | How do they want to feel? | In control, not nagging the team |
| **Social** | How do they want to be perceived? | EM who runs a tight async team |

### Forces of progress

| Force | Question |
|-------|----------|
| Push | What's broken about the status quo? |
| Pull | What's attractive about the new solution? |
| Anxiety | What fears block switching? |
| Habit | What inertia keeps them on the old way? |

**Funnel implication:** Anxiety + habit → objections and activation risk.

## Persona template (evidence-based)

```markdown
### [Segment label — not a fake name]
- **Role / segment:** 
- **Buyer vs user:** 
- **Trigger event:** (observed or from VoC)
- **Success metric they care about:** 
- **Top objection:** 
- **Alternative considered:** 
- **Proof they trust:** 
- **Voice snippet:** (optional, 1 phrase from VoC)
```

**Reject** personas with only demographics and a stock photo narrative.

## Trigger events inventory

Document what causes **search behavior**:

| Category | Examples |
|----------|----------|
| Organizational | New hire, funding, reorg, team growth |
| Operational | Tool failure, process breakdown, compliance |
| Competitive | Vendor price change, sunset, bad support |
| Personal | Promotion, new mandate, peer recommendation |

Tie triggers to **TOFU content and ad angles** in handoff to `conversion-copywriting`.

## Objection inventory

List top 5 reasons people don't buy:

| # | Objection | Type | Pre-empt in (stage/asset) |
|---|-----------|------|---------------------------|
| 1 | | rational / emotional / procedural | |
| 2 | | | |

**Procedural** = procurement, security review, legal — common in enterprise; route to BOFU assets.

## Alternatives map

| Alternative | Why chosen | Our wedge |
|-------------|------------|-----------|
| Incumbent tool | | |
| DIY / manual | | |
| Competitor X | | |
| Do nothing | | |

"If do nothing wins" → urgency and trigger work needed in TOFU.

## Voice-of-customer extraction

When user provides or you research via web_search:

1. Collect 30+ data points before claiming a pattern
2. Tag: objection, trigger, outcome, alternative, praise
3. Cluster top 5 themes
4. Pass **language bank** to `conversion-copywriting`

See `references/voc-mining.md` for G2, Reddit, support ticket mining.

## B2B vs B2C routing

| Signal | Load reference |
|--------|----------------|
| Firmographics, titles, pipeline | `references/b2b-firmographics.md` |
| Lifestyle, identity, DTC | `references/b2c-psychographics.md` |

## Output format

```markdown
## Audience (for Funnel Spec recap)
**ICP:** [≤2 lines]
**Buyer / User:** [titles]
**Trigger:** [event]
**Top objection:** [one line]
**Alternative:** [incumbent]

### Objection inventory
[table]

### Alternatives map
[table]
```

Brief recap must fit **4 lines max** in final Funnel Spec.

## Do not use when

- Audience already documented in brief with buyer/user/objection → skip to confirm only
- User asks only for funnel diagram → `funnel-visualization` (but flag if ICP missing)
- Pure math request → `funnel-metrics`

## Anti-patterns

| Mistake | Fix |
|---------|-----|
| Skipping discovery on "fix my funnel" | Ask for rates + buyer first |
| Generic persona | Require trigger + objection + alternative |
| Single-quote proof | Triangulate; label confidence |
| Assuming buyer = user | Explicitly ask in B2B |

## Coordination

- **Before:** Nothing — often first skill
- **To funnel-frameworks:** ICP informs PLG vs sales-led choice
- **To conversion-copywriting:** Objections, voice snippets, buyer hero
- **To channel-playbooks:** Where audience spends time
- **Optimize phase:** Re-validate assumptions that failed in tests

## Quality checklist

- [ ] Buyer vs user identified (B2B)
- [ ] ≥1 trigger event documented
- [ ] ≥3 objections listed
- [ ] ≥2 alternatives mapped
- [ ] No fictional persona names without evidence
- [ ] Brief recap ≤4 lines ready for Funnel Spec

## References

- `references/b2b-firmographics.md`
- `references/b2c-psychographics.md`
- `references/voc-mining.md`
