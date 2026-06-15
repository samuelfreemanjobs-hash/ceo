# Spec: 80% Automation Completion

## Problem

Agents are well-defined but operation is human-initiated; memory and triggers are missing.

## Requirements

1. Live `context/`, `inbox/`, `specs/` at repo root
2. Automation scripts in `.ai/utils/` with CI validation
3. GitHub Actions for CI, daily inbox, weekly analytics
4. Platform sync: `.codex` and `.gemini` agent trees
5. Cleo `*approve` + activation protocol on all agents
6. Sample `data/analytics/` for Ana workflows

## Acceptance criteria

- `python3 .ai/utils/validate-agents.py --platform claude` exits 0
- `python3 .ai/utils/validate-agents.py --platform codex` exits 0
- Pre-commit hook documented; `git config core.hooksPath .githooks`
- README reflects tier-adaptive Cleo + live team-brain
