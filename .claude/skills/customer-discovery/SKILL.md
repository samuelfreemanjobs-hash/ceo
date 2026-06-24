---
name: customer-discovery
description: Defines what good customer discovery looks like for B2B offer building — BANT, technical fit, political map, dossier_confidence scoring. Use when running Offer Discovery agent or when Director assesses whether dossier is sufficient to proceed. Triggers on "discovery quality", "dossier confidence", "missing context", "BANT", "decision map".
---

# Customer Discovery

Used by **Offer Discovery** (`offer-discovery`) and **Offer Director** (low-confidence gate).

## Discovery dimensions

| Dimension | Sources | Minimum for "high" confidence |
|-----------|---------|-------------------------------|
| **Budget** | CRM amount, rep_brief, transcript | Amount or range cited with source |
| **Authority** | decision_makers with roles | ≥1 economic + ≥1 technical or champion |
| **Need** | pains with verbatim evidence | ≥2 pains with evidence |
| **Timeline** | opportunity.expected_close, urgency_signals | Close date + ≥1 urgency signal |
| **Technical fit** | scope prerequisites, integrations | Known stack or explicit gap |
| **Political map** | decision_makers, champion role | Champion identified or flagged gap |

## dossier_confidence scoring

**high**
- >5 activity records
- ≥1 call transcript
- rep_brief consistent with system data (`rep_brief_consistency = consistent`)
- No unresolved disputes on key fields (amount, timeline, decision-maker)

**medium**
- Some CRM/activity data
- No major contradictions
- ≥1 pain documented

**low**
- New account OR sparse data OR unresolved disputes
- Director: ask rep **ONE** focused clarifying question before proceeding

## Gap flagging

Populate `open_gaps` when:
- No economic buyer identified
- No documented pain with evidence
- Competitor mentioned but no context
- Integration requirement stated but system unknown
- Amount contradicts rep_brief without dispute resolution

## Anti-patterns

- Inferring pain from industry vertical alone
- Paraphrasing customer quotes
- Filling `unknown` with plausible guesses
- High confidence without transcript on enterprise deals

## References

- `references/bant-checklist.md`
