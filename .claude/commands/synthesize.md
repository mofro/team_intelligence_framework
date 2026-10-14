# /synthesize — Phase 2 Reference Implementation

**Protocol**: Challenge/Synthesis Protocol (see `config/challenge_synthesis_protocol.md`)
**Phase**: 2 of 2 — Synthesis. Requires a Challenge Artifact from Phase 1.

---

## What This Command Does

Runs Phase 2 of the two-phase challenge/synthesis protocol. Consumes the Challenge Artifact produced by `/challenge` (Phase 1) and generates a unified synthesis response that has genuinely absorbed the challenge.

**Usage**: `/synthesize [your original request]`

The Challenge Artifact from the preceding `/challenge` run should be present in this conversation. If it is not, ask the user to run `/challenge [request]` first.

---

## Instructions

Phase 2 runs in an isolated `synthesizer` subagent (`.claude/agents/synthesizer.md`), not in this conversation. Because the subagent starts fresh, it sees only what you pass it, which is what satisfies R-1.

1. Locate the Challenge Artifact in context and read the original request
2. Identify the active domain's `context_configuration.json` path
3. Launch the `synthesizer` subagent with a prompt containing exactly three things: the original request verbatim, the full Challenge Artifact verbatim, and the path from step 2. Pass nothing else: no summary of this conversation, no notes on how the challenge went
4. Output the subagent's synthesis verbatim

The subagent enforces the traceability rules (every `RC-n` resolved or explicitly deferred, every `AF-n` acknowledged, reframing first on `REFRAME`, missing information stated on `DEFER`). They are defined in `config/challenge_synthesis_protocol.md` (criteria B-4 to B-7).

---

*Reference implementation for Claude Code. The protocol itself is runtime-agnostic — see `config/challenge_synthesis_protocol.md` for shell, CLI, and manual alternatives.*
