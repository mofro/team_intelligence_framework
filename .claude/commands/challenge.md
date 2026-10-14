# /challenge — Phase 1 Reference Implementation

**Protocol**: Challenge/Synthesis Protocol (see `config/challenge_synthesis_protocol.md`)
**Phase**: 1 of 2 — Challenge only. Do not synthesize.

---

## What This Command Does

Runs Phase 1 of the two-phase challenge/synthesis protocol against the provided request. Produces a Challenge Artifact that the `/synthesize` command (Phase 2) consumes.

**Usage**: `/challenge [your request]`

---

## Instructions

Phase 1 runs in an isolated `challenger` subagent (`.claude/agents/challenger.md`), not in this conversation. The subagent is read-only and cannot see this conversation, which is what satisfies R-1.

1. Read the request provided after `/challenge`
2. Identify the active domain context and its `challenge_focus` from the loaded `context_configuration.json`. If no domain context is active, use "first principles: correctness, completeness, and coherence"
3. Launch the `challenger` subagent with a prompt containing only `challenge_focus: <value>` and the request verbatim. Add nothing else: no background, no history, no summary of this conversation
4. Output the subagent's Challenge Artifact verbatim. Do not edit it, add commentary, or offer solutions

The user will then run `/synthesize` with the same request.

---

## Challenge Artifact Format

Every list entry MUST carry a stable ID (`PF-n`, `RE-n`, `AF-n`, `RC-n`) — synthesis traces against these IDs.

```
CHALLENGE ARTIFACT
==================
schema_version: 1.1
verdict: PROCEED | REFRAME | DEFER

original_request: [verbatim]

premise_flags:
- [PF-1] ...

risks_and_edge_cases:
- [RE-1] ...

alternative_framings:
- [AF-1] ...

required_clarifications:
- [RC-1] ...

context_consulted:       # optional; omit if nothing was read
- [path or source]
```

Full schema, cardinality rules, and conformance criteria: `config/challenge_synthesis_protocol.md`.

---

*Reference implementation for Claude Code. The protocol itself is runtime-agnostic — see `config/challenge_synthesis_protocol.md` for shell, CLI, and manual alternatives.*
