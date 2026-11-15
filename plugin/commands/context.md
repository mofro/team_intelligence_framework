---
description: Create or update the project context (.persona/context.md) by interview. The challenge commands use it.
argument-hint: ""
allowed-tools: Read
---

# /tif:context

Interview the user and write `.persona/context.md`: what this body of work is, what exists and is decided, the facts of its world, and what is out of scope. `/tif:challenge` and `/tif:synthesize` read it, so the challenge is aimed at this project and not at a generic one.

## Rules

- Record only what the user says. Do not invent, infer or "improve" facts. If an answer is thin, keep it thin or ask a follow-up; do not pad it.
- Ask in short rounds, one topic at a time, waiting for the answer before the next. Do not present a long questionnaire.
- Do not write any file until the user has seen the full draft and said yes. Write nothing else, anywhere.
- Never overwrite silently.

## Steps

1. Read `.persona/context.md` if it exists. If it does, this is an update: show the user what it says in two or three lines and ask what has changed or is missing, then go to step 5 with proposed edits instead of a new file.
2. Interview, in this order, one round each:
   1. **Goal**: what is this project trying to achieve, and for whom?
   2. **Current state and decisions**: what already exists, and what has been decided (and why, if the user says)?
   3. **World and vocabulary**: facts about the domain a newcomer would get wrong, and terms the project uses in a particular way.
   4. **Constraints and non-goals**: fixed limits, and what the project will not do.
3. Offer a domain. Read `${CLAUDE_PLUGIN_ROOT}/framework/domains.json` and list its domain names with their descriptions. If personas are installed in `.persona/personas/`, you may use their `reference_context` to suggest one. The user decides; "none" is a valid answer. A domain only sets the challenge lens; it does not limit which personas or teams are used. Optionally ask whether the user wants a custom `focus` (one phrase naming what challenges should concentrate on); it overrides the domain's lens.
4. Draft the file. Front matter holds only what the user chose:

   ```markdown
   ---
   domain: <name>      # omit if none
   focus: <phrase>     # omit if none
   ---

   # Goal
   ...

   # Current state and decisions
   ...

   # World and vocabulary
   ...

   # Constraints and non-goals
   ...
   ```

   Leave out a heading the user gave nothing for rather than filling it.
5. Show the complete draft (or, for an update, the proposed edits against the existing text) and ask: "Write this to `.persona/context.md`?" Wait for an explicit yes.
6. On yes, write the file (create `.persona/` if needed) and report the path. On no, write nothing and ask what to change, or stop if the user wants to.

After writing, tell the user that `/tif:challenge` and `/tif:synthesize` will now use it, and that it is plain text they can edit by hand.
