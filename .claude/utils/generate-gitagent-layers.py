#!/usr/bin/env python3
"""Generate GitAgent SKILLS.md and SUBAGENTS.md layers for all agents."""

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

AGENT_CONFIG: dict[str, dict] = {
    "ceo": {
        "display_name": "Cleo",
        "role_title": "Executive Orchestrator",
        "skills_intro": "Cleo loads index catalogs and orchestration skills — never domain implementation skills.",
        "claude_skills": [
            ("using-ceo", "Session start; skill discovery before any response", True),
            ("dispatching-parallel-agents", "Tier 3 parallel orchestration with independent subtasks", False),
            ("subagent-driven-development", "Tier 3–4 multi-agent implementation pipelines", False),
            ("verification-before-completion", "Before marking orchestration complete", True),
        ],
        "tasks": [],
        "checklists": [],
        "templates": [],
        "data": [
            (".claude/data/kb.yaml", "Durable orchestration memory and team context"),
            (".ai/data/orchestration-log.jsonl", "Append-only orchestration observability log"),
        ],
        "indexes": [
            "agents.index.yaml",
            "tasks.index.yaml",
            "checklists.index.yaml",
            "data.index.yaml",
        ],
        "skill_rules": [
            "Invoke `using-ceo` at session start before responding.",
            "Read skill files from `.claude/skills/<name>/SKILL.md` when trigger matches.",
            "Never load implementation skills (TDD, debugging) — route to Devon instead.",
            "Consult indexes before Task invocation; do not guess agent capabilities.",
        ],
        "subagents_intro": "Cleo delegates via Task tool per triage tier. Never does specialist work directly.",
        "delegations": [
            {
                "name": "Manny",
                "id": "pm",
                "when": "Requirements, PRDs, ExecPlan decisions, scope negotiation",
                "never": "Tier 0–1 questions; implementation or test execution",
                "tier": "2–4",
            },
            {
                "name": "Devon",
                "id": "developer",
                "when": "Implementation, debugging, architecture, refactors",
                "never": "Product prioritization without spec; marketing analysis",
                "tier": "2–4",
            },
            {
                "name": "Quinn",
                "id": "qa",
                "when": "Quality gates, test review, Tier 4 evaluator loop",
                "never": "Writing production code; product scoping",
                "tier": "2–4 (evaluator at Tier 4)",
            },
            {
                "name": "Ana",
                "id": "analytics",
                "when": "Campaign performance, metrics, trend analysis",
                "never": "Strategy authoring without data request",
                "tier": "2–3",
            },
            {
                "name": "Mark",
                "id": "marketer",
                "when": "GTM strategy, channel planning, growth experiments",
                "never": "Raw data pipeline fixes",
                "tier": "2–3",
            },
            {
                "name": "Casey",
                "id": "writer",
                "when": "Research, long-form content, documentation",
                "never": "Code review; PRD ownership",
                "tier": "2–3",
            },
            {
                "name": "Sally",
                "id": "ux-expert",
                "when": "UX flows, wireframes, accessibility specs",
                "never": "Backend implementation",
                "tier": "2–3",
            },
            {
                "name": "Pepe",
                "id": "prepper",
                "when": "System optimization, agent/task tuning (user-initiated)",
                "never": "Routine feature delivery routing",
                "tier": "2",
            },
        ],
        "prompt_templates": [
            (
                "Tier 2 single specialist",
                'Task(subagent_type="{id}", prompt="Goal: {goal}. Tier: 2. Pattern: route-single-agent. Acceptance: {criteria}", description="{short}")',
            ),
            (
                "Tier 3 sequential",
                'Task(subagent_type="pm", ...) → summarize → Task(subagent_type="developer", ...) → summarize → Task(subagent_type="qa", ...)',
            ),
            (
                "Tier 4 evaluator",
                'Workers produce → Task(subagent_type="qa", prompt="Evaluate cycle {n}/3. Criteria: ... Output: ...", description="Quinn evaluate")',
            ),
        ],
        "subagent_rules": [
            "Never invoke agents below Tier 2.",
            "Parallel Task calls only at Tier 3+ when subtasks are independent.",
            "Pass compressed context: goal, tier, pattern, acceptance criteria, artifact paths.",
            "Log every orchestration to `.ai/data/orchestration-log.jsonl`.",
            "Never tell the user to switch profiles — invoke directly.",
        ],
    },
    "analytics": {
        "display_name": "Ana",
        "role_title": "Analytics Specialist",
        "skills_intro": "Ana uses data tasks, checklists, and verification skills — not implementation skills.",
        "claude_skills": [
            ("verification-before-completion", "Before publishing analysis report", True),
            ("systematic-debugging", "Data pipeline or calculation anomalies", False),
        ],
        "tasks": [
            ("analyze-campaign-performance.yaml", "Full campaign analysis workflow", True),
        ],
        "checklists": [
            ("analytics-checklist.yaml", "Pre-delivery report validation", True),
        ],
        "templates": [
            ("analytics-report-tmpl.yaml", "Standard report structure"),
        ],
        "data": [
            ("calculation-best-practices.yaml", "Metric calculation standards"),
        ],
        "delegations": [
            {
                "name": "Devon",
                "id": "developer",
                "when": "Data pipeline bugs, ETL fixes, custom analytics tooling",
                "never": "Interpreting campaign results Ana can compute",
            },
            {
                "name": "Mark",
                "id": "marketer",
                "when": "Strategy recommendations from analysis findings",
                "never": "Replacing Ana's metric calculations",
            },
        ],
        "prompt_templates": [
            (
                "Pipeline fix",
                'Task(subagent_type="developer", prompt="Analytics pipeline incomplete data. File: {path}. Issue: {issue}. Fix extraction logic.", description="Fix data pipeline")',
            ),
            (
                "Strategy handoff",
                'Task(subagent_type="marketer", prompt="Analysis complete: {report_path}. Key finding: {finding}. Develop optimization strategy.", description="Marketing strategy from data")',
            ),
        ],
    },
    "developer": {
        "display_name": "Devon",
        "role_title": "Senior Developer & Architect",
        "skills_intro": "Devon loads implementation, debugging, and quality skills before coding.",
        "claude_skills": [
            ("test-driven-development", "New features and bugfixes before implementation", True),
            ("systematic-debugging", "Any bug or test failure investigation", True),
            ("verification-before-completion", "Before marking work complete", True),
            ("receiving-code-review", "When processing Quinn's feedback", False),
            ("using-git-worktrees", "Isolated feature work when needed", False),
            ("use-context7", "Library/framework documentation lookup", False),
            ("executing-plans", "Multi-step implementation plans", False),
            ("finishing-a-development-branch", "Merge/PR decision after completion", False),
        ],
        "tasks": [],
        "checklists": [
            ("code-quality-checklist.yaml", "Pre-commit quality review", True),
            ("openai-sdk-compliance-checklist.yaml", "SDK/orchestration compliance", False),
        ],
        "delegations": [
            {
                "name": "Quinn",
                "id": "qa",
                "when": "Post-implementation review, security-sensitive changes",
                "never": "Writing tests Devon should write first",
            },
            {
                "name": "Manny",
                "id": "pm",
                "when": "Ambiguous requirements, complex multi-phase features",
                "never": "Routine bugfixes with clear repro",
            },
            {
                "name": "Sally",
                "id": "ux-expert",
                "when": "UI implementation without design spec",
                "never": "Backend-only changes",
            },
        ],
        "prompt_templates": [
            (
                "QA review",
                'Task(subagent_type="qa", prompt="Review implementation. Files: {files}. Test edge cases and security.", description="QA review feature")',
            ),
            (
                "Requirements gap",
                'Task(subagent_type="pm", prompt="Requirements unclear on {topic}. Need: {questions}.", description="Clarify requirements")',
            ),
        ],
    },
    "pm": {
        "display_name": "Manny",
        "role_title": "Lean Product Manager",
        "skills_intro": "Manny uses planning, brainstorming, and spec skills — not implementation.",
        "claude_skills": [
            ("brainstorming", "New feature ideation before spec", True),
            ("speckit-specify", "Structured feature specifications", False),
            ("speckit-plan", "Complex features needing implementation plan", False),
            ("writing-plans", "Multi-step delivery plans", False),
            ("create-deep-research-prompt", "Market/tech research prompts", False),
        ],
        "tasks": [
            ("create-task.yaml", "Developer-ready task definitions", True),
            ("create-doc.yaml", "PRDs and product documents", True),
            ("create-deep-research-prompt.yaml", "Research prompt generation", False),
        ],
        "checklists": [
            ("pm-context-checklist.yaml", "Before any spec — mandatory", True),
        ],
        "delegations": [
            {
                "name": "Devon",
                "id": "developer",
                "when": "Feasibility review, estimates, phased implementation planning",
                "never": "Having Devon write the PRD",
            },
            {
                "name": "Quinn",
                "id": "qa",
                "when": "Test scenario design from requirements",
                "never": "Running test suites",
            },
            {
                "name": "Sally",
                "id": "ux-expert",
                "when": "UI-heavy features needing design spec",
                "never": "Backend-only API specs",
            },
            {
                "name": "Ana",
                "id": "analytics",
                "when": "Data-driven prioritization or validation metrics",
                "never": "Replacing user interview evidence",
            },
        ],
    },
    "qa": {
        "display_name": "Quinn",
        "role_title": "Test Architect & Quality Advisor",
        "skills_intro": "Quinn uses quality, review, and verification skills — advisory not implementation.",
        "claude_skills": [
            ("requesting-code-review", "Structured review dispatch", True),
            ("verification-before-completion", "Before issuing gate verdict", True),
            ("systematic-debugging", "Root-cause analysis for failures", False),
        ],
        "tasks": [
            ("test-scenarios.yaml", "Test design before review — required", True),
            ("create-qa-report.yaml", "Formal QA report generation", True),
            ("nfr-assess.yaml", "Non-functional requirements assessment", False),
            ("review-task.yaml", "Task-level review workflow", False),
        ],
        "checklists": [
            ("code-quality-checklist.yaml", "Code review depth", True),
            ("openai-sdk-compliance-checklist.yaml", "Orchestration compliance", False),
        ],
        "delegations": [
            {
                "name": "Devon",
                "id": "developer",
                "when": "FAIL/CONCERNS requiring code fixes",
                "never": "Fixing code directly",
            },
            {
                "name": "Manny",
                "id": "pm",
                "when": "Missing or ambiguous acceptance criteria",
                "never": "Rewriting requirements without user",
            },
        ],
    },
    "marketer": {
        "display_name": "Mark",
        "role_title": "Marketing Strategist",
        "skills_intro": "Mark uses GTM and content strategy skills — delegates data and copy.",
        "claude_skills": [
            ("developing-marketing-strategy", "GTM and channel strategy work", True),
            ("brainstorming", "Campaign ideation", False),
        ],
        "tasks": [
            ("create-marketing-strategy.yaml", "Full marketing strategy workflow", True),
            ("optimize-content.yaml", "Content performance optimization", False),
        ],
        "checklists": [],
        "delegations": [
            {
                "name": "Ana",
                "id": "analytics",
                "when": "Campaign performance data, ROI, CAC trends",
                "never": "Inventing metrics",
            },
            {
                "name": "Casey",
                "id": "writer",
                "when": "Blog posts, copy, content series from strategy",
                "never": "Technical documentation",
            },
            {
                "name": "Sally",
                "id": "ux-expert",
                "when": "Landing page or conversion UX design",
                "never": "Implementing pages in code",
            },
            {
                "name": "Manny",
                "id": "pm",
                "when": "Product positioning tied to roadmap decisions",
                "never": "Engineering task breakdown",
            },
        ],
    },
    "ux-expert": {
        "display_name": "Sally",
        "role_title": "UX Expert",
        "skills_intro": "Sally uses design doc and frontend prompt skills — delegates build and requirements.",
        "claude_skills": [
            ("brainstorming", "Design exploration before spec", False),
        ],
        "tasks": [
            ("create-doc.yaml", "UX spec documents", True),
            ("generate-ai-frontend-prompt.yaml", "AI UI generation prompts", True),
            ("execute-checklist.yaml", "Checklist-driven design review", False),
        ],
        "checklists": [],
        "delegations": [
            {
                "name": "Devon",
                "id": "developer",
                "when": "Feasibility review, implementation kickoff",
                "never": "Writing production components",
            },
            {
                "name": "Manny",
                "id": "pm",
                "when": "Missing user research or requirements",
                "never": "Defining visual design without user context",
            },
            {
                "name": "Quinn",
                "id": "qa",
                "when": "Accessibility audit beyond Sally's spec",
                "never": "Replacing WCAG review in spec",
            },
        ],
    },
    "writer": {
        "display_name": "Casey",
        "role_title": "Content & Research Writer",
        "skills_intro": "Casey uses research and writing workflow skills — delegates technical validation.",
        "claude_skills": [
            ("create-deep-research-prompt", "Deep research setup", False),
        ],
        "tasks": [
            ("warmstart-article.yaml", "STORM warmstart research", True),
            ("synthesize-article.yaml", "Multi-perspective synthesis", True),
            ("research-topic.yaml", "Topic research workflow", True),
            ("optimize-content.yaml", "SEO/readability optimization", False),
        ],
        "checklists": [
            ("content-quality-checklist.yaml", "Pre-publish content QA", True),
        ],
        "delegations": [
            {
                "name": "Devon",
                "id": "developer",
                "when": "Technical accuracy review of code/API content",
                "never": "Writing the article for Casey",
            },
            {
                "name": "Ana",
                "id": "analytics",
                "when": "Benchmark data and statistical claims",
                "never": "Inventing statistics",
            },
            {
                "name": "Mark",
                "id": "marketer",
                "when": "Messaging alignment with GTM strategy",
                "never": "Owning content draft",
            },
            {
                "name": "Quinn",
                "id": "qa",
                "when": "Factual accuracy audit for high-stakes content",
                "never": "Line editing",
            },
        ],
    },
    "prepper": {
        "display_name": "Pepe",
        "role_title": "Project Preparation Specialist",
        "skills_intro": "Pepe uses project analysis and optimization skills — meta-layer only.",
        "claude_skills": [
            ("analyze-project-context", "Before any optimization — mandatory", True),
            ("code-quality-check", "Auditing agent/task quality", False),
            ("document-project-state", "Project documentation generation", False),
        ],
        "tasks": [
            ("analyze-project-context.yaml", "Initial project analysis", True),
            ("optimize-agent.yaml", "Agent file optimization", True),
            ("optimize-task.yaml", "Task workflow optimization", True),
            ("optimize-checklist.yaml", "Checklist optimization", True),
        ],
        "templates": [
            ("project-analysis-tmpl.yaml", "Analysis report structure"),
        ],
        "data": [
            ("optimization-best-practices.md", "Optimization standards"),
        ],
        "delegations": [
            {
                "name": "Devon",
                "id": "developer",
                "when": "Validate technical preferences from analysis",
                "never": "Feature implementation",
            },
            {
                "name": "Manny",
                "id": "pm",
                "when": "Product context for task/agent alignment",
                "never": "Writing optimized agent files without approval",
            },
            {
                "name": "Quinn",
                "id": "qa",
                "when": "Quality standards for checklist optimization",
                "never": "Applying changes without user [1] Apply",
            },
        ],
    },
}


