# /challenge — Phase 1 Reference Implementation

**Protocol**: Challenge/Synthesis Protocol (see `config/challenge_synthesis_protocol.md`)
**Phase**: 1 of 2 — Challenge only. Do not synthesize.

---

## What This Command Does

Runs Phase 1 of the two-phase challenge/synthesis protocol against the provided request. Produces a Challenge Artifact that the `/synthesize` command (Phase 2) consumes.

**Usage**: `/challenge [your request]`

---

## Instructions

You are in Challenge Phase. Apply the full behavioral contract from `config/challenge_phase_prompt.md`:

1. Read the request provided after `/challenge`
2. Identify the active domain context and its `challenge_focus` field from the loaded `context_configuration.json`
3. Apply the adversarial lens scoped to that `challenge_focus`
4. Produce a Challenge Artifact in the standard format

**Do not offer solutions. Do not move toward synthesis.**

Output the Challenge Artifact. The user will then run `/synthesize` with the same request, and the artifact will be available as context.

---

## Challenge Artifact Format

```
CHALLENGE ARTIFACT
==================
Original request: [verbatim]

Premise flags:
- ...

Risks and edge cases:
- ...

Alternative framings:
- ...

Required clarifications before synthesis:
- ...

Challenge verdict: [PROCEED | REFRAME | DEFER]
```

---

*Reference implementation for Claude Code. The protocol itself is runtime-agnostic — see `config/challenge_synthesis_protocol.md` for shell, CLI, and manual alternatives.*
