## Context

See proposal.md for motivation. Current state, from an audit of the repo on 2026-10-09:

- 25 persona-shaped files (24 personas plus the template `persona_schema_example.json`, about 93 KB), all `schema_version` 1.2 with identical `persona` keys and near-identical `metadata` keys. `persona.persona_name` is unique.
- 6 team files. Five resolve fully against persona names. `intelligence_framework_team` lists four members with no file.
- Team ids show the same file-name-versus-id pattern: `react_fullstack_team.json` defines `react_fullstack_development_team` and `news_aggregation_team.json` defines `news_aggregation_app_team`. The development context config uses the file-name spelling (`react_fullstack_team`). This was found while running the generator, not in the first audit.
- 7 `context_configuration*.json` files. In `personas/development/context_configuration.json`, four persona ids (`developer_coding_persona`, `10_foot_ui_designer`, `design_expert`, `ott_ux_persona`) are the file-name stems of personas whose `persona_name` is different (`experienced_developer`, `ui_designer`, `ux_ui_strategist`, `ux_designer`). It also lists `security_review_team`, which exists only as an example in a Markdown file with a `.json` extension.
- The framework is configuration read by an LLM. No code in this repo loads these files.
- `CONFIG_REFERENCE.md` and `PERSONA_FRAMEWORK_IMPLEMENTATION_GUIDE.md` (line 215) say ids are `persona_name` values.
- The root `teams/` directory is empty. The existing `.github/workflows/collect-context.yml` is an unrelated deploy template.

## Goals / Non-Goals

**Goals:**
- A deterministic index, derived entirely from files already in the repo, that a consumer can use to fetch a subset.
- Zero changes to the format or content of existing persona, team or context files.
- A process guard so teams cannot again name members that have no file.

**Non-Goals:**
- Tags and any keyword/search ranking. Domain from path, summary, role and expertise are enough for a first version.
- Changes in `persona-conductor-proto`. This change specifies the contract only.
- A slimmer or derived persona format. The index only points at the unmodified files.
- A hosted service or package registry. The index is a static file served by GitHub.
- Rewriting existing ids anywhere.

## Decisions

### Decision: do not edit context_configuration; resolve mismatches with aliases

The id mismatches look like a simple rename, but I could not establish that a rename is safe, so this change does not make it.

What was found when tracing usage of the four stale ids:

- They are used as keys and values inside `personas/development/context_configuration.json` (`available_personas`, `always_on_personas`, `default_primary_persona`, `collaboration_patterns` keys such as `developer_coding_persona` and `10_foot_ui_designer`). Renaming means changing both values and JSON keys.
- `developer_coding_persona` is also the always-on and default-primary persona and appears in `config/persona_interaction_architecture_v1.md:100` as the user-facing handle `@developer_coding_persona` and in `config/persona_collaboration_framework_v1.md:127`. `USER_GUIDE.md` teaches `@experienced_developer`. The docs already disagree about what users type.
- `ARCHITECTURAL_DECISIONS.md:176` lists the stale ids in a checklist, which is a historical record.
- The files that users have already copied by hand into their own projects, and anything Conductor has already installed, may use either spelling. A rename here does not reach those copies.
- Since the framework is read by an LLM, a mismatched id degrades silently (the model may fuzzy-match) rather than failing. That makes it hard to tell from a test whether a rename helped or changed behavior, for example which persona is always-on.

Decision: leave all context files untouched, make both spellings resolve through `aliases` in the index (for consumers), and report the mismatches as informational notes. The behavior of existing sessions is unchanged.

Alternatives considered:
- **Rename ids in the config to `persona_name`.** Matches the documented convention, but changes which handle is "always-on" in a live config and breaks the older docs and any user copies. Needs its own change with a before/after behavior check, and a decision on which spelling users should type.
- **Rename `persona_name` in the persona files to match the config.** Larger blast radius: team files, USER_GUIDE, TODO, transcripts and the journal use the current names.
- **Do nothing.** Leaves consumers unable to resolve the config ids.

A follow-up change, "reconcile development context ids", is recommended only after deciding which spelling users should type. This change makes that follow-up easier because the generator will list exactly what resolves only via alias.

### Decision: canonical id is `persona.persona_name`

It is already unique, already what team files use, and already documented as the id. Consumers get one stable id and the aliases handle the rest. Alternatives: the file stem (inconsistent suffixes, `_schema`/`_persona`/`_v1.1`) or a new `id` field (would modify every persona file).

### Decision: alias derivation

Aliases exist for consumers reading the index. They do not change how the framework treats ids in a session. Whether the framework copes with the mismatched ids today has not been verified; a manual check (addressing `@design_expert` and `@ux_ui_strategist` in a development session) would settle it.

Aliases are the file-name stem plus the stem with the trailing version suffix (`_v<digits>[.<digits>]`), then `_schema`, then `_persona` stripped one at a time. A dry run over the 25 current files showed no alias maps to two personas, no alias equals a different persona's canonical id, and all four stale config ids resolve to exactly one persona each. Collisions are errors so a future persona cannot silently steal an alias.

The same derivation applies to team files, which have the same mismatch.

Alternative considered: a hand-maintained alias table. Rejected because it would drift, which is the problem this change addresses.

### Decision: generated, committed, deterministic index with CI freshness check

