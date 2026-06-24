# Competition Analyzer Agent

A single-agent system equipped with composable Skills for decision-grade competitive intelligence.

---

## Architecture choice and rationale

**Pattern:** Single agent + Skills. The simplest architecture that meets the need, per _Building Effective AI Agents_.

**Why not multi-agent collaborative (as the guide's "Competitive Intelligence Gathering" example suggests)?** Competitive intelligence is multi-domain — pricing, product, marketing, financials, social signals, strategic moves — which makes a collaborative swarm pattern _look_ like the right fit. But these domains **compose more than they conflict**. They synthesize into one coherent picture of a competitor. A single agent equipped with specialized Skills can carry that synthesis end-to-end without:

- the ~10–15x token cost of multi-agent coordination
- the emergent-behavior risk of peer-to-peer negotiation
- the observability burden of debugging cross-agent communication
- the coordination overhead when domains turn out to be tightly coupled (and in competitive intel they always are — a pricing change is also a positioning change is also a GTM signal)

**When the architecture should evolve.** Move to hierarchical multi-agent (supervisor + specialists) when **any one** of these becomes true:

1. Average investigation context exceeds the model's window even with context editing and memory tools (pricing teardowns + financial filings + 12 months of press + sales call notes is the threshold to watch).
2. Latency from sequential sub-investigations becomes a blocker — at that point, parallel sub-agents per domain are worth the token cost.
3. The Skills count exceeds ~10 and trigger reliability starts degrading (the description-matching gets noisy).
4. You need different models for different sub-tasks — e.g., a cheaper model for high-volume monitoring sub-agents and a frontier model for strategic synthesis.

Don't pre-build for these. Instrument and measure first.

---

## What's in this package

```
competition-analyzer/
├── README.md                                       (this file)
├── system-prompt.md                                Agent definition — paste into API system parameter
├── CLAUDE.md                                       Persistent operating principles
├── worked-example.md                               End-to-end trace on a real competitor (Linear)
└── skills/
    ├── gtm-competitor-analysis/SKILL.md         Public GTM, funnels, ad evidence, monitoring
    ├── competitor-profiling/SKILL.md               Systematic profile-building methodology
    ├── pricing-teardown/SKILL.md                   Specialized pricing analysis methodology
    ├── source-evaluation/SKILL.md                  Reliability, recency, bias framework
    └── strategic-synthesis/SKILL.md                Findings → insight → recommendation
```

**Orchestration integration:** Agent persona also lives at `.github/agents/competition-analyzer.md` (mirrored to `.claude/`, `.gemini/`) for CEO / Marketing Director Task-tool routing.

---

## Tools / MCP this agent expects

**Required**

- `web_search` — for discovery of public competitor signals
- `web_fetch` — for direct reading of competitor sites, pricing pages, docs, blog posts

**Strongly recommended**

- A CRM connector (Salesforce / HubSpot MCP) — for internal win/loss notes, which are the single highest-signal source of competitive intel
- Document ingestion — for analyst reports (Gartner, Forrester), 10-Ks, S-1s

**Optional, in priority order**

- Job board search (LinkedIn / Indeed MCP) — hiring is a leading indicator of strategy
- App-store and changelog feeds — for product velocity signals
- Pricing aggregators — for SaaS pricing teardowns
- News/PR feeds with structured deduplication

---

## How to deploy

**Option A — Claude API (production):**

1. Use `system-prompt.md` as the `system` parameter on `/v1/messages`.
2. Append the contents of all `skills/*/SKILL.md` files into the system prompt, OR — better — host the skill folder and load via the Skills mechanism on the Claude Developer Platform.
3. Configure the tools listed above. The system prompt assumes `web_search` and `web_fetch` are available; gate skills that need other tools behind the relevant connectors.

**Option B — Claude Code / agent harness (development, iteration):**

1. Drop this entire folder into your project root.
2. The `CLAUDE.md` is auto-loaded by Claude Code.
3. Skills are discovered by the harness from `skills/*/SKILL.md`.

**Option C — Claude.ai Project (research, lightweight use):**

1. Upload the files into a Claude Project.
2. Put `system-prompt.md` content into the Project's custom instructions.

**Option D — CEO orchestration (this repo):**

1. Invoke via Task tool: `subagent_type: competition-analyzer`
2. Or route through Morgan (`marketing-director`) for campaign-context competitive work
3. Artifacts land in `docs/marketing/research/`

---

## Quality contract

The agent commits to:

1. **Distinguishing observation from inference** in every claim.
2. **Attaching a confidence level** — _Confirmed / Likely / Unverified_ — to every finding.
3. **Citing sources** with a "last verified" timestamp.
4. **Declining to fabricate** when evidence is insufficient. "I don't have a verified source for that" is always an acceptable answer.
5. **Flagging when a question needs human judgment** rather than more data — e.g., strategic bets, ethical calls.

These are enforced by the system prompt and reinforced in CLAUDE.md.

---

## Anti-patterns this design avoids

- **Hallucinated competitor features.** Source evaluation skill + explicit confidence levels make fabrication structurally costly.
- **Stale intelligence.** Every finding carries a "last verified" stamp; recency is part of the data model, not an afterthought.
- **Narrative fitting.** Strategic synthesis skill requires evidence-tagged inferences and flags pattern-matching that outruns the data.
- **Recency bias.** Profile structure forces a baseline view, not just a "recent moves" view.
- **Over-engineering.** Starts as one agent. Multi-agent is a documented next step, not the starting point.
