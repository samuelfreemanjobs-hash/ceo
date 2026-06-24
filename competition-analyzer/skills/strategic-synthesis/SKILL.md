---
name: strategic-synthesis
description: Use when converting competitive findings into SWOT, battle cards, positioning briefs, move alerts, and strategic recommendations. Invoke after evidence gathering is complete — synthesize last, not first.
---

# Strategic Synthesis

**Used by:** Competition Analyzer (primary), Marketing Director (campaign context)

## Synthesis rules

1. **Evidence on the table first.** No strategic conclusion before findings are listed with confidence tags.
2. **Separate observation, inference, hypothesis** in the synthesis layer.
3. **Recommendations carry confidence** — "We recommend X (Likely, based on …)" not "We must X."
4. **Invite human judgment** on strategic calls — make trade-offs legible.

## Output types

### SWOT

| | Content | Tag each item |
|---|---------|---------------|
| Strengths | | Confirmed/Likely/Unverified |
| Weaknesses | | |
| Opportunities (for us) | | |
| Threats (to us) | | |

### Battle card (≤1 page)

1. **Who they are** — one sentence
2. **Their pitch** — how they position (quoted if possible)
3. **Where we win** — 3 bullets with evidence
4. **Where they win** — 2 bullets (honest)
5. **Landmines** — claims not to make without substantiation
6. **Objection handlers** — top 3 objections + responses
7. **Questions to ask** — discovery questions that expose gaps

### Competitive landscape

- Define comparison dimensions upfront (pricing, ICP, features, GTM)
- Table: competitors × dimensions
- Highlight whitespace and crowding
- **Do not** rank without criteria stated

### Move alert

- **What changed** (observation)
- **When detected** / last verified
- **Why it matters** (inference — labeled)
- **Suggested response options** (not a single forced answer)
- **Urgency:** monitor | respond | escalate

### Strategic brief

1. Question framing
2. Key findings (bulleted, confidence-tagged)
3. Implications
4. Recommendation options (2–3 with trade-offs)
5. Open questions
6. Sources + confidence summary

## Anti-patterns

- Don't collapse "they raised prices" into "they're abandoning SMB" without evidence chain
- Don't produce battle cards without checking prohibited-claims rules if used in external copy
- Don't recommend copying competitor tactics without noting our positioning fit

## Handoff to Marketing Director

Return to Director:

```json
{
  "summary": "2-3 sentence executive summary",
  "artifact_path": "docs/marketing/research/...",
  "confidence_highlights": ["Confirmed: ...", "Unverified: ..."],
  "open_questions": ["..."]
}
```