`index.json` is committed so consumers can fetch it with a plain GitHub raw URL, and generated so it cannot drift from the persona files. No timestamps or commit hashes go in the file, otherwise every commit would make it stale. Staleness is detected by regenerating in memory and diffing, run in CI. Integrity comes from sha256 of exact file bytes.

Language: Python 3 standard library only. It is already available on the user's machine and on GitHub runners, adds no dependency or `package.json`, and the work is JSON walking and hashing. Alternatives: Node (the repo has no `package.json`), shell with `jq` (fragile for the alias and validation logic).

Output formatting: sorted keys within entries where order is not meaningful, entries sorted by `id`, two-space indent, trailing newline, UTF-8 without BOM.

### Decision: severity model

Errors fail generation and CI: unparseable candidate files, missing required fields, duplicate `persona_name`, alias collisions, team members or `default_primary` that do not resolve. Warnings and notes never fail: context-config references that resolve only via alias (note) or not at all (warning).

Unresolved team members are an error because that is the process failure this change closes: a team referring to a persona that exists only in a conversation. Context-config problems are warnings because five of them exist today and are being deliberately left alone, and failing CI on them would force the rename this change defers.

### Decision: teams are first-class index entries and a bundle install path

Team entries carry `members`, so selecting a team expands to the team file plus member personas. This is how a team becomes a shorthand for "download these personas", alongside the individual path. The team file is included because it contains `default_primary`, activation keywords and collaboration notes the framework uses.

### Decision: stub personas, marked with an optional top-level key

The four missing members get stub files so the team resolves, the CI error is satisfied, and, more importantly, so the gap is visible and self-correcting rather than just silenced.

How the "imperative to flesh out" works inside the existing framework: the stub's `behavioral_rules` carries a rule to announce its stub status on first invocation per session and offer to define itself from the work in progress, without refusing the task. This relies only on the mechanism all personas already use (rules read by the model), with no new framework behavior.

Marker: `"stub": true` at the top level. It is additive, optional, and absent from complete personas, so the 25 existing files are unaffected. Alternatives: a `metadata.status` field (would invite adding it to every file for consistency), a filename suffix such as `_stub` (renaming on completion would break paths and git history), or a separate stubs list (a second source of truth that can drift from the files).

Seed content: each stub's `role`, `expertise` and `approach` are derived only from `intelligence_framework_team.json`'s `decision_hierarchy` and `collaboration_patterns` lines, for example "Technical architecture decisions" for `system_architect`. Nothing is invented beyond that, and the stub says so. Location and naming follow the repo convention: `personas/ai_development/<persona_name>_persona_schema.json`.

### Decision: index contents are limited to fields in existing files

Entries copy `role`, `expertise`, `schema_version` and `version` from the existing persona files and add only derived values (`domain`, `subdomain`, `path`, `bytes`, `sha256`, `aliases`, `status`). This honors the backward-compatibility constraint: there is no second persona format.

### Decision: keep the retrieval contract minimal, park the rest

Conductor is a separate repo and this repo cannot enforce what a consumer does. The specs therefore require only what this repo controls: a fetchable index, lookup by id or alias, and team entries that list their members. Consumer-side behavior (hash verification, compatibility checks, stub and dependency disclosure, install layout, listing context configs and dependencies in the index) is recorded as roadmap items in `docs/persona-index-roadmap.md`, to be pulled into Conductor's work or into this repo's index when a consumer needs them. `sha256` and `bytes` stay in the index because they are free to generate and make those later features possible.

## Risks / Trade-offs

- [Stub text is guesswork about roles the user improvised] → Seed only from team-file statements, label the stub as such, and mark the team as containing stubs in the index and at install time.
- [A stub's "announce yourself" rule is only a model instruction and may be inconsistently followed] → It is a nudge, not a gate. The index `status` and install-time disclosure give a second, deterministic signal.
- [Aliases hide the id inconsistency instead of fixing it] → Intentional for this change. Generation prints every alias-resolved config reference so the follow-up change has an exact worklist.
- [Committed generated file can conflict on merges] → Single regenerate command, CI check explains it, and ordering is deterministic so conflicts are mechanical.
- [Consumers fetching from `main` get a moving target] → Tag pinning is a roadmap recommendation. This change does not cut a release.
- [Conductor may need fields or behavior this repo-side design cannot anticipate] → Its loading code has not been read for this change. The contract in persona-retrieval is deliberately small, and the roadmap file lists likely additions.
- [Adding the `stub` key could surprise a strict reader] → The framework reads files as prompt context, and no code validates keys. The key is documented, and the generator is the only thing that interprets it.

## Migration Plan

1. Add stubs, generator, workflow and `index.json` in one branch/PR. Existing files are untouched, so there is no data migration.
2. Run the generator and review its error, warning and note output. The expected result is zero errors, one warning (`security_review_team`), and notes for the four alias-resolved ids.
3. Merge, then optionally tag a release for Conductor to pin to.
4. Rollback: delete `index.json`, the script, the workflow and the stub files. Nothing else depends on them.

## Open Questions

- Which spelling should users type for the development personas (`@developer_coding_persona` or `@experienced_developer`)? Needed for the deferred follow-up change, not for this one.
- Does Conductor need `context_configuration.json` files at all? If so, listing them in the index is a roadmap item.
- Should `security_review_team` become a real team file or be removed from `available_teams`? It is reported as a warning until decided.
