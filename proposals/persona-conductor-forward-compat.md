# Proposal: changes to TIF for compatibility with persona-conductor

Status: **proposal for review. This commit contains only this document. No TIF file has been edited.**
Written 2026-10-07. Source project: `~/Code/persona-conductor-proto` (`DESIGN.md` section 8, decisions D4, D5, D7, D20).

## Why this exists

`persona-conductor` is a separate Claude Code plugin that conducts TIF-format personas: it
lists the personas in a project, answers in one persona's voice, shows several personas'
disagreements side by side, or briefs sub-agents with a persona. It keeps a decision log per project.
It reads TIF persona JSON directly and does not depend on the TIF repo at runtime; users copy the
personas they want into their project.

While building it, its author compared TIF's documents with TIF's actual files and found places
where they disagree, and a few places where the plugin would be cleaner if TIF chose one form.
This document lists each, says what was found, what the change would be, and what it buys.
The question for the reviewer is **whether any of this is worth changing TIF for**.

## The main point, stated plainly

The plugin works today with unmodified TIF personas. It was tested on the real files, including the
cases below. **None of the changes here is required for it to run.** They are about making TIF
consistent with itself and, secondarily, making the pairing smoother. Each item says whether the
plugin would notice if it were skipped.

## Items

Evidence was re-checked against the repo on 2026-10-07 (commit `1134cab`).

### 1. `defers_to` has three forms; the overview documents a different one

- **Found:** `config/framework_configuration_overview.md` (lines 169, 178, 360) says `defers_to` is a
  list of expertise-domain strings and that it does not use persona names. `config/persona_interaction_architecture_v1.md`
  (line 50) shows `"defers_to": ["other_persona_names"]`. In the 24 persona files: 18 use objects
  `{expertise_domain, description}`, 1 uses strings (`10_foot_ui_designer_persona_schema_v1.1.json`:
  `["ux_designer"]`, which is a persona name), 4 are empty, 1 omits the field (plus the example
  template and `llm_prompt_specialist_persona_schema.json`, which omit it).
- **Change:** document the object form as canonical in the overview and add a short note in the
  interaction architecture marking the persona-name form superseded. Optionally convert the one
  string-form file.
- **Why:** the object carries the reason for deferring, which a conductor can relay. Domain-based
  deference stays portable across teams, which is what the overview says it wants.
- **Plugin impact if skipped:** none. The compiler accepts strings and objects.
- **Cost / risk:** documentation edits plus one JSON edit. Low.

### 2. `reference_libraries` embeds URLs the overview says do not exist

- **Found:** the overview says schemas carry no embedded knowledge bases or URLs. 21 personas
  have `reference_libraries`; 41 entries are `http` URLs across 11 personas (for example the
  security specialist: oauth.net, jwt.io, owasp.org). Entries are a mix of URLs, bare filenames and
  descriptions.
