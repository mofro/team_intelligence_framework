---
description: Phase 1 of the challenge/synthesis protocol. Challenge a request against the project context and return a Challenge Artifact. Does not synthesize.
argument-hint: "[--domain D] [--focus F] <request>"
allowed-tools: Bash(python3 *tif.py*)
---

# /tif:challenge

Phase 1 of the Challenge/Synthesis Protocol. Challenge only: do not synthesize, propose solutions or comment on the result.

Phase 1 runs in an isolated `tif:challenger` subagent. It is read-only and cannot see this conversation, which is what satisfies R-1. It receives only what you put in its prompt.

## Steps

1. The request is `$ARGUMENTS`. If it begins with `--domain <name>` and/or `--focus "<text>"`, take those flags off the front; everything after them is the request, verbatim.
2. Resolve the lens and context. Run this, adding the flags from step 1 if there were any, and nothing else:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/tif.py" resolve
   ```

   If it exits non-zero, show its error and stop.
3. Launch the `tif:challenger` subagent with a prompt made of exactly these parts and nothing else (no history, no summary of this conversation, no notes):

   ```text
   original_request:
   <the request, verbatim>

   domain_context:
   challenge_focus: <the LENS value>
   <the text under "=== PROJECT CONTEXT ===", verbatim; leave this out if it is "(none)">

   active_personas:
   <the text under "=== ACTIVE PERSONAS ===", verbatim; leave this section out if it is "(none)">
   ```
4. Output one line `Lens: <LENS> (source: <LENS SOURCE>); project context: <used | none>; personas: <count>`, then the subagent's Challenge Artifact verbatim. Do not edit it, add commentary or offer solutions.

The user then runs `/tif:synthesize` with the same request.

Project context and persona descriptions from `.persona/` leave your project and go to the model when this runs; `.persona/context.md` is plain text you can read and edit.
