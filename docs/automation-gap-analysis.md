# Automation Gap Analysis — Path to 80% Agent Automation

**Date:** 2026-06-15  
**Scope:** CEO-Orchestration repo + business operations it supports  
**Target:** ~80% of repeatable work executed by agents with human gates only where stakes require it

---

## Current state (what you have)

| Area | Status | Automation value |
|------|--------|------------------|
| GitAgent 6-layer stack (ops, SOUL, SKILLS, SUBAGENTS, DUTIES, rules, memory) | ✅ All 9 agents (.claude + .github) | High — agents know who/how/what/delegate |
| Tier-adaptive CEO orchestration (Cleo) | ✅ Prompt + core-config | High — reduces over-orchestration |
| Task / checklist / template indexes | ✅ 20 tasks, 6 checklists | Medium — procedural repeatability |
| Specialist roster + delegation maps | ✅ SUBAGENTS.md per agent | High |
| Shared `.ai/` asset layer | ✅ skills, data, templates | Medium |
| Team-brain starter kit | ✅ `starter-kits/team-brain/` | High — but **not wired into this repo root** |
| Codex flat agents | ⚠️ Manual profile switching | Low automation |
| Observability spec | ⚠️ Documented only | Medium — no runtime yet |

**Rough automation today:** ~35–45% of *defined* workflows (agent can execute if a human starts the right profile and feeds context). **Business-wide:** lower until memory, integrations, and triggers exist.

---

## What's missing — prioritized

### P0 — Blocks autonomous operation (do first)

| # | Gap | Why it matters | Suggested fix |
|---|-----|----------------|---------------|
| 1 | **Team-brain not live at repo root** | No `context/`, `inbox/`, `specs/` → agents lose cross-session memory | Copy/adopt `starter-kits/team-brain/` structure; fill `how-we-operate.md`, `okrs.md`, `icp.md` |
| 2 | **`orchestration-log.jsonl` not initialized** | Cleo can't observe or resume orchestration history | Create `.ai/data/orchestration-log.jsonl`; add writer helper or hook |
| 3 | **`kb.yaml` orchestration_memory empty** | Handoffs lack durable structured facts | Populate `session_state` / `orchestration_memory` sections; agents write pointers |
| 4 | **No pre-commit `inject-metadata.py`** | GitAgent layer checksums never enforced | Add hook + script for SOUL/SKILLS/DUTIES frontmatter |
| 5 | **No scheduled / triggered runs** | 100% human-initiated sessions | Cloud Agent cron, GitHub Actions, or Slack `#ceo-agent` trigger → Cleo |
| 6 | **Codex agents not on GitAgent layout** | Half your platforms still manual-switch | Migrate `.codex/agents/<id>/` like `.claude` |

### P1 — High leverage for 80% automation

| # | Gap | Why it matters | Suggested fix |
|---|-----|----------------|---------------|
| 7 | **Inbox processing automation** | Raw notes never become structured context | Daily agent job: inbox → `context/` + `specs/` (team-brain rhythm) |
| 8 | **Cycle automation** | No open/close spec cycles without human | Template duplicate + Manny opens cycle; Cleo sequences PM→Dev→QA |
| 9 | **MCP / API integrations** | Agents can't read real business data | Connect: analytics sources, ad platforms, CRM, GitHub, Notion, Supabase per channel |
| 10 | **Credential & secrets management** | Can't call external APIs safely | `.env` + Cursor secrets / GitHub Actions secrets; document in `context/rules-for-ai.md` |
| 11 | **Human approval UI** | Tier 4 + Pepe gates are chat-only | Slack reactions, GitHub PR review, or explicit `APPROVE` command channel |
| 12 | **Agent memory hydration on boot** | `memory/session-state.yaml` not auto-loaded | Activation protocol in each `<id>.md`: read memory/ + kb.yaml first |
| 13 | **CI quality gates** | Devon ships without automated CI | GitHub Actions: lint, test, Quinn advisory on PR |
| 14 | **Real data files for Ana** | Campaign analysis is spec-only without CSVs | `data/analytics/` + connection to ad export schedule |

### P2 — Operational maturity

