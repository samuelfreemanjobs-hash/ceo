---
name: channel-playbooks
description: Use this skill whenever the user is selecting, evaluating, or designing tactics for a specific marketing channel — paid search, paid social (Meta/LinkedIn/TikTok/X), SEO, content, email, webinars, outbound sales, partnerships, affiliate, influencer, direct mail, podcast, community, events. Triggers on channel names, "where should I advertise", "best channel for X", "should I do Google Ads or Meta", "outbound vs inbound", "channel mix", "CPL", "which channel". Provides per-channel playbook mechanics, math, creative patterns, KPIs, and failure modes. Matches channels to business stage, ACV, and audience. Do NOT use for funnel stage naming (funnel-frameworks), full copy drafts (conversion-copywriting), or attribution modeling alone (funnel-metrics).
---

# Channel Playbooks

**Phase:** Map (3), Build (4) · **Requires:** audience + framework stages from prior skills

## Purpose

Assign **channels to buyer-state stages** with honest fit assessment. Pick 1–2 channels to dominate before sprawl.

## Channel concentration principle

> Dominate 1–2 channels before adding a third.

Flag when user requests 5+ channels at early stage. Recommend sequence: prove unit economics on one, then expand.

## Channel-fit matrix (summary)

| Channel | Fits when | Poor fit when | Typical ACV |
|---------|-----------|---------------|-------------|
| Paid search | High intent, known category | Pre-category, no search volume | $500+ |
| Meta ads | B2C, visual, fast path to buy/lead | Niche B2B, long enterprise cycle | Any B2C |
| LinkedIn ads | B2B, title targeting | Low ACV consumer | $5K+ |
| SEO / content | 6–18 mo horizon, searchable pain | Need revenue in 30 days | Any |
| Email | Owned list, lifecycle triggers | No capture, no list | Any |
| Cold outbound | High ACV, defined ICP list | Self-serve $9–49/mo | $15K+ |
| Partnerships | Complementary audiences | No partner manager | Varies |
| Community | Identity, dev/prosumer | Commodity, no moderation | Varies |
| Webinars | Complex B2B, education needed | Impulse DTC | $3K+ |
| Events | Enterprise trust, high touch | Low budget, PLG scale | $25K+ |

## Per-channel assignment template

For each channel × stage assignment, document:

```markdown
### [Channel] @ [Stage name]
1. **Mechanics** — how it moves buyers at this stage
2. **Math** — CPL/CAC range (cite source or label heuristic)
3. **Creative patterns** — what converts (not full copy)
4. **KPIs** — primary + guardrail
5. **Failure modes** — common mistakes
```

Load `references/channels/{channel}.md` for depth.

## Channel mix by business type

| Business | Primary (start here) | Secondary (after proof) |
|----------|---------------------|-------------------------|
| PLG SaaS | SEO, product-led referral | Paid search brand, comparison pages |
| Sales-led B2B | Outbound + LinkedIn, content MOFU | Paid search BOFU, events |
| DTC | Meta/TikTok, email retention | Influencer, Google Shopping |
| Services | Referral, LinkedIn organic | Webinar, SEO local |
| Marketplace | Supply outbound/partners; demand paid social | SEO both sides |

## Honest assessments (say these out loud)

| Situation | Say |
|-----------|-----|
| $9/mo app + outbound | "Outbound economics won't work — focus PLG + paid social" |
| Zero domain authority + SEO only | "SEO is 12+ months — need interim channel" |
| Enterprise + Meta lead gen | "LinkedIn or outbound; Meta leads are usually low quality" |
| No list + "email strategy" | "Need capture asset first — popup, lead magnet, trial" |

## Operational workflow

1. Confirm **ACV/AOV**, **motion**, **timeline**, **budget band**
2. Load audience context — where they spend time
3. Map channels to **stages** from `funnel-frameworks` (not the reverse)
4. Score fit: Strong / OK / Poor per channel
5. Recommend **1 primary + 1 optional** for v1
6. For each assigned channel, fill playbook template (abbreviated in table if many)
7. Hand creative patterns to `conversion-copywriting` — don't write full ads here

## Output format (stage table column)

| Stage | Channels | Rationale |
|-------|----------|-----------|
| Aware | SEO, Twitter | ICP searches comparison terms |
| Considering | Retargeting, email nurture | Owned + intent |

## Math policy

- Cite benchmarks via `web_search` or label **heuristic**
- Run CAC sanity check via `funnel-metrics` + code_execution
- Never invent platform-specific CPL without source or label

## Do not use when

- User needs full email body copy → `conversion-copywriting`
- User needs funnel shape only → `funnel-frameworks`
- User asks "is 2% conversion good" → `funnel-metrics`
- Auditing competitor channels only → `competition-analyzer` input, then this skill

## Anti-patterns

| Mistake | Fix |
|---------|-----|
| Channel as stage | Assign channel TO buyer state |
| Spray and pray | Concentration principle |
| LinkedIn for $19/mo consumer | Matrix says poor fit |
| Paid without landing page match | Flag LP requirement in build phase |

## References

| File | Channel |
|------|---------|
| `references/channels/paid-search.md` | Google/Bing search |
| `references/channels/meta-ads.md` | Meta (FB/IG) |
| `references/channels/linkedin-ads.md` | LinkedIn |
| `references/channels/seo-content.md` | SEO + content |
| `references/channels/email.md` | Lifecycle email |
| `references/channels/outbound.md` | Cold outbound (see also cold-outbound.md) |
| `references/channels/cold-outbound.md` | SDR/email/LinkedIn sequence |
| `references/channels/partnerships.md` | Partners, affiliates |
| `references/channels/community.md` | Community-led |

## Coordination

- **From funnel-frameworks:** Stage names
- **From audience-mapping:** Where ICP is reachable
- **To conversion-copywriting:** Angles and formats per channel
- **To funnel-metrics:** CPL/CAC targets per channel

## Quality checklist

- [ ] Channels mapped to stages, not conflated
- [ ] ≤2 primary channels recommended for early stage
- [ ] Poor-fit channels explicitly rejected with reason
- [ ] Math labeled source or heuristic
- [ ] Failure modes noted for assigned channels
