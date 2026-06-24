# Voice calibration reference

Load when brand voice is unclear or copy fails the voice check in the evaluator loop.

## Quick calibration interview

Ask the user for 2–3 examples:

1. Copy they **love** (internal or competitor)
2. Copy they **hate** (and why)
3. One **customer email or review** in their words

## Five voice dimensions

| Dimension | Spectrum | How to detect |
|-----------|----------|---------------|
| Formality | corporate → irreverent | Contractions, jargon, emoji |
| Pace | long-form → punchy | Avg sentence length, paragraph size |
| Vocabulary | technical → accessible | Acronyms, explainers |
| POV | founder I → we → they | Subject of sentences |
| Humor | none → absurd | Jokes, irony, memes |

Document choices in output:

```markdown
**Voice profile:** professional + accessible, punchy, mixed vocab, founder "I", dry humor
```

## Defaults by audience (when no examples)

| Audience | Default voice |
|----------|---------------|
| B2B SMB | Professional, conversational, you-focused |
| Enterprise | Formal, proof-heavy, risk-aware |
| DTC consumer | Casual, punchy, benefit-led |
| Dev tools | Technical-accessible, no marketing fluff |
| Info products | Authoritative + personal story |

Flag: `[VOICE ASSUMPTION — tune before ship]`

## Rewrite patterns

| Generic SaaS | Calibrated |
|--------------|------------|
| "Leverage our platform" | "Run standups in Slack" |
| "Best-in-class solution" | "287 teams switched last quarter" |
| "We're excited to announce" | Cut — lead with reader outcome |
| "Synergy", "robust", "seamless" | Replace with measurable claim |

## VoC → voice

Pull phrases from `audience-mapping` swipe file. Customer words > marketer words.

## Compliance handoff

Before external publish: Morgan → `compliance-agent` for claims, competitor refs, regulated industries.