| # | Gap | Why it matters | Suggested fix |
|---|-----|----------------|---------------|
| 15 | **DUTIES enforcement automation** | Rules in `rules/` are self-check only | Optional linter script validating agent outputs against rules |
| 16 | **`.gemini/` parity** | Fourth platform unmigrated | Mirror `.claude/agents/` structure |
| 17 | **Zapier / event triggers** | No "when X happens → Cleo" | Zapier MCP: new lead → Manny task; support ticket → Devon |
| 18 | **Customer-facing boundaries** | Agents might act externally without guardrails | `rules/outbound-comms.yaml` + approval for email/posts |
| 19 | **Cost / token dashboard** | No visibility into 10–15× multi-agent spend | Parse `orchestration-log.jsonl` → weekly summary |
| 20 | **Agent behavior tests** | Prompt regressions undetected | Fixture prompts per agent; expected tier/route assertions |
| 21 | **Documentation drift** | README still describes "prescribe not execute" for CEO | Update README for tier-adaptive auto-orchestration |
| 22 | **Writer research automation** | Casey needs manual source gathering | Firecrawl / search MCP in SKILLS triggers |
| 23 | **Marketing execution loop** | Mark produces strategy but not automated reporting | Weekly Cleo→Ana→Mark pipeline on schedule |
| 24 | **Deploy pipeline** | Tier 4 "ship to prod" has no defined path | Devin/CI/CD + Quinn gate + human approve |

### P3 — Nice to have

| # | Gap | Suggested fix |
|---|-----|---------------|
| 25 | `DUTIES.md` approval workflow in Git | PR template requiring duty/sign-off |
| 26 | Per-agent metrics (cycle time, rework rate) | Extend orchestration log schema |
| 27 | Voice/Slack dedicated Cleo interface | Already started — wire to Task orchestration |
| 28 | Multi-tenant / client separation in memory | `memory/clients/<id>/` pattern |

---

## 80% automation definition (recommended)

| Work type | Target agent ownership | Human role |
|-----------|------------------------|------------|
| Triage & routing | Cleo 95% | Approve Tier 4 only |
| Product specs & tasks | Manny 85% | Validate assumptions |
| Implementation | Devon 80% | Review PR, edge cases |
| QA / gates | Quinn 85% | Waive FAIL explicitly |
| Analytics reports | Ana 90% | Data source setup |
| Marketing strategy | Mark 75% | Budget approval |
| Content drafts | Casey 80% | Section approvals |
| UX specs | Sally 85% | Brand/stakeholder sign-off |
| System tuning | Pepe 70% | Every Apply decision |
| Inbox → structured docs | Cleo + Casey 80% | Sensitive items |
| External comms / spend / legal | 0% autonomous | Human only |

**Weighted average toward 80%** requires P0 + P1 complete and team-brain operating for ≥2 weeks.

---

## Recommended implementation sequence

```text
Week 1 (foundation)
  ├── Adopt team-brain at repo root (context/, inbox/, specs/)
  ├── Init orchestration-log + kb.yaml memory sections
  ├── pre-commit inject-metadata
  └── CI: lint + test on PR

Week 2 (triggers)
  ├── Scheduled: inbox process, weekly analytics, cycle open/close
  ├── Slack/GitHub trigger → Cleo
  └── MCP: GitHub + Notion or your CRM

Week 3 (integrations)
  ├── Analytics data pipeline → Ana
  ├── Codex + Gemini GitAgent migration
  └── Approval flows for Tier 4 + Pepe

Week 4 (measure)
  ├── orchestration-log dashboard
  ├── Agent behavior fixtures
  └── Retrospective: % tasks completed without human mid-work
```

---

## GitAgent layer completion (this PR)

| Layer | Status |
|-------|--------|
| `<id>.md` | ✅ |
| `SOUL.md` | ✅ |
| `SKILLS.md` | ✅ |
| `SUBAGENTS.md` | ✅ |
| `DUTIES.md` | ✅ Added |
| `rules/` | ✅ Added |
| `memory/` | ✅ Added |

**Still optional per GitAgent:** `DUTIES.md` human approval in Git, `memory/long-term/` archive, cross-agent `rules/shared/`.

---

## Open questions for Sam

1. Which **business** is this automating first (product, agency, content, SaaS)? Prioritizes MCP integrations.
2. **Approval channel** preference: Slack, GitHub PR, or email?
3. Adopt **team-brain at repo root** or separate business repo?
4. **80%** — measure by task count, hours, or revenue activities?
