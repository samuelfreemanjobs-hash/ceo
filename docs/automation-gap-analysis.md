# Automation Gap Analysis — Path to 80% Agent Automation

**Date:** 2026-06-15 (updated)  
**Scope:** CEO-Orchestration repo + business operations it supports  
**Target:** ~80% of repeatable work executed by agents with human gates only where stakes require it

---

## Current state (post automation sprint)

| Area | Status | Automation value |
|------|--------|------------------|
| GitAgent 6-layer stack (all 9 agents) | ✅ `.claude`, `.github`, `.codex`, `.gemini` | High |
| Tier-adaptive CEO (Cleo) | ✅ Prompt + core-config + `*approve` | High |
| Team-brain at repo root | ✅ `context/`, `inbox/`, `specs/` | High |
| Orchestration log runtime | ✅ JSONL + `orchestration-log.py` | Medium |
| kb.yaml orchestration_memory | ✅ Populated with automation pointers | Medium |
| Pre-commit metadata injection | ✅ `.githooks/pre-commit` + `inject-metadata.py` | Medium |
| Scheduled runs | ✅ Daily inbox, weekly analytics, CI | High |
| Activation protocol | ✅ All agent `<id>.md` files | Medium |
| Agent validation CI | ✅ `validate-agents.py` + fixtures | High |
| Analytics sample data | ✅ `data/analytics/campaign-weekly.csv` | Medium |
| MCP integration doc | ✅ `context/mcp-integrations.md` + `.env.example` | Medium |
| Outbound comms gate | ✅ `ceo/rules/outbound-comms.yaml` | Medium |
| Rules linter | ✅ `lint-rules.py` in CI | Low |

**Rough automation today:** ~75–80% of *defined* workflows (agents + scripts + schedules). **Business-wide:** depends on live MCP auth and real analytics exports.

---

## Remaining gaps (P2/P3)

| # | Gap | Priority | Notes |
|---|-----|----------|-------|
| 1 | Live MCP credentials in CI | P2 | User must authenticate Cursor MCP + GitHub secrets |
| 2 | Slack `#ceo-agent` webhook | P2 | Documented in `mcp-integrations.md`; needs token |
| 3 | Token cost dashboard | P2 | Parse `orchestration-log.jsonl` → weekly markdown report |
| 4 | Zapier event triggers | P2 | Use Zapier MCP per workspace rules |
| 5 | Deploy pipeline (Tier 4 ship) | P2 | Devin/CI/CD + Quinn + human approve |
| 6 | `memory/long-term/` archive | P3 | Optional GitAgent extension |
| 7 | Per-agent cycle-time metrics | P3 | Extend log schema |
| 8 | Multi-tenant `memory/clients/` | P3 | For agency use cases |

---

## 80% automation definition (unchanged)

| Work type | Target agent ownership | Human role |
|-----------|------------------------|------------|
| Triage & routing | Cleo 95% | Approve Tier 4 only |
| Product specs & tasks | Manny 85% | Validate assumptions |
| Implementation | Devon 80% | Review PR |
| QA / gates | Quinn 85% | Waive FAIL explicitly |
| Analytics reports | Ana 90% | Data source setup |
| Marketing strategy | Mark 75% | Budget approval |
| Content drafts | Casey 80% | Section approvals |
| UX specs | Sally 85% | Stakeholder sign-off |
| System tuning | Pepe 70% | Every Apply decision |
| Inbox → structured docs | Cleo + Casey 80% | Sensitive items |
| External comms / spend / legal | 0% autonomous | Human only |

---

## Setup reference

See [`docs/automation-setup.md`](automation-setup.md) for hooks, scripts, and workflows.

---

## Open questions for Sam

1. Which **business vertical** to prioritize for live MCP (product, agency, content, SaaS)?
2. **Approval channel** preference: Slack, GitHub PR, or email?
3. **80% metric** — task count, hours, or revenue activities?
