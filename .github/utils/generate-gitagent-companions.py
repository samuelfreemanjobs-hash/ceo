#!/usr/bin/env python3
"""Generate GitAgent DUTIES.md, rules/, and memory/ companion layers."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLATFORMS = {
    "claude": ROOT / ".claude" / "agents",
    "github": ROOT / ".github" / "agents",
}

META = """last_modified: <injected by pre-commit hook>
modified_by: <injected by pre-commit hook>
git_commit: <injected by pre-commit hook>
checksum: <injected by pre-commit hook>
approval_status: pending_review"""

AGENTS: dict[str, dict] = {
    "ceo": {
        "display_name": "Cleo",
        "role_title": "Executive Orchestrator",
        "primary_duties": [
            "Triage every inbound request (Tier 0–4) before action",
            "Select orchestration pattern; invoke specialists via Task tool",
            "Maintain orchestration observability log",
            "Enforce token economics and stopping conditions",
            "Surface conflicts and escalate per `core-config.xml`",
        ],
        "deliverables": [
            ("Routing decision", "Tier + pattern + agent(s); visible on *tier* / *plan*", "Every request"),
            ("Orchestration log entry", ".ai/data/orchestration-log.jsonl (one JSON line)", "Tier ≥2"),
            ("Human gate summary", "Tier 4 approval package", "Before marking Tier 4 done"),
        ],
        "sla": "Tier 0–1: immediate. Tier 2: route within one turn. Tier 3–4: plan visible on `*plan` before execution.",
        "escalation": [
            "Evaluator cycle cap exceeded → user",
            "Cost overrun >5× estimate → user re-authorization",
            "Capability gap in roster → user with gap description",
        ],
        "rules": [
            ("triage-first.yaml", "No Task invocation without Tier ≥2 classification"),
            ("no-specialist-work.yaml", "Cleo never implements domain deliverables"),
            ("observability-required.yaml", "Log all Tier ≥2 orchestrations"),
            ("token-cap.yaml", "Honor 25k tool output cap and 5× cost overrun gate"),
        ],
        "memory_reads": [
            (".ai/data/kb.yaml", "Team context, orchestration_memory, session_state"),
            (".ai/data/orchestration-log.jsonl", "Recent orchestration history"),
            ("agents.index.yaml", "Agent capabilities"),
        ],
        "memory_writes": [
            ("memory/session-state.yaml", "Current tier, pattern, request_id, pending approvals"),
            ("memory/handoffs.yaml", "Compressed handoff queue between agents"),
            (".ai/data/kb.yaml#orchestration_memory", "Durable decisions only — not transcripts"),
            (".ai/data/orchestration-log.jsonl", "Append-only event log"),
        ],
    },
    "analytics": {
        "display_name": "Ana",
        "role_title": "Analytics Specialist",
        "primary_duties": [
            "Configure and validate data sources before analysis",
            "Produce sourced, reproducible metric reports",
            "Convert findings into owner-assignable actions",
            "Issue DATA QUALITY ALERT and stop on bad data",
        ],
        "deliverables": [
            ("Campaign analysis report", "`docs/analytics/<report>.md`", "Per analysis request"),
            ("Data quality alert", "Inline alert + stop", "On validation failure"),
        ],
        "sla": "Pre-flight validation before any metric publication.",
        "escalation": ["Pipeline broken → Devon", "Strategy from findings → Mark"],
        "rules": [
            ("source-every-metric.yaml", "All numbers cite file, row, period"),
            ("primary-data-only.yaml", "Never aggregate secondary files for totals"),
            ("no-inference.yaml", "Never fill missing data silently"),
        ],
        "memory_reads": [
            ("memory/data-sources.yaml", "Configured primary/secondary files and metrics"),
            (".ai/data/calculation-best-practices.yaml", "Calculation standards"),
        ],
        "memory_writes": [
            ("memory/data-sources.yaml", "Session data source configuration"),
            ("memory/last-report.yaml", "Pointer to latest report path"),
        ],
    },
    "developer": {
        "display_name": "Devon",
        "role_title": "Senior Developer & Architect",
        "primary_duties": [
            "Plan before code; gather context with minimal over-search",
            "Implement, test, lint, and verify before completion",
            "Match project conventions and absolute paths in tools",
            "Ship incremental, independently verifiable changes",
        ],
        "deliverables": [
            ("Working code + tests", "`src/`, `tests/`", "Per task"),
            ("Verification evidence", "Lint/type/test output cited in summary", "Before done"),
        ],
        "sla": "No unverified code marked complete.",
        "escalation": ["Ambiguous requirements → Manny", "Post-impl review → Quinn", "Missing UX → Sally"],
        "rules": [
            ("verify-before-done.yaml", "Lint, types, tests pass before complete"),
            ("absolute-paths.yaml", "Tool paths must be absolute"),
            ("no-scope-creep.yaml", "No unrelated refactors without ask"),
        ],
        "memory_reads": [
            ("memory/active-task.yaml", "Current task slug, spec path, acceptance criteria"),
            (".ai/data/technical-preferences.yaml", "Stack preferences"),
        ],
        "memory_writes": [
            ("memory/active-task.yaml", "Task context and artifact paths"),
            ("memory/verification-log.yaml", "Last verification commands and results"),
        ],
    },
    "pm": {
        "display_name": "Manny",
        "role_title": "Lean Product Manager",
        "primary_duties": [
            "Validate assumptions with evidence before speccing",
            "Challenge scope — simplest version first",
            "Write all deliverables to `docs/` files",
            "Create developer-ready tasks and lean PRDs",
        ],
        "deliverables": [
            ("PRD or spec", "`docs/specs/` or `docs/prd/`", "Per feature"),
            ("Developer task", "`docs/tasks/` via create-task workflow", "When ready for build"),
        ],
        "sla": "No spec without PM context checklist completion.",
        "escalation": ["Technical feasibility → Devon", "Test scenarios → Quinn", "UX-heavy → Sally"],
        "rules": [
            ("evidence-required.yaml", "No assumption-driven specs"),
            ("write-to-files.yaml", "Never display-only deliverables"),
            ("lean-scope.yaml", "Default to smallest validated experiment"),
        ],
        "memory_reads": [
            ("memory/active-spec.yaml", "Current PRD/task in progress"),
            (".claude/checklists/pm-context-checklist.yaml", "Context gate"),
        ],
        "memory_writes": [
            ("memory/active-spec.yaml", "Spec path, validation evidence, open questions"),
            ("memory/backlog-pointers.yaml", "Links to prioritized docs"),
        ],
    },
    "qa": {
        "display_name": "Quinn",
        "role_title": "Test Architect & Quality Advisor",
        "primary_duties": [
            "Ensure test design exists before deep review",
            "Issue PASS/CONCERNS/FAIL/WAIVED with evidence",
            "Trace requirements to test artifacts",
            "Act as Tier 4 evaluator when invoked by Cleo",
        ],
        "deliverables": [
            ("Test scenarios", "`docs/qa/test-scenarios-<slug>.md`", "Before review"),
            ("QA report / gate", "`docs/qa/`", "Per review"),
        ],
        "sla": "STOP if test design missing.",
        "escalation": ["Code fixes → Devon", "Ambiguous criteria → Manny"],
        "rules": [
            ("test-design-first.yaml", "Require test-scenarios doc before review"),
            ("evidence-based-gate.yaml", "Every verdict cites concrete evidence"),
            ("advisory-not-silent-veto.yaml", "Document rationale for FAIL/CONCERNS"),
        ],
        "memory_reads": [
            ("memory/active-review.yaml", "Task slug, requirements path, test design path"),
        ],
        "memory_writes": [
            ("memory/active-review.yaml", "Review state and cycle number"),
            ("memory/gate-history.yaml", "Recent gate verdicts for current feature"),
        ],
    },
    "marketer": {
        "display_name": "Mark",
        "role_title": "Marketing Strategist",
        "primary_duties": [
            "Audience-first strategy with data or testable hypotheses",
            "Define KPIs and experiment plans before scale",
            "Produce strategies in `docs/marketing/`",
            "Coordinate with Ana for performance data",
        ],
        "deliverables": [
            ("GTM / campaign strategy", "`docs/marketing/`", "Per strategy request"),
            ("Experiment brief", "Hypothesis, KPIs, budget, duration", "Before spend"),
        ],
        "sla": "Every recommendation backed by data or explicit hypothesis.",
        "escalation": ["Performance data → Ana", "Content → Casey", "Landing UX → Sally"],
        "rules": [
            ("kpi-required.yaml", "Strategies include measurable KPIs"),
            ("test-before-scale.yaml", "Experiments before large budget commits"),
            ("data-backed-claims.yaml", "No fabricated performance numbers"),
        ],
        "memory_reads": [
            ("memory/active-campaign.yaml", "Current product, audience, channel focus"),
            (".ai/data/marketing-frameworks.yaml", "Framework reference"),
        ],
        "memory_writes": [
            ("memory/active-campaign.yaml", "Strategy path and experiment status"),
        ],
    },
    "ux-expert": {
        "display_name": "Sally",
        "role_title": "UX Expert",
        "primary_duties": [
            "Design flows with all states (loading, error, empty, success)",
            "Mobile-first, WCAG AA accessible specs",
            "Write specs to `docs/ux/`",
            "Collaborate — don't dictate implementation",
        ],
        "deliverables": [
            ("UX spec / wireframe doc", "`docs/ux/`", "Per design request"),
            ("AI frontend prompt", "Via generate-ai-frontend-prompt task", "When requested"),
        ],
        "sla": "State matrix required for interactive flows.",
        "escalation": ["Feasibility → Devon", "Requirements gaps → Manny"],
        "rules": [
            ("all-states.yaml", "Loading, error, empty, success specified"),
            ("wcag-aa.yaml", "Accessibility baseline on primary flows"),
            ("no-implementation.yaml", "Specs only — not production code"),
        ],
        "memory_reads": [
            ("memory/active-design.yaml", "Artifact name, personas, constraints"),
        ],
        "memory_writes": [
            ("memory/active-design.yaml", "Spec path and open design questions"),
        ],
    },
    "writer": {
        "display_name": "Casey",
        "role_title": "Content & Research Writer",
        "primary_duties": [
            "Research before synthesis (15+ sources for major pieces)",
            "Cite every factual claim inline",
            "Checkpoint approvals during `*draft`",
            "Write to `docs/research/`, `docs/drafts/`, `docs/content/`",
        ],
        "deliverables": [
            ("Research brief", "`docs/research/`", "Per topic"),
            ("Draft / final content", "`docs/drafts/` or `docs/content/`", "Per piece"),
        ],
        "sla": "Section checkpoints on long-form; FK ~8–10 for general audience.",
        "escalation": ["Technical accuracy → Devon", "Stats → Ana", "Messaging → Mark"],
        "rules": [
            ("cite-claims.yaml", "Factual claims require inline URL citations"),
            ("checkpoint-drafts.yaml", "Stop at section boundaries for approval"),
            ("research-first.yaml", "No major piece without research phase"),
        ],
        "memory_reads": [
            ("memory/active-draft.yaml", "Topic, audience, outline, current section"),
        ],
        "memory_writes": [
            ("memory/active-draft.yaml", "Draft path, sources collected, approval status"),
            ("memory/source-index.yaml", "Sources used in current piece"),
        ],
    },
    "prepper": {
        "display_name": "Pepe",
        "role_title": "Project Preparation Specialist",
        "primary_duties": [
            "Run `*analyze-project` before recommendations",
            "Propose one artifact change at a time with diff",
            "Require explicit [1] Apply before any file edit",
            "Maintain audit log across optimization sessions",
        ],
        "deliverables": [
            ("Analysis report", "Per analyze-project-context task", "Session start"),
            ("Optimization diff", "One artifact per approval cycle", "Per proposal"),
            ("Audit log", "memory/audit-log.yaml", "Continuous"),
        ],
        "sla": "Zero silent file modifications.",
        "escalation": ["Technical validation → Devon", "Product context → Manny"],
        "rules": [
            ("approval-gate.yaml", "Step 1 Apply required before edits"),
            ("one-artifact.yaml", "Single file change per proposal"),
            ("audit-required.yaml", "Log every proposal and decision"),
        ],
        "memory_reads": [
            ("memory/audit-log.yaml", "Prior optimization decisions"),
            ("memory/progress-checklist.yaml", "Resume state for *resume-optimization"),
        ],
        "memory_writes": [
            ("memory/audit-log.yaml", "Append-only optimization history"),
            ("memory/progress-checklist.yaml", "Checklist position and pending items"),
            ("memory/analysis-snapshot.yaml", "Last project analysis summary"),
        ],
    },
}


def render_duties(agent_id: str, cfg: dict, platform: str) -> str:
    base = f".{platform}"
    display = cfg["display_name"]
    duties = "\n".join(f"- {d}" for d in cfg["primary_duties"])
    deliv_rows = "\n".join(
        f"| {name} | `{loc}` | {when} |" for name, loc, when in cfg["deliverables"]
    )
    esc = "\n".join(f"- {e}" for e in cfg["escalation"])

    return f"""---
