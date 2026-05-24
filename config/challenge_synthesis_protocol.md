# Challenge/Synthesis Protocol v1.0

## Purpose

This document is the **runtime-agnostic interface contract** for two-phase challenge/synthesis collaboration. It defines what each phase must receive and produce. Any runtime that satisfies this contract is a valid implementation — Claude Code, a shell script, a Jupyter notebook, or manual two-conversation orchestration are all equivalent at the protocol layer.

The protocol exists because genuine challenge and integrated synthesis are structurally incompatible goals within a single LLM invocation. A model asked simultaneously to challenge and synthesize will coherence-drift toward synthesis. Separating them into distinct execution contexts removes the conflict.

---

## Two-Phase Architecture

```
[Original Request + Domain Context]
          │
          ▼
    ┌─────────────┐
    │  Phase 1    │  ← Challenge Phase (separate invocation)
    │  Challenge  │    Adversarial lens. No synthesis framing.
    └──────┬──────┘
           │  Challenge Artifact
           ▼
    ┌─────────────┐
    │  Phase 2    │  ← Synthesis Phase
    │  Synthesis  │    Unified voice. Full team integration.
    └─────────────┘
```

---

## Phase 1: Challenge

**Purpose**: Surface weaknesses in the premise before solutions form. The challenge phase must be adversarial without being hostile — its job is to find what's wrong, missing, or unexamined.

**Behavioral contract**:
- No synthesis framing, no "let me help you with that" orientation
- Interrogate the premise, not just the implementation
- Identify hidden assumptions the request takes for granted
- Generate alternative framings that recast the problem
- Surface risks, edge cases, and second-order effects
- Ask questions that must be answered before good synthesis is possible

**Inputs**:
- `original_request`: The user's request verbatim
- `domain_context`: The active `challenge_focus` from the domain's `context_configuration.json`
- `active_personas`: Which specialist lenses should challenge (optional; defaults to all relevant)

**Output — Challenge Artifact**:

```
CHALLENGE ARTIFACT
==================
Original request: [verbatim]

Premise flags:
- [assumption being taken for granted]
- [hidden constraint the request doesn't acknowledge]

Risks and edge cases:
- [what breaks at scale / under edge conditions]
- [second-order effect not considered]

Alternative framings:
- [restatement that changes the solution space]
- [different problem that the request might actually be solving]

Required clarifications before synthesis:
- [question that must be answered for good synthesis]
- [decision that hasn't been made but needs to be]

Challenge verdict: [PROCEED | REFRAME | DEFER]
```

The artifact format is intentionally human-readable. Structure matters; verbosity does not. A good challenge artifact is concise and pointed.

---

## Phase 2: Synthesis

**Purpose**: Produce a unified, integrated response that has genuinely absorbed the challenge artifact. The synthesis phase speaks with the authority of the full team and the humility of having been challenged.

**Behavioral contract**:
- Address every `Required clarification` from the challenge artifact (or state why it's deferred)
- Acknowledge reframings that changed the synthesis direction
- If `Challenge verdict` is REFRAME: lead with the reframing before solving
- If `Challenge verdict` is DEFER: state what's missing and what would unlock synthesis
- Primary voice system applies: one voice leads, others woven in seamlessly

**Inputs**:
- `original_request`: The user's request verbatim
- `challenge_artifact`: Full output of Phase 1
- `domain_context`: Full domain `context_configuration.json`

**Output**: Unified synthesis response per the active collaboration framework

---

## Conforming Runtimes

All of the following satisfy the protocol. None are required infrastructure.

| Runtime | How to run Phase 1 | How to run Phase 2 |
|---|---|---|
| **Manual two-conversation** | New chat with `challenge_phase_prompt.md` as system prompt | New chat (or same) with challenge artifact pasted as context |
| **Shell script + any LLM CLI** | `llm -s "$(cat challenge_phase_prompt.md)" "$request"` | `llm -s "$(cat synthesis_prompt.md)" "$request + $artifact"` |
| **`llm` CLI (Simon Willison)** | Same as above; swap backend with `-m model_name` | Same |
| **Claude Code** (reference impl) | `/challenge [request]` — see `.claude/commands/challenge.md` | `/synthesize [request]` — see `.claude/commands/synthesize.md` |
| **Jupyter notebook** | Cell 1: challenge API call | Cell 2: synthesis API call with Cell 1 output |
| **Python script** | `anthropic.messages.create(system=challenge_prompt, ...)` | `anthropic.messages.create(system=synthesis_prompt, messages=[..., artifact])` |

The shell script pattern is the most portable and philosophically explicit: it treats the protocol as UNIX composition.

---

## Domain Challenge Focus

Each domain's `context_configuration.json` contains a `challenge_focus` field that scopes the adversarial lens. The challenge phase uses this as the primary interrogation axis.

| Domain | `challenge_focus` |
|---|---|
| development | `architecture_goals_and_software_correctness` |
| financial | `long_term_financial_outcomes_and_competing_priorities` |
| gaming | `narrative_goals_and_player_experience` |
| writing | `story_goals_and_narrative_consistency` |
| ai_development | `platform_capabilities_and_implementation_constraints` |

---

## What This Protocol Does Not Define

- **Persona identity**: Governed by individual persona schemas
- **Team composition**: Governed by team definition files
- **Synthesis voice patterns**: Governed by `persona_collaboration_framework_v2.md`
- **Domain-specific expertise routing**: Governed by `context_configuration.json`

This protocol defines only the seam between challenge and synthesis. Everything else is downstream.

---

## Verification

A conforming implementation satisfies all of the following:

1. Phase 1 can run in complete isolation from synthesis framing — no "how can I help" orientation, no solution-building
2. The challenge artifact is legible to a human without running any code
3. Phase 2 explicitly addresses or acknowledges every item in the challenge artifact
4. The full protocol can be exercised via manual two-conversation orchestration (no tooling required)
5. Swapping the LLM backend requires changing one variable, not the protocol structure
