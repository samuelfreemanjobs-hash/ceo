---
name: strategic-synthesis
description: Use when converting competitor findings into strategic insights, SWOT analyses, battle cards, positioning recommendations, executive briefs, or any output that includes a "so what". Triggers include "what does this mean for us", "should we worry about [competitor]", "build a battle card", "summarize the competitive landscape", "give me a SWOT", "what's the recommendation", or any explicit request for implication or action. Do NOT use for purely descriptive profile requests with no strategic question attached — use competitor-profiling for those. Do NOT use to fabricate a recommendation when the evidence base is too thin; flag the gap instead.
---

# Strategic Synthesis

Synthesis is where competitor _facts_ become _decisions_. This is the highest-stakes part of the agent's work and the easiest place to fail by overreaching.

**Used by:** Competition Analyzer (primary), Marketing Director (campaign context)

## The synthesis pyramid

Every synthesized output has three layers. Always present them in this order:

1. **Finding** — the synthesized statement (the "so what")
2. **Evidence** — the observations that support it
3. **Implication / recommendation** — what the user should do or consider

Synthesis fails when these collapse — when the finding is asserted without evidence, when evidence is presented without a finding, or when an implication is offered without grounding in either.

## Outputs this skill produces

### Battle Card (sales-facing)

**Purpose:** Help a salesperson win a deal where this competitor is in the picture.

**Structure (≤1 page):**

- **Headline differentiation** — the single sharpest thing your product does that theirs doesn't, in one sentence
- **Top 3 objections you will hear**, each with: the objection, the recommended response, the evidence backing the response
- **Where they win** — situations where you should consider not competing aggressively (honesty here protects credibility on everything else)
- **Where you win** — situations where you should lean in
- **Recent moves to be aware of** — anything that changes how the rep should pitch
- **Do not say** — things that would be untrue, easily disprovable, or that make us look defensive

Battle cards rot fast. Date them prominently. Set a 60-day refresh.

**Template:** `.github/templates/battle-card-tmpl.yaml` · **Example:** `competition-analyzer/worked-example.md`  
**Output path:** `docs/marketing/research/battle-cards/{competitor}-battle-card-{date}.md`

### SWOT

**Structure:**

- **Strengths** — what they genuinely do well, evidence-tagged
- **Weaknesses** — what they genuinely don't, evidence-tagged
- **Opportunities** — adjacent moves available to them given strengths
- **Threats** — incoming risks to them given weaknesses

A SWOT is _about the competitor_, not about you. A SWOT that says "their strength is they're cheaper than us" is conflating analysis with positioning. Keep the lens consistent.

Common failure: padding. Real SWOTs have 3–5 items per quadrant, not 12. If you can't distinguish the top 5 from the rest, you don't understand the competitor yet.

### Positioning brief

**Structure:**

- The competitive frame they want to win in
- The frame you want to win in
- Where the frames overlap and where they diverge
- The two or three positioning moves available to you, with tradeoffs

Positioning is _not_ feature comparison. Don't make it one.

### Move Alert

**Purpose:** Flag a competitor change that warrants action.

**Structure (short, single page):**

- **What changed** — one sentence
- **When** — date detected, date the change occurred
- **Why it matters** — the strategic interpretation, with confidence
- **What it might signal** — alternative interpretations (the obvious one is sometimes wrong)
- **Recommended next step** — investigate further, alert sales, update battle card, no action

**Output path:** `docs/marketing/research/alerts/{competitor}-{change}-{date}.md`

### Strategic brief (executive)

**Structure:**

- **Lede** — the recommendation, up front, one sentence. Bury nothing.
- **Why now** — what changed that surfaces this question now
- **Evidence** — the relevant findings, briefly
- **Risks of the recommendation** — what could make it wrong
- **Confidence** — how strong the evidence is and what would change the call

Executives read the lede and the risks. Optimize accordingly.

## Frameworks (use as lenses, not as templates)

- **Porter's Five Forces** — for industry-structural questions
- **Jobs to be Done** — for understanding why customers actually buy
- **Crossing the Chasm** — for category-formation timing questions
- **Wardley Mapping** — for evolution-and-commodification dynamics
- **3 Horizons** — for organizing what's near vs. far for them

Frameworks are tools, not templates. Don't force every output through a framework. Use the lens that makes the question clearer.

## Pattern recognition: common competitor moves

Recognize and name these when the evidence supports — but require multiple data points, not one:

- **Move upmarket** — pricing rises, sales-led motion strengthens, enterprise features prioritized, SMB de-emphasized
- **Move downmarket** — self-serve appears, PLG signals grow, free tier added or expanded
- **Platform play** — APIs, marketplace, integrations become hero messaging
- **Bundle play** — adjacent products acquired or built; cross-sell motion appears
- **Retreat** — quiet de-emphasis of a segment, pricing changes that don't make sense, hiring pulled back
- **Pivot** — category framing changes; ICP shifts; leadership changes precede a new narrative

A _name_ for a pattern is a finding. Don't assign one until you have evidence consistent with it _and_ inconsistent with the alternatives.

## Recommendation discipline

When the user asks "should we do X" or "what should we do":

1. **State the recommendation first**, in one sentence.
2. **Tag your confidence** — high / moderate / low (map to Confirmed / Likely / Unverified where appropriate).
3. **List the strongest evidence for** the recommendation (2–4 points).
4. **List the strongest evidence against** the recommendation (1–3 points). Always include this. A recommendation with no counter-evidence is suspicious.
5. **Identify the most decision-relevant unknown** — what would, if you learned it, change the recommendation?
6. **Note when this is judgment**, not data — explicitly. "The data supports either response; this is a strategic choice for the human."

A recommendation without counter-evidence is advocacy, not analysis.

## Required closing sections (all synthesized outputs)

1. **Sources** — every source cited
2. **Confidence summary** — Confirmed / Likely / Unverified
3. **Open questions** — what wasn't determinable and what would resolve it

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

## Anti-patterns

- **Narrative fitting.** Three data points don't make a trend. If you're working hard to make the data tell a clean story, the data may not have a clean story to tell.
- **Hindsight as insight.** Explaining a recent move as "obvious in retrospect" is not analysis. Ask whether you would have predicted it from the prior baseline.
- **Mirror-imaging.** Assuming the competitor will do what you would do in their position. They have different constraints and different information.
- **Capability ≠ intent.** Just because a competitor _could_ do something doesn't mean they will. Look for hiring, pricing, or messaging that signals intent before predicting moves.
- **Recommendation theater.** Recommendations that hedge to the point of saying nothing. "Continue monitoring" is a non-recommendation. If the evidence isn't there for a real call, say so — don't dress it up.
- **Confidence inflation under deadline pressure.** Time pressure does not change what the evidence supports. State confidence honestly and let the user decide how to act under uncertainty.
- **Battle cards without prohibited-claims check.** If used in external copy, route through compliance / `prohibited-claims-and-disclaimers` skill.

## When to refuse a synthesis

It is correct to decline a synthesis request when:

- The evidence base is too thin for any non-trivial finding to be supported
- The question requires data you don't have access to (e.g., their internal numbers) and any answer would be speculation
- The "right" answer is a value judgment about your own company's strategy, not a fact about the competitor

Don't manufacture a synthesis to satisfy a request. The honest answer ("I can't responsibly synthesize this given current evidence; here's what would close the gap") is more useful than a confident-sounding fabrication.