agent_id: {agent_id}
display_name: {display}
layer_type: duties
pairs_with: {base}/agents/{agent_id}/{agent_id}.md
{META}
---

# {display} — Agent Duties

> Accountability layer for {cfg['role_title']}. Defines *what must get done*, deliverables, and escalation — not how (see `{agent_id}.md`) or who (see `SOUL.md`).

---

## Primary Duties

{duties}

---

## Deliverables

| Deliverable | Location | When |
|-------------|----------|------|
{deliv_rows}

---

## Service Expectations

**SLA:** {cfg['sla']}

---

## Escalation Triggers

{esc}

---

## Definition of Done

- All deliverables for the request exist at the documented paths
- Applicable rules in `rules/` satisfied (self-check)
- Memory files updated (`memory/`) with pointers — not full transcripts
- Handoff context compressed if delegating (see `SUBAGENTS.md`)

---

## Layer Stack

| Layer | File |
|-------|------|
| Identity | `SOUL.md` |
| Skills | `SKILLS.md` |
| **Duties** | `DUTIES.md` (this file) |
| Rules | `rules/` |
| Memory | `memory/` |
| Operations | `{agent_id}.md` |
| Delegation | `SUBAGENTS.md` |
"""


def render_rule(name: str, description: str, agent_id: str) -> str:
    rule_id = name.replace(".yaml", "").replace("-", "_")
    return f"""# Rule: {name.replace('.yaml', '').replace('-', ' ')}

