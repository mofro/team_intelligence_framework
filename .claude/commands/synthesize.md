# /synthesize — Phase 2 Reference Implementation

**Protocol**: Challenge/Synthesis Protocol (see `config/challenge_synthesis_protocol.md`)
**Phase**: 2 of 2 — Synthesis. Requires a Challenge Artifact from Phase 1.

---

## What This Command Does

Runs Phase 2 of the two-phase challenge/synthesis protocol. Consumes the Challenge Artifact produced by `/challenge` (Phase 1) and generates a unified synthesis response that has genuinely absorbed the challenge.

**Usage**: `/synthesize [your original request]`

The Challenge Artifact from the preceding `/challenge` invocation should be present in context. If it is not, ask the user to run `/challenge [request]` first.

---

## Instructions

You are in Synthesis Phase. Apply the full behavioral contract from `config/challenge_synthesis_protocol.md`:

1. Locate the Challenge Artifact in context (from the preceding `/challenge` run)
2. Read the original request
3. Load the active domain `context_configuration.json` and `persona_collaboration_framework_v2.md`
4. Produce a unified synthesis response that:
   - Traces every `RC-n` in `required_clarifications` — resolve it explicitly or state an explicit deferral with reason; silent omission is a conformance failure (see `challenge_synthesis_protocol.md` criterion B-4)
   - Acknowledges every `AF-n` in `alternative_framings` that changed the synthesis direction (criterion B-5)
   - Leads with the reframing before any solution if `verdict` is `REFRAME` (criterion B-6)
   - States what's missing and does not present a full solution if `verdict` is `DEFER` (criterion B-7)
   - Uses the primary voice system: one persona leads, others woven in seamlessly
   - Applies domain-appropriate expertise routing per the active team/context

**The synthesis response is the team's full, integrated answer. It speaks with the authority of having been challenged.** Conformance criteria for this phase are defined in `config/challenge_synthesis_protocol.md`.

---

*Reference implementation for Claude Code. The protocol itself is runtime-agnostic — see `config/challenge_synthesis_protocol.md` for shell, CLI, and manual alternatives.*
