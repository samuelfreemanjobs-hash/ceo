# Voice-of-customer mining

Extract patterns from public and user-supplied sources. **Triangulate** — never single-quote as gospel.

## Source tiers

| Tier | Sources | Use for |
|------|---------|---------|
| S | User's sales calls, support tickets, surveys | Objections, language, triggers |
| A | G2, Capterra, Trustpilot (patterns across 20+ reviews) | Themes, comparisons |
| B | Reddit, forums, community Slack | Pain language, alternatives |
| C | Social comments, one-off tweets | Hypotheses only |

## Mining process

1. **Collect** 30–50 data points minimum for pattern claims
2. **Tag** quotes: objection, trigger, outcome, alternative, praise
3. **Cluster** into top 5 themes
4. **Quote sparingly** — paraphrase patterns in Funnel Spec; cite 1–2 vivid phrases max

## G2 / review mining prompts

Search reviews for:

- "switched from" / "replaced"
- "wish" / "missing" / "frustrated"
- "worth it" / "ROI"
- "team won't use" / "adoption"

## Reddit mining

- `site:reddit.com [category] [pain keyword]`
- Note subreddit context (r/smallbusiness ≠ r/enterprise)

## Output artifacts

| Artifact | Format |
|----------|--------|
| Objection inventory | Top 5 with frequency estimate |
| Language bank | 10 phrases customers actually use |
| Trigger list | Events that precede search |
| Alternatives map | What they compare you to |

## Handoff to copy skill

Pass to `conversion-copywriting`:

- Top objection to pre-empt in hero
- Verbatim phrase for headline testing (A/B)
- Proof types customers mention (speed, support, price)

## Ethics & compliance

- Don't fabricate quotes or stats
- Flag when sample size is thin
- Route external claims to compliance before publish
