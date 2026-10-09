# Proposal: changes to TIF for compatibility with persona-conductor

Status: **all six items applied on this branch (004b6d4, 5603ab2, f872856, 9fc629b, e5c9a98, 7ae0f97); item 2 in a reduced form (see its section).**
The first two commits on the branch were this document alone. Sections below describe each item as proposed; an
**Applied** line says what was actually done, including where it departs from the proposal.
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
- **Applied (004b6d4):** both docs updated and the superseded form marked; `10_foot_ui_designer` now defers to the domain
  `user_experience_design` (a domain name taken from the UX persona's `expertise_scope`, my choice of mapping).

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
- **Cost / risk:** the largest item, and someone must decide what each `path` is. Do not do it unless TIF itself wants lazy references.
- **Found while preparing it (2026-10-07):** the entries are objects `{type, description, url}`, not strings, in 21
  persona files. Many `url` values are `internal://...` placeholders with no file behind them (all financial and screenplay
  personas, parts of development), the rest are real web URLs. So there is no local path to write for any of them without
  inventing a document. A mechanical rename to `references: [{when, source}]` (no `path`) is possible but would leave
  entries nothing can load.
- **Two more nonexistent guides found in the same scan** (missed in item 3): `financial/context_configuration.json` lists
  `financial_collaboration_guide.md`, and `writing/screenplays/context_configuration_screenplays.json` lists
  `writing_collaboration_guide.md`; neither existed. **Resolved (a3587c2):** skeleton guides now exist (`status: skeleton`,
  structure from `personas/examples/financial_team_collaboration_guide.md`); filling them in is tracked in
  [issue #8](https://github.com/mofro/team_intelligence_framework/issues/8). Review of this branch is issue #7.
- **Applied in reduced form (7ae0f97, reviewer decision 2026-10-08):** `reference_libraries` in the 21 persona files became
  `references: [{"description": ...}]`. `type`, `url` and `depth` were dropped (68 entries: 41 https URLs, 27 `internal://`
  placeholders). No `path` was written because no local files exist; one can be added per entry later. Compiled plugin output for
  the security specialist is byte-identical before and after. The URLs are gone from the files but remain in git history.

### 3. Missing and nonexistent references in `development/context_configuration.json`

- **Found:** `reference_libraries` lists four files. `ARCHITECTURAL_DECISIONS.md` exists in TIF. The other three do not:
  - `PERSONA_ENGAGEMENT_GUIDE.md` and `FILE_PERSISTENCE_GUIDELINES.md`: exist only in HeroHeaven. **These are
    not dangling by mistake.** TIF's overview template lists `PERSONA_ENGAGEMENT_GUIDE.md` in every context's
    `reference_libraries`, and `personas/gaming/hero_heaven/context_configuration_hero_heaven.json` reaches both through
    `{PROJECT_ROOT}/`. They are per-project files that each project supplies; the domain contexts (development, gaming,
    financial, writing, AI development) name them as the expected filenames. (The first draft of this document called them
    dangling; that was wrong.) The HeroHeaven copies are project-specific: frontmatter `project: TTRPG_Hero_Heaven`,
    examples such as `world/mechanics.md`, rules about the Lore Keeper, and an unfilled `{{date}}` placeholder.
  - `development_collaboration_guide.md`: **not found.** Searched 2026-10-07: file names across the whole disk,
    Spotlight, TIF git history (never added or deleted), `~/Code` and HeroHeaven text, and the file listings of six
    zip archives. The only mentions are the config line itself. It was most likely named but never written.
    Not searched: file contents of conversation exports or notes, other zips, anything off this machine.
  - `security_review_team` (line 60): no such file is in `personas/development/teams/`; the name appears only as an
    example in `personas/examples/team_definition_examples.json`.
- **Change:** remove `development_collaboration_guide.md` and `security_review_team`. Leave the two
  project-supplied filenames, and state in the overview that projects supply them.
- **Why:** a reader (or model) following the first two hits nothing and has no explanation. The other two are by design.
- **Plugin impact if skipped:** none; the plugin ignores these fields.
- **Applied (5603ab2, 004b6d4):** the two entries were removed from the development context. The overview gained a
  note that projects supply `PERSONA_ENGAGEMENT_GUIDE.md` and `FILE_PERSISTENCE_GUIDELINES.md`.
  Reversible: if a copy of `development_collaboration_guide.md` turns up, restore the line.

### 4. The HeroHeaven engagement guide is project-level

- **Found:** `PERSONA_ENGAGEMENT_GUIDE.md` (165 lines in the older copy) is project-specific: its frontmatter says
  `project: TTRPG_Hero_Heaven` and it opens with the Lore Keeper's autonomous-editing and "Ahem..." protocols.
  23 persona files carry `reference_guide: "See PERSONA_ENGAGEMENT_GUIDE.md ..."`, which under the per-project design
  above points at whatever guide the using project supplies. TIF already has `personas/gaming/hero_heaven/` holding that
  project's personas and context.
- **Copies on this machine:** `~/Documents/Games/HeroHeaven 2/` (2025-12 versions, not a git repo),
  `~/Documents/Games/HeroHeaven/.meta/` (2026-03-15, larger: the engagement guide is 8,626 bytes against 8,487 and the
  persistence guidelines 3,242 against 1,461), and 2025-12 versions inside `~/Documents/Games/HeroHeaven.zip`.
  The `.meta` copies are the newest, and the hero_heaven context's `project_root` is `~/Documents/Games/HeroHeaven`.
- **Change:** copy the newest versions into `personas/gaming/hero_heaven/` as that project's documents.
- **Why:** project docs belong with the project's personas, and it gives the template a worked example.
- **Plugin impact if skipped:** none.
- **Applied (f872856):** both `.meta` copies were added to `personas/gaming/hero_heaven/`.
  **Departure from the first draft:** the 23 `reference_guide` pointers were *not* repointed, because they refer to the
  project-supplied file, not to this copy. No persona file other than `10_foot_ui_designer` (item 1) was edited.
  **Deferred (reviewer decision, 2026-10-07):** whether `hero_heaven`'s own `{PROJECT_ROOT}` references should point at
  the copies in this repo instead of the HeroHeaven folder. Left unchanged; HeroHeaven cleanup will happen later.

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
- **Applied (9fc629b, e5c9a98):** documented in the collaboration framework and the overview. Set on the four colliding
  personas (`UID`, `UXD`, `INSA`, `INVA`, the values the plugin's algorithm would pick anyway). A scan of all 24 persona
  files found no other collision.

### 6. Small: glossary

- The plugin's design added a short glossary (belief, consult, deference and similar terms), adopted only where TIF
  has no term. If useful, a section in `framework_configuration_overview.md`. Not needed by the plugin.
- **Applied (e5c9a98):** a short glossary at the end of the overview (five terms from Konolige & Nilsson, AAAI-80).

## How I would rank them

This is the author's view; the decision is the reviewer's.

| Item | Fixes an existing inconsistency in TIF | Helps the plugin | Effort |
|---|---|---|---|
| 1 `defers_to` | yes | no | low |
| 3 nonexistent references | yes | no | low |
| 4 HeroHeaven guides | yes (with 3) | no | low |
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

1. This document (done, a1729c5; revised 08c69b7 and again with the applied commits).
2. Items 1, 3, 4 (done: 004b6d4, 5603ab2, f872856).
3. Item 5: the optional field, documented.
4. Item 6, if wanted.
5. Item 2 only if the reviewer wants lazy references.

Nothing is merged; the branch is pushed to `origin` (2026-10-08) for review under issue #7. The branch can be deleted without effect on the plugin.
