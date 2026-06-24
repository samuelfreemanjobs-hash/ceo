# Worked Example: Battle Card for Linear

This is a complete trace of the Competition Analyzer agent running on a real request, against a real competitor, with real sources. It shows how the system prompt, CLAUDE.md, and four Skills compose end-to-end.

> **Why Linear?** Public pricing, distinctive positioning, visible strategic moves in the AI era. Useful as a demonstration; nothing here is internal to Linear, all sources are public.
>
> **Re-verify before use.** Pricing and product change. Treat retrieval dates as part of the data model.

---

## The request

> **User:** _"Linear keeps coming up in our customer conversations. Build me a competitive battle card for our sales team — we sell project/issue tracking into engineering teams at startups and growth-stage companies."_

---

## Phase 1 — Clarification (per CLAUDE.md)

The default workflow says to ask _one_ clarifying question only when the lens is genuinely ambiguous. Here, lens (sales-facing battle card) is clear. ICP overlap is clear. One question is still worth asking because it changes the framing of "where they win":

> **Agent:** _"One quick clarification: should this battle card assume an apples-to-apples positioning fight (we're a direct issue-tracking alternative), or are we differentiated on an adjacent axis (e.g., we serve cross-functional teams, or we do something Linear doesn't)? Different framings produce different objection-handlers."_

> **User:** _"Direct alternative. Treat Linear as the main competitor."_

Now the lens is fixed: direct competitor, sales-facing, engineering ICP at startup/growth-stage. Proceed.

---

## Phase 2 — Decomposition and planning

The agent applies the default workflow from CLAUDE.md:

```
Sub-investigations identified:
  1. Pricing teardown                      → pricing-teardown skill
  2. Positioning and ICP                   → competitor-profiling §4, §5
  3. Product strengths/limitations          → competitor-profiling §2, §8
  4. Recent strategic moves (12 mo)         → competitor-profiling §7
  5. Source quality across all of above    → source-evaluation (continuous)
  6. Synthesis into battle card             → strategic-synthesis (last)

Parallelizable: 1, 2, 3, 4 are independent. Run concurrently.
Sequential: 6 depends on 1–4. 5 runs throughout.

Skills loaded: pricing-teardown, competitor-profiling, source-evaluation, strategic-synthesis.
```

---

## Phase 3 — Parallel tool execution

Three search calls and one fetch fired concurrently:

```
[web_search]   "Linear app pricing tiers 2026"          → 8 sources returned
[web_fetch]    https://linear.app/pricing                → primary source
[web_search]   "Linear app new product launch 2026 agents AI"  → 8 sources returned
```

---

## Phase 4 — Findings with source evaluation applied

### Pricing (pricing-teardown skill in action)

**The conflict.** Secondary sources gave inconsistent pricing for the Business tier: $16, $30, and a "68% cut from $50 to $16 in seven months" narrative. Per source-evaluation, when sources conflict, go to the primary source.

`web_fetch(linear.app/pricing)` resolved the conflict:

| Tier | Price | Unit | Notes |
|------|-------|------|-------|
| Free | $0 | — | Unlimited members, 2 teams, 250 issues, Linear Agent (beta), Agent platform |
| Basic | $10 | per user/month, **annual only** | 5 teams, unlimited issues, admin roles |
| Business | $16 | per user/month, **annual only** | Unlimited teams, private teams, Triage Intelligence, Code Intelligence (beta), Insights, Asks, Zendesk/Intercom |
| Enterprise | Custom | annual only | SAML+SCIM, audit log, HIPAA, advanced org modeling, account management |

**Confidence:** All four tiers — **Confirmed** (primary source, retrieved 2026-06-14).

The "68% price cut" claim from one secondary source: **Unverified** — only one source asserts it, and primary source can't confirm prior pricing. _This is exactly the failure mode source-evaluation guards against — three independent-looking articles can all trace back to one upstream claim._

**Hidden tier inference (Enterprise):**

