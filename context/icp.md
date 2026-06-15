# Ideal Customer Profile — CEO-Orchestration

**Last updated:** 2026-06-15

## Primary user

**Solo operator or small team** building with multiple AI coding assistants who need:

- Consistent specialist agents across Claude, Codex, Copilot, Gemini
- Durable memory (team-brain) beyond single chat sessions
- Lean orchestration without full BMAD overhead

## Characteristics

- Semi-technical: comfortable with git, markdown, and CLI agents
- Runs 2–4 AI platforms for different strengths
- Wants agents to **execute** with human gates only at high stakes
- Values token efficiency and observable orchestration

## Jobs to be done

1. Route requests to the right specialist automatically (Cleo triage)
2. Keep context across sessions (`context/`, `specs/`, agent `memory/`)
3. Process raw notes into structured work (inbox → specs)
4. Ship features with PM → Dev → QA pipeline
5. Tune the system without breaking prompts (Pepe + validation CI)

## Anti-personas

- Large enterprise needing formal RACI and SSO-only workflows
- Teams wanting a single opaque "do everything" agent with no gates
- Users who never touch git or repository structure
