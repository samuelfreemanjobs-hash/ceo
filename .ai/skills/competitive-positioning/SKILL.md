---
name: competitive-positioning
description: Use when Enterprise Offer Copywriter must pre-handle objections from dossier.competitors_mentioned without naming competitors in customer-facing text. Triggers on "competitor objection", "battle card", "why not X", "competitive positioning in offer". Load battle cards from docs/marketing/research/battle-cards/ or competition-analyzer output. Never name competitor in customer-facing copy.
---

# Competitive Positioning (Enterprise Offer Copy)

Used by **Enterprise Copywriter** (`offer-copywriter`) when `dossier.competitors_mentioned` is non-empty.

## Rules

1. **Never name the competitor** in customer-facing narrative
2. **Position positively** — our strengths, not their weaknesses
3. **Pre-handle objections** triggered by `competitor:<name>` in structured output only
4. **Source from battle cards** — do not invent competitive claims

## Battle card lookup

For each `dossier.competitors_mentioned[].name`:

1. Search `docs/marketing/research/battle-cards/` for matching card
2. If missing → invoke `competition-analyzer` for profile OR flag `open_gaps` to Director
3. Extract: typical objections, our counters, proof points, landmines

## Objection response pattern

| Step | Action |
|------|--------|
| 1 | Identify objection theme from battle card (price, integration, support, etc.) |
| 2 | Map to dossier pain we address |
| 3 | Write response citing dossier evidence + in-scope capability |
| 4 | Set `trigger`: `competitor:<name>` in JSON (internal only) |

## Banned in customer text

- Competitor names
- "Unlike [vendor]..."
- Unverified superiority claims
- Trash-talking people or companies

## Handoffs

- Missing battle card → `competition-analyzer` (Scout)
- Claim needs substantiation → Risk & Compliance / legal review