def platform_base(platform: str) -> str:
    return f".{platform}"


def render_skills(agent_id: str, cfg: dict, platform: str) -> str:
    base = platform_base(platform)
    display = cfg["display_name"]
    lines = [
        "---",
        f"agent_id: {agent_id}",
        f"display_name: {display}",
        "layer_type: skills",
        f"pairs_with: {base}/agents/{agent_id}/{agent_id}.md",
        META,
        "---",
        "",
        f"# {display} — Agent Skills",
        "",
        f"> Capability layer for {cfg['role_title']}. Pairs with `{agent_id}.md` (operations) and `SOUL.md` (identity).",
        f"> {cfg.get('skills_intro', '')}",
        "",
        "---",
        "",
        "## Invocation Rules",
        "",
    ]
    for rule in cfg.get(
        "skill_rules",
        [
            "Read skill file at `.claude/skills/<name>/SKILL.md` when trigger matches.",
            "Required skills (below) run before deliverables.",
            "Follow skill instructions exactly — they override default behavior.",
            "Tasks and checklists are procedural skills; load YAML from `.claude/tasks/` or `.claude/checklists/`.",
        ],
    ):
        lines.append(f"- {rule}")

    lines += ["", "---", "", f"## Claude Skills (`{base}/skills/`)", "", "| Skill | Trigger | Required |", "|-------|---------|----------|"]
    for skill, trigger, required in cfg.get("claude_skills", []):
        req = "yes" if required else "no"
        lines.append(f"| `{skill}` | {trigger} | {req} |")
    if not cfg.get("claude_skills"):
        lines.append("| — | No dedicated Claude skills | — |")

    lines += ["", "---", "", f"## Task Workflows (`{base}/tasks/`)", "", "| Task | Purpose | Required |", "|------|---------|----------|"]
    for task, purpose, required in cfg.get("tasks", []):
        req = "yes" if required else "no"
        lines.append(f"| `{task}` | {purpose} | {req} |")
    if not cfg.get("tasks"):
        lines.append("| — | See operational spec for ad-hoc workflows | — |")

    lines += ["", "---", "", f"## Checklists (`{base}/checklists/`)", "", "| Checklist | Purpose | Required |", "|-----------|---------|----------|"]
    for chk, purpose, required in cfg.get("checklists", []):
        req = "yes" if required else "no"
        lines.append(f"| `{chk}` | {purpose} | {req} |")
    if not cfg.get("checklists"):
        lines.append("| — | None assigned | — |")

    if cfg.get("templates") or cfg.get("data") or cfg.get("indexes"):
        lines += ["", "---", "", "## Supporting Resources", ""]
        if cfg.get("indexes"):
            lines.append(f"**Indexes** (`{base}/`):")
            for idx in cfg["indexes"]:
                lines.append(f"- `{idx}`")
            lines.append("")
        if cfg.get("templates"):
            lines.append(f"**Templates** (`{base}/templates/`):")
            for tmpl, purpose in cfg["templates"]:
                lines.append(f"- `{tmpl}` — {purpose}")
            lines.append("")
        if cfg.get("data"):
            lines.append(f"**Data** (`{base}/data/` or `.ai/data/`):")
            for data, purpose in cfg["data"]:
                lines.append(f"- `{data}` — {purpose}")
            lines.append("")

    lines += [
        "---",
        "",
        "## Layer Boundaries",
        "",
        "| Layer | File | Owns |",
        "|-------|------|------|",
        f"| Identity | `SOUL.md` | Who {display} is |",
        f"| **Skills** | `SKILLS.md` (this file) | What tools/workflows to load |",
        f"| Operations | `{agent_id}.md` | How to execute work |",
        f"| Delegation | `SUBAGENTS.md` | When to invoke other agents |",
        "",
        "Skills answer *what to load*; they do not replace operational procedure in `{id}.md`.".format(
            id=agent_id
        ),
    ]
    return "\n".join(lines) + "\n"