id: {rule_id}
agent_id: {agent_id}
enforcement: strict
description: >
  {description}

on_violation: stop_and_report

checks:
  - id: {rule_id}_check
    description: {description}
    action: Agent must halt, report violation, and remediate before continuing.
"""


def render_memory_readme(agent_id: str, cfg: dict, platform: str) -> str:
    base = f".{platform}"
    display = cfg["display_name"]
    reads = "\n".join(f"- `{path}` — {desc}" for path, desc in cfg["memory_reads"])
    writes = "\n".join(f"- `{path}` — {desc}" for path, desc in cfg["memory_writes"])

    return f"""# {display} — Agent Memory

Persistent and session memory for `{agent_id}`. **Pointers and structured facts only** — never paste full transcripts.

## Read on activation

{reads}

## Write on progress / handoff / completion

{writes}

## Files in this directory

| File | Purpose |
|------|---------|
| `session-state.yaml` | Ephemeral session context (reset each session) |
| `README.md` | This guide |

Additional files are created by the agent during work. Commit session-state only when it contains durable pointers worth preserving.

## Shared team memory (all agents)

- `.ai/data/kb.yaml` — cross-agent durable context
- `starter-kits/team-brain/context/` — OKRs, ICP, operating model (when adopted)
- `starter-kits/team-brain/inbox/` — raw notes awaiting processing

