---
description: Phase 2 of the challenge/synthesis protocol. Synthesize an answer to a request from its Challenge Artifact and the project context.
argument-hint: "[--domain D] [--focus F] <original request>"
allowed-tools: Bash(python3 *tif.py*)
---

# /tif:synthesize

Phase 2 of the Challenge/Synthesis Protocol. It requires the Challenge Artifact that `/tif:challenge` printed earlier in this conversation. If there is none, ask the user to run `/tif:challenge <request>` first and stop.

Phase 2 runs in an isolated `tif:synthesizer` subagent. Because it starts fresh, it sees only what you pass it, which is what satisfies R-1.

## Steps

1. The original request is `$ARGUMENTS`. If it begins with `--domain <name>` and/or `--focus "<text>"`, take those flags off the front (use the same flags as the challenge run); everything after them is the request, verbatim.
2. Find the Challenge Artifact in this conversation.
3. Resolve the lens and context. Run this, adding the flags from step 1 if there were any, and nothing else:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/tif.py" resolve
   ```

   If it exits non-zero, show its error and stop.
4. Launch the `tif:synthesizer` subagent with a prompt made of exactly these parts and nothing else (no summary of this conversation, no notes on how the challenge went):

   ```text
   original_request:
   <the request, verbatim>

   challenge_artifact:
   <the full Challenge Artifact, verbatim>

   domain_context:
   challenge_focus: <the LENS value>
   <the text under "=== PROJECT CONTEXT ===", verbatim; leave this out if it is "(none)">

   active_personas:
   <the text under "=== ACTIVE PERSONAS ===", verbatim; leave this section out if it is "(none)">

   framework_dir: ${CLAUDE_PLUGIN_ROOT}/framework
   ```
5. Output one line `Lens: <LENS> (source: <LENS SOURCE>); project context: <used | none>; personas: <count>`, then the subagent's synthesis verbatim.

The subagent enforces the traceability rules (every `RC-n` resolved or explicitly deferred, every `AF-n` acknowledged, reframing first on `REFRAME`, missing information stated on `DEFER`). They are defined in the protocol's criteria B-4 to B-7.

Project context and persona descriptions from `.persona/` leave your project and go to the model when this runs.