def render_subagents(agent_id: str, cfg: dict, platform: str) -> str:
    base = platform_base(platform)
    display = cfg["display_name"]
    subagents_intro = cfg.get(
        "subagents_intro",
        "Delegate work outside this agent's domain. Never invoke for work this agent owns.",
    )
    lines = [
        "---",
        f"agent_id: {agent_id}",
        f"display_name: {display}",
        "layer_type: subagents",
        f"pairs_with: {base}/agents/{agent_id}/{agent_id}.md",
        META,
        "---",
        "",
        f"# {display} — Agent Subagents",
        "",
        f"> Delegation layer for {cfg['role_title']}. Defines when and how to invoke other agents via the Task tool.",
        f"> {subagents_intro}",
        "",
        "---",
        "",
        "## Invocation Rules",
        "",
    ]
    default_rules = [
        "Use the **Task tool** with `subagent_type`, `prompt`, and `description`.",
        "Include: goal, acceptance criteria, artifact paths, and relevant context.",
        "Invoke only when criteria in the delegation table are met.",
        f"Never invoke another agent for work {display} owns end-to-end.",
        "Compress context at handoffs — no full transcript dumps.",
    ]
    for rule in cfg.get("subagent_rules", default_rules):
        lines.append(f"- {rule}")

    lines += [
        "",
        "---",
        "",
        "## Delegation Map",
        "",
        "| Agent | ID | When to invoke | Never when |",
        "|-------|-----|----------------|------------|",
    ]
    for d in cfg.get("delegations", []):
        tier = d.get("tier", "—")
        never = d.get("never", "—")
        when = d.get("when", "—")
        if tier != "—":
            when = f"{when} (tier: {tier})" if agent_id == "ceo" else when
        lines.append(f"| {d['name']} | `{d['id']}` | {when} | {never} |")

    lines += ["", "---", "", "## Prompt Templates", ""]
    for label, template in cfg.get("prompt_templates", []):
        lines.append(f"### {label}")
        lines.append("")
        lines.append("```")
        lines.append(template)
        lines.append("```")
        lines.append("")

    if not cfg.get("prompt_templates"):
        lines.append("*See operational spec `Agent Orchestration` section for examples.*")
        lines.append("")

    lines += [
        "---",
        "",
        "## Anti-Patterns",
        "",
        f"- **Circular delegation.** {display} invokes Devon who invokes {display} for the same task.",
        "- **Capability invention.** Invoking an agent for work not in their `agents.index.yaml` description.",
        "- **Prompt starvation.** Task prompt missing acceptance criteria or file paths.",
        "- **Proxy implementation.** Using subagents to do this agent's core deliverable.",
        "",
        "---",
        "",
        "## Layer Boundaries",
        "",
        "| Question | Answer in… |",
        "|----------|------------|",
        f"| Who delegates? | `{agent_id}.md` orchestration sections |",
        "| When to delegate? | `SUBAGENTS.md` (this file) |",
        f"| What skills before delegating? | `SKILLS.md` |",
        f"| Who is {display}? | `SOUL.md` |",
    ]
    return "\n".join(lines) + "\n"