- **Change (D5 in the plugin's design):** replace with `references: [{path, when}]`: local relative
  paths plus a "consult when" hint, loaded only when needed. A URL may survive only as a never-fetched
  `source` provenance string.
- **Why:** a URL in a prompt invites fetching, which costs tokens, drifts, and fails offline. Local
  paths with a trigger hint are what the Persona plugin does and are cheaper.
- **Plugin impact if skipped:** none. The compiler drops `reference_libraries` and `reference_guide`
  from the prompt. **The plugin has no code that reads `references`**: lazy loading was deferred
  until a persona has one. Doing this change alone gives the plugin nothing new.
- **Cost / risk:** the largest item: 21 persona files, and someone must decide what each
  `path` is. Do not do it unless TIF itself wants lazy references.

### 3. Dangling references in `development/context_configuration.json`

- **Found:** `reference_libraries` lists `PERSONA_ENGAGEMENT_GUIDE.md`, `FILE_PERSISTENCE_GUIDELINES.md` and
  `development_collaboration_guide.md`. None exists in TIF. The first two exist in the HeroHeaven 2 project; the third
  was not found anywhere. (`ARCHITECTURAL_DECISIONS.md`, also listed, does exist.) Line 60 lists a team
  `security_review_team`; no such file is in `personas/development/teams/` (the name appears only as an example
  in `personas/examples/team_definition_examples.json`).
  23 persona files also point `reference_guide` at `PERSONA_ENGAGEMENT_GUIDE.md`.
- **Change:** remove or repoint the dangling entries; create or drop the team.
- **Why:** a reader (or model) following these hits nothing.
- **Plugin impact if skipped:** none; the plugin ignores these fields.
- **Cost / risk:** small, but each fix needs a decision (write the missing guide, or delete the reference).

### 4. The HeroHeaven engagement guide is project-level

- **Found:** `PERSONA_ENGAGEMENT_GUIDE.md` lives in HeroHeaven 2 and is specific to that project
  (`project: TTRPG_Hero_Heaven`, Lore Keeper "Ahem" protocol). The development context cites it as if generic.
  TIF already has `personas/gaming/hero_heaven/` holding that project's personas and context.
- **Change:** copy it into `personas/gaming/hero_heaven/`; do not present it as a framework-level guide.
- **Why:** project docs belong with the project's personas.
- **Plugin impact if skipped:** none.
- **Cost / risk:** one file copy, plus fixing the references in item 3.

### 5. Optional `persona.abbreviation` field (new, from plugin decision D20)

- **Found:** TIF defines tags like `[BD] [LD] [SS]` only in prose, to be deduced by the LLM
  (`config/persona_collaboration_framework_v1.md` lines 34-35 and 88-89;
  `config/domain_agnostic_framework.md` lines 59-60, 68, 75). Deducing by initials collides in the real set:
  `ui_designer` and `ux_designer` both give `UD`; `insurance_analyst` and `investment_advisor` both give `IA`.
- **Change:** allow an optional `persona.abbreviation` (1-6 letters or digits) in persona files and mention it in
  the framework docs. Set it where initials collide or read badly.
- **Why:** pins the tag so it does not drift between sessions or between tools.
- **Plugin impact if skipped:** none. The plugin derives tags and resolves collisions itself
  (`UID`/`UXD`, `INSA`/`INVA`). Using the field only makes the choice yours instead of the algorithm's.
- **Compatibility, checked 2026-10-07:** TIF has no code that reads persona JSON, no schema with
  `additionalProperties`, and one persona already has an extra key (`methodology`). An added field is
  not rejected by any tooling. The LLM reads it as text.
- **Cost / risk:** one doc line and, at most, a handful of persona edits.

### 6. Small: glossary

- The plugin's design added a short glossary (belief, consult, deference and similar terms), adopted only where TIF
  has no term. If useful, a section in `framework_configuration_overview.md`. Not needed by the plugin.

## How I would rank them

This is the author's view; the decision is the reviewer's.

| Item | Fixes an existing inconsistency in TIF | Helps the plugin | Effort |
|---|---|---|---|
| 1 `defers_to` | yes | no | low |
| 3 dangling references | yes | no | low to medium |
| 4 move the HeroHeaven guide | yes (with 3) | no | low |
| 5 `abbreviation` | no | slightly | low |
| 2 `references` | partly | no (no consumer yet) | high |
| 6 glossary | no | no | low |

Items 1, 3 and 4 are worth doing on their own merits, whether or not the plugin exists. Item 5 is a
convenience. Item 2 should wait until something consumes it.

## What the plugin does if TIF never changes

It keeps working. It reads `persona`, `collaboration` and `behavioral_rules`, tolerates missing or
oddly typed fields, ignores the rest, and treats users' copies in `.persona/personas/` as the
source of truth. The cost of not retrofitting is TIF's existing inconsistencies staying as they are.

## Proposed commits on this branch (each needs a separate go)

1. This document (done).
2. Items 1, 3, 4: documentation and reference fixes.
3. Item 5: the optional field, documented.
4. Item 6, if wanted.
5. Item 2 only if the reviewer wants lazy references.

Nothing is merged. The branch can be deleted without effect on the plugin.