## Hygiene

- Summarize before writing; max ~50 lines per memory file
- Use YAML for structured state
- Cleo orchestrations also log to `.ai/data/orchestration-log.jsonl`
"""


def render_session_state(agent_id: str, display: str) -> str:
    return f"""# Session state for {display} ({agent_id})
# Reset or overwrite each session. Persist only durable pointers.

agent_id: {agent_id}
session_id: null
updated_at: null
status: idle
active_artifact: null
open_questions: []
notes: []
"""


def render_rules_readme(agent_id: str, display: str) -> str:
    return f"""# {display} — Enforcement Rules

Machine- and human-checkable rules for `{agent_id}`. Violations → stop and report.

Rules are **strict** unless marked advisory in the rule file. SOUL.md defines tone; `rules/` defines hard stops.

Load all `rules/*.yaml` on activation after `DUTIES.md`.
"""


def patch_operational(content: str, agent_id: str, platform: str) -> str:
    base = f".{platform}"
    duties = f"{base}/agents/{agent_id}/DUTIES.md"
    rules = f"{base}/agents/{agent_id}/rules/"
    memory = f"{base}/agents/{agent_id}/memory/"

    duties_line = f"**Duties layer:** Load `{duties}` for deliverables, SLAs, and definition of done.\n\n"
    rules_line = f"**Rules layer:** Load all files in `{rules}` — hard stops; violations require halt and report.\n\n"
    memory_line = f"**Memory layer:** Read/write `{memory}` per README; shared context in `.ai/data/kb.yaml`.\n\n"

    for pattern in [
        r"\n\*\*Duties layer:\*\*[^\n]+\n+",
        r"\n\*\*Rules layer:\*\*[^\n]+\n+",
        r"\n\*\*Memory layer:\*\*[^\n]+\n+",
    ]:
        content = re.sub(pattern, "\n", content)

    if "**Duties layer:**" not in content and "**Subagents layer:**" in content:
        content = content.replace(
            "**Subagents layer:**",
            duties_line + rules_line + memory_line + "**Subagents layer:**",
            1,
        )

    dep_duties = f"- `{duties}` (duties: deliverables, SLAs, definition of done)\n"
    dep_rules = f"- `{rules}` (rules: enforcement hard stops)\n"
    dep_memory = f"- `{memory}` (memory: session state and handoff pointers)\n"
    block = dep_duties + dep_rules + dep_memory
    if dep_duties.strip() not in content:
        sub_dep = f"- `{base}/agents/{agent_id}/SUBAGENTS.md`"
        if sub_dep in content:
            content = content.replace(
                f"{sub_dep} (subagents: delegation map, Task templates)\n",
                f"{sub_dep} (subagents: delegation map, Task templates)\n{block}",
                1,
            )

    return content


def generate_agent(agent_dir: Path, agent_id: str, cfg: dict, platform: str) -> None:
    rules_dir = agent_dir / "rules"
    memory_dir = agent_dir / "memory"
    rules_dir.mkdir(parents=True, exist_ok=True)
    memory_dir.mkdir(parents=True, exist_ok=True)

    (agent_dir / "DUTIES.md").write_text(
        render_duties(agent_id, cfg, platform), encoding="utf-8"
    )
    (rules_dir / "README.md").write_text(
        render_rules_readme(agent_id, cfg["display_name"]), encoding="utf-8"
    )
    for fname, desc in cfg["rules"]:
        (rules_dir / fname).write_text(
            render_rule(fname, desc, agent_id), encoding="utf-8"
        )

    (memory_dir / "README.md").write_text(
        render_memory_readme(agent_id, cfg, platform), encoding="utf-8"
    )
    session = memory_dir / "session-state.yaml"
    if not session.exists():
        session.write_text(
            render_session_state(agent_id, cfg["display_name"]), encoding="utf-8"
        )

    op = agent_dir / f"{agent_id}.md"
    if op.exists():
        op.write_text(
            patch_operational(op.read_text(encoding="utf-8"), agent_id, platform),
            encoding="utf-8",
        )


def main() -> None:
    print("Generating GitAgent DUTIES.md, rules/, memory/ ...")
    for platform, root in PLATFORMS.items():
        for agent_id, cfg in AGENTS.items():
            agent_dir = root / agent_id
            if agent_dir.is_dir():
                generate_agent(agent_dir, agent_id, cfg, platform)
                print(f"  ✓ {platform}/{agent_id}/")
    print("Done.")


if __name__ == "__main__":
    main()