def patch_operational(content: str, agent_id: str, platform: str) -> str:
    base = platform_base(platform)
    skills = f"{base}/agents/{agent_id}/SKILLS.md"
    subagents = f"{base}/agents/{agent_id}/SUBAGENTS.md"
    soul = f"{base}/agents/{agent_id}/SOUL.md"

    skills_line = (
        f"**Skills layer:** Load `{skills}` for capability triggers, task workflows, and checklists.\n\n"
    )
    sub_line = (
        f"**Subagents layer:** Load `{subagents}` for delegation map and Task tool templates.\n\n"
    )

    content = re.sub(r"\n\*\*Skills layer:\*\*[^\n]+\n+", "\n", content)
    content = re.sub(r"\n\*\*Subagents layer:\*\*[^\n]+\n+", "\n", content)

    identity_line = (
        f"**Identity layer:** Load `{soul}` for personality, tone, and identity constraints. "
        f"Pairs with this operational spec.\n\n"
    )
    block = identity_line + skills_line + sub_line
    if "**Skills layer:**" not in content:
        content = re.sub(
            r"\*\*Identity layer:\*\* Load `[^`]+` for personality, tone, and identity constraints\. Pairs with this operational spec\.\n+",
            block,
            content,
            count=1,
        )

    dep_skills = f"- `{skills}` (skills: capabilities, tasks, checklists)\n"
    dep_sub = f"- `{subagents}` (subagents: delegation map, Task templates)\n"
    if dep_skills.strip() not in content:
        soul_dep = f"- `{soul}` (identity: personality, tone, constraints)\n"
        if soul_dep in content:
            content = content.replace(soul_dep, soul_dep + dep_skills + dep_sub, 1)
        elif "## Dependencies" in content:
            content = content.replace(
                "## Dependencies\n\n",
                "## Dependencies\n\n" + dep_skills + dep_sub,
                1,
            )

    content = re.sub(
        r"(identity: personality, tone, constraints)\nYou have access",
        r"\1\n\nYou have access",
        content,
    )
    content = re.sub(
        r"(identity: personality, tone, constraints)\n(- `)",
        r"\1\n\n\2",
        content,
    )
    content = re.sub(
        r"(identity: personality, tone, constraints)\nOn activation",
        r"\1\n\nOn activation",
        content,
    )

    return content


