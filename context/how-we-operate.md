# How We Operate

**Owner:** Sam Freeman  
**Last updated:** 2026-06-15

Operating manual for the CEO-Orchestration agent system. Update when the operating model changes — not for every status tick.

## Team and responsibilities

| Person / Agent | Area | Primary responsibility | Can decide without escalation |
|----------------|------|------------------------|-------------------------------|
| Sam (human) | Vision, spend, external comms | Strategic direction, Tier 4 approval, Pepe Apply | Final say on all gates |
| Cleo (`ceo`) | Triage & routing | Tier 0–4 classification, pattern selection, orchestration | Tier 0–3 routing within policy |
| Manny (`pm`) | Product | Specs, tasks, cycle briefs | Lean scope within active cycle |
| Devon (`developer`) | Engineering | Implementation, PRs, fixes | Code within approved spec |
| Quinn (`qa`) | Quality | Test design, advisory gates | FAIL advisory (not silent veto) |
| Ana (`analytics`) | Data | Campaign reports, metrics | Analysis from primary sources only |
| Mark (`marketer`) | Growth | Strategy, channel plans | Draft strategy; not budget spend |
| Casey (`writer`) | Content | Research, drafts | Draft sections; not publish |
| Sally (`ux-expert`) | UX | Specs, accessibility | Design recommendations |
| Pepe (`prepper`) | System tuning | Audits, optimization proposals | Recommend only — Apply needs approval |

## Decision rights

| Decision | Default owner | When escalation is required |
|----------|---------------|-----------------------------|
| Tier routing (0–3) | Cleo | Tier 4 or ambiguous blast radius |
| Spec scope | Manny | Changes OKRs or cross-cycle priority |
| Ship to production | Sam + Quinn | Always Tier 4 |
| Pepe optimization Apply | Sam | Every Apply |
| External publish (email, social, ads) | Sam | Always |
| Inbox → spec promotion | Cleo (automated daily) | Sensitive or legal content |

## Rituals

| Ritual | Participants | Frequency | Output |
|--------|--------------|-----------|--------|
| Inbox process | Cleo → Casey/Manny | Daily (GitHub Action) | `specs/<cycle>/` or `context/` |
| Weekly analytics | Cleo → Ana → Mark | Weekly (Monday) | `data/analytics/` report |
| Cycle open | Manny + Cleo | Per initiative | `specs/<cycle-id>/` |
| Cycle close | Manny + Quinn | End of cycle | `retrospective.md`, `learnings.md` |
| Orchestration review | Cleo | Weekly | `orchestration-log.jsonl` summary |

## Inbox processing rhythm

- Raw notes → `inbox/`
- **Automated:** `.ai/utils/process-inbox.py process-all` (daily workflow) promotes items to `specs/`
- Processed raw notes → `inbox/archive/`
- Agents read `context/rules-for-ai.md` before acting

## Escalation triggers

- Tier 4 pattern selected (production, security, irreversible)
- Quinn FAIL on high-stakes deliverable
- KPI off-track two consecutive checkpoints
- Blocker past agreed SLA
- Customer-facing issue affecting trust or revenue
- Scope, priority, or spend changes materially

## Cycle opening checklist

- [ ] Run `.ai/utils/open-cycle.sh <slug> "<title>"` or duplicate `specs/template/`
- [ ] Fill `00-brief.md` / `command_center.md`
- [ ] Confirm `context/okrs.md` and owners
- [ ] Log orchestration start via `orchestration-log.py`

## Cycle closing checklist

- [ ] Update KPI snapshot in cycle folder
- [ ] Finalize `decision_log.md`
- [ ] Write `retrospective.md`
- [ ] Append to `context/learnings.md`
- [ ] Archive inbox items if any remain