- Estimated ACV: $20K–$80K based on Vendr median of $22,800/year and reported sales motion. **Likely.**
- Likely capabilities: everything in Business + SSO/SCIM, audit logs, HIPAA, dedicated CSM. **Confirmed** (pricing page lists these).
- Sales process: full enterprise cycle with security review and procurement. **Likely.**

**Pricing model classification:**

- Unit: **per-seat** (pure)
- Commitment: **annual required** on Basic, Business, Enterprise
- Free tier: feature- and quota-limited (250 issues / 2 teams), forever-free
- Self-serve ceiling: Business tier — Enterprise requires sales contact

**Strategy interpretation:** Value-based with PLG-style funnel, transitioning toward enterprise. Free tier exists to win bottoms-up adoption inside engineering teams; the 250-issue cap forces quick upgrade once a team is real. The recent introduction of Enterprise-only governance features and the "issue tracking is dead" repositioning suggest movement upmarket. **Likely.**

### Positioning (competitor-profiling §4)

**Hero claim, June 2026:** _"The system for product development. Purpose-built for planning and building products. Designed for the AI era."_ (Source: linear.app homepage, 2026-06-14. **Confirmed.**)

**Note the shift.** Older positioning was "the fast issue tracker." Current positioning is "system for product development" with AI-era framing. This is a **deliberate category move**, not just refreshed copy.

**Differentiation points emphasized:**

1. Speed (47ms API responses cited externally, **Likely** — single source, but consistent with widely reported perception)
2. Opinionated workflow (low configuration overhead) — **Confirmed**
3. Agent-native: Linear Agent, MCP support, Code Intelligence — **Confirmed**
4. Engineering-first design — **Confirmed**

**Conspicuous absences:** No HR / legal / cross-functional pitches anywhere. They are _not_ trying to be a Jira-Service-Management or Asana-style horizontal play. This is a strength (focus) and a vulnerability (limits expansion within an account).

### Recent moves (competitor-profiling §9)

Last 12 months, by date:

| Date | Move | Confidence |
|------|------|------------|
| Sep 2025 | Cursor background agents can be assigned issues directly from Linear | Confirmed |
| Oct 2025 | Triage Intelligence launched | Confirmed |
| Feb 2026 | MCP server expanded with milestones/updates | Confirmed |
| Mar 24, 2026 | **Linear Agent public beta** — flagship launch | Confirmed |
| Mar 26, 2026 | CEO Karri Saarinen publicly declares _"issue tracking is dead"_ | Confirmed (The Register interview) |
| May 14, 2026 | Linear Agent gains codebase-reading capability | Confirmed |
| May 28, 2026 | **Diffs** launched — code review inside Linear | Confirmed |
| Jun 11, 2026 | CEO post on how agents are forcing code-review changes | Confirmed |

**Pattern recognition (per strategic-synthesis):** This is a **platform play**. Three signals consistent with it: (a) MCP-first architecture, (b) explicit category repositioning, (c) moving up the stack from issue tracking into code review (Diffs). Not just AI features bolted on — the product surface is being rebuilt around the assumption that agents are first-class users. **Likely → Confirmed** given the consistent multi-quarter cadence.

### Strengths/weaknesses synthesis (competitor-profiling §8)

**Real strengths:**

- Speed and UX polish — well-attested, repeatedly cited
- Strong brand in engineering ICP — 33,000 companies (Confirmed, primary source)
- Coherent agent-native product story — earliest mover among PM tools to take agents seriously as users of the product, not just features in it
- Opinionated defaults — high time-to-value for teams that fit the workflow

**Real weaknesses (and where to attack):**