def patch_soul(content: str, agent_id: str) -> str:
    """Update Identity vs Operations table."""
    table = f"""| What skills and checklists apply? | `agents/{agent_id}/SKILLS.md` |
| When to delegate to other agents? | `agents/{agent_id}/SUBAGENTS.md` |"""
    if "SKILLS.md" in content and "SUBAGENTS.md" in content:
        content = re.sub(
            r"\| What checklists/tasks apply\? \|[^\n]+\n",
            table + "\n",
            content,
        )
    elif "## Identity vs Operations" in content:
        content = content.replace(
            f"| How does",
            table + "\n| How does",
            1,
        )
    return content


def generate_for_platform(agents_root: Path, platform: str) -> None:
    for agent_id, cfg in AGENT_CONFIG.items():
        agent_dir = agents_root / agent_id
        if not agent_dir.is_dir():
            continue
        (agent_dir / "SKILLS.md").write_text(
            render_skills(agent_id, cfg, platform), encoding="utf-8"
        )
        (agent_dir / "SUBAGENTS.md").write_text(
            render_subagents(agent_id, cfg, platform), encoding="utf-8"
        )
        op = agent_dir / f"{agent_id}.md"
        if op.exists():
            op.write_text(patch_operational(op.read_text(encoding="utf-8"), agent_id, platform), encoding="utf-8")
        soul = agent_dir / "SOUL.md"
        if soul.exists():
            soul.write_text(patch_soul(soul.read_text(encoding="utf-8"), agent_id), encoding="utf-8")
        print(f"  ✓ {platform}/{agent_id}/ SKILLS + SUBAGENTS")


def main() -> None:
    print("Generating GitAgent SKILLS.md and SUBAGENTS.md layers...")
    for platform, root in PLATFORMS.items():
        generate_for_platform(root, platform)
    print("Done.")


if __name__ == "__main__":
    main()