- **Annual-only paid billing** — real procurement friction for budget-uncertain teams. (Confirmed.)
- **Free-tier 250-issue cap is aggressive** — teams hit it within weeks, then face the annual commitment decision. Some bounce. (Likely — multiple secondary sources, consistent with the cap's existence.)
- **Engineering-only by design** — does not serve marketing, HR, legal, support-only teams. An account that needs cross-functional PM has to buy two tools. (Confirmed.)
- **Limited customization** — opinionated workflow is a strength for green-field teams and a weakness for teams with established processes or compliance-driven workflows. (Confirmed.)
- **Smaller marketplace than Jira** — 3,000+ Jira apps vs Linear's curated integrations. (Likely.)
- **Pricing trajectory uncertain** — secondary sources disagreed on whether Business tier has been volatile. **Unverified.** Worth monitoring; not worth claiming.

---

## Phase 5 — Strategic synthesis → Battle Card

The strategic-synthesis skill produces the final artifact:

---

```
═════════════════════════════════════════════════════════════
  BATTLE CARD — Linear
  For: Sales team selling project/issue tracking to startup &
       growth-stage engineering teams
  Last verified: 2026-06-14 · Refresh: 2026-08-13 (60 days)
═════════════════════════════════════════════════════════════

  HEADLINE
  Linear is the strongest engineering-only PM tool on the
  market and is repositioning aggressively around AI agents.
  Compete on flexibility, cross-functional fit, and procurement
  terms — not on speed or polish.


  TOP 3 OBJECTIONS YOU WILL HEAR

  1. "Linear is faster / nicer to use."
     RESPONSE: Acknowledge — Linear's UX is genuinely good.
     Pivot to the question of fit: Linear's speed comes from
     opinionated defaults that don't bend. Ask the prospect to
     describe one workflow they currently rely on that doesn't
     fit a cycles/projects/triage model. If they can't, Linear
     is a real fit; if they can, that workflow is the wedge.

  2. "Linear has the agents/AI story."
     RESPONSE: Linear has the *narrative*. Linear Agent and
     Code Intelligence are both in beta as of June 2026. Ask
     what specific agentic workflow they actually need to run
     in production today, then compare on that specific case
     rather than the launch announcement.

  3. "Linear is what engineers want."
     RESPONSE: For pure engineering teams that fit Linear's
     workflow, this is true. For companies where PM also has
     to coordinate with marketing, support, compliance, or
     ops, Linear is one of two tools they'll buy. Reframe
     from "what engineers want" to "what the company needs to
     standardize on."


  WHERE WE WIN

  • Cross-functional PM needs (Linear is engineering-only)
  • Heavy customization or compliance-driven workflows
  • Buyers who need monthly billing (Linear is annual-only on
    all paid tiers)
  • Teams with established Jira-style processes they can't
    rebuild from scratch
  • Risk-averse buyers wanting a marketplace of integrations


  WHERE LINEAR WINS — BE HONEST

  • New engineering teams choosing greenfield
  • Teams that explicitly want to ship faster by adopting an
    opinionated system
  • AI-forward eng orgs wanting to delegate work to coding
    agents (Cursor, Claude Code) via MCP today
  • Buyers who prize UX and speed above all else
  Do not compete head-on in these scenarios. Qualify out
  rather than discount your way in.


  RECENT MOVES TO BE AWARE OF (60 days)

  • Jun 11 — CEO post on agents reshaping code review
  • May 28 — Diffs launched (code review inside Linear)
  • May 14 — Linear Agent can read codebases
  Linear is moving up-stack from issue tracking into code
  review and product orchestration. If a prospect mentions
  "consolidating tools," this is the consolidation story
  Linear is selling. Have a counter-story ready.


  PRICING (verified 2026-06-14)

  Free       $0           2 teams, 250 issues cap
  Basic      $10/u/mo     5 teams, unlimited issues — ANNUAL ONLY
  Business   $16/u/mo     Unlimited teams, AI features — ANNUAL ONLY
  Enterprise Custom       SSO, SCIM, audit, HIPAA
  Median customer pays ~$22,800/year (Vendr data; Likely).


  DO NOT SAY
  • Don't claim Linear is "expensive." At $10–$16/seat it is
    competitively priced; the friction is annual-only billing,
    not the dollar amount. Attack the term, not the price.
  • Don't claim Linear "doesn't have AI." They have the strongest
    AI/agent story in the category. Argue maturity and breadth,
    not existence.
  • Don't reference unverified pricing histories ("they raised
    prices by X%") — secondary sources disagree and primary
    source can't confirm.


  CONFIDENCE SUMMARY
  Confirmed: pricing tiers, positioning shift, AI-product
             launches, customer count (33k+), annual-only
             billing
  Likely:    Vendr median ACV ($22,800), engineering-only ICP,
             platform-play interpretation
  Unverified: pricing history / volatility, exact enterprise
             ACV ranges, internal sales motion details

  OPEN QUESTIONS
  • How is Linear Agent performing in real adoption (vs.
    announcement)? — would resolve with customer reference
    data or G2 review velocity
  • Are they discounting heavily on the annual-only term? —
    would resolve with first-party win/loss data from our
    own sales team
```

**Example artifact path:** `docs/marketing/research/battle-cards/linear-battle-card-example-2026-06-14.md`

---

## Phase 6 — Reflection: what this example demonstrates

A few things the architecture did that are worth naming:

### 1. The skills composed without coordination overhead

`competitor-profiling`, `pricing-teardown`, `source-evaluation`, and `strategic-synthesis` all ran in a single agent's reasoning loop. No supervisor, no handoffs, no shared message bus. The methodology came from the skills; the synthesis happened in one place. This is the case for the single-agent architecture made concrete — the domains _composed_ rather than required orchestration.

### 2. Source-evaluation prevented a real error

Three secondary sources gave conflicting pricing for the Business tier. Without source-evaluation requiring primary verification, the agent could easily have published "Linear cut prices 68% in seven months" as a finding. With primary verification, that claim got correctly tagged **Unverified** and was excluded from the battle card. _This is the failure mode the skill exists to prevent._

### 3. Confidence labels carried real signal

The battle card surfaces what's Confirmed, what's Likely, and what's Unverified. A sales rep using this card knows which claims are bulletproof and which carry risk if challenged. That discipline came from the system prompt's three-tier confidence vocabulary, applied consistently in every skill.

### 4. Strategic-synthesis included counter-evidence

The "Where Linear Wins — Be Honest" section exists because strategic-synthesis explicitly requires counter-evidence on every recommendation. A battle card that pretends Linear has no strengths is not credible and not useful. Sales reps quickly learn to ignore advocacy and trust analysis — the skill is built around that.

### 5. The agent asked one clarifying question, not three

CLAUDE.md says "Default to _one_ clarifying question, not three." That constraint shows up in the actual interaction — direct/adjacent framing was the one thing that genuinely changed the output structure, so it was the one thing asked.

### 6. What would justify upgrading to multi-agent?

This task ran comfortably in a single agent. Roughly 4 tool calls, ~10K tokens of context, one structured output. The multi-agent threshold (per README's evolution path) would be triggered by, say:

- A **landscape analysis** of 8 competitors at this depth — context window pressure becomes real, parallel sub-agents per competitor start paying for themselves
- **Continuous monitoring** of 20+ tracked competitors — different agents per surveillance domain (pricing watch, hiring watch, news watch) would let cheaper models handle the high-volume work and reserve the frontier model for synthesis
- A **deep M&A diligence** workflow where financial analysis, technical due diligence, and customer research each need their own sustained investigation

None of those apply here. Single agent + Skills was the right call, and the example shows what that looks like in practice.

---

## Sources (for the analysis above)

| Source | URL | Retrieved | Reliability |
|--------|-----|-----------|-------------|
| Linear pricing page | https://linear.app/pricing | 2026-06-14 | Tier S — primary |
| Linear homepage | https://linear.app/ | 2026-06-14 | Tier S — primary |
| Linear AI page | https://linear.app/now/ai | 2026-06-14 | Tier S — primary |
| Linear changelog (Linear Agent intro) | https://linear.app/changelog/2026-03-24-introducing-linear-agent | 2026-06-14 | Tier S — primary |
| The Register — "issue tracking is dead" | https://www.theregister.com/2026/03/26/linear_agent/ | 2026-06-14 | Tier A — reputable trade press, named author |
| Vendr — Linear pricing data | https://www.vendr.com/marketplace/linear | 2026-06-14 | Tier B — aggregator, useful for median ACV, weaker for tier accuracy |
| Multiple SaaS pricing trackers | (various) | 2026-06-14 | Tier B–C — flagged disagreement on Business tier history, treated as Unverified |
