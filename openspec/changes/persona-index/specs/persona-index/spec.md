## Purpose

Provides one machine-readable catalog of every persona and team in this repository, so tools and people can discover what exists and where it lives without scanning directories or copying files by hand.

## ADDED Requirements

### Requirement: Root index file
The repository SHALL contain a file `index.json` at its root that lists every persona and every team in the repository. The file SHALL declare an `index_version`. The file SHALL NOT contain timestamps, commit hashes or any other value that changes when no persona or team file has changed.

#### Scenario: Index regenerated with no catalog changes
- **WHEN** the index is generated twice from the same set of persona and team files
- **THEN** both outputs are byte-identical

#### Scenario: Consumer checks the format version
- **WHEN** a consumer reads `index.json`
- **THEN** it finds an `index_version` it can compare against the versions it supports

### Requirement: Persona qualification
A file SHALL be indexed as a persona if and only if it is a JSON file under `personas/` that has top-level `metadata` and `persona` objects, and is not a team file, a `context_configuration*.json` file, the template `personas/persona_schema_example.json`, or a file under `personas/examples/`. Files that do not parse as JSON SHALL be excluded from persona entries without failing generation when they are under `personas/examples/`.

#### Scenario: Template excluded
- **WHEN** the index is generated
- **THEN** `personas/persona_schema_example.json` does not appear as a persona entry

#### Scenario: Example files that are not JSON
- **WHEN** `personas/examples/` contains Markdown content with a `.json` extension
- **THEN** generation succeeds and those files do not appear in the index

#### Scenario: Unparseable persona file elsewhere
- **WHEN** a file outside `personas/examples/` that would otherwise qualify cannot be parsed as JSON
- **THEN** generation reports an error naming the file

### Requirement: Persona entries
Each persona entry SHALL contain: `id` (the file's `persona.persona_name`), `name` (`metadata.name`), `summary` (`metadata.description`), `role` (`persona.role`), `domain` (the first directory under `personas/`), `subdomain` (remaining directories between the domain and the file, or null), `schema_version`, `version` (`metadata.version`), `path` (repo-relative, forward slashes), `bytes`, `sha256` of the file's exact bytes, `aliases`, `expertise` and `status`. Entries SHALL be ordered by `id`. Fields that a persona file does not provide, such as `persona.custom_name`, SHALL NOT cause the entry to be omitted.

#### Scenario: Domain and subdomain from path
- **WHEN** a persona file is at `personas/writing/screenplays/dp_persona_schema.json`
- **THEN** its entry has domain `writing` and subdomain `screenplays`

#### Scenario: Hash matches file
- **WHEN** a consumer hashes the file at an entry's `path`
- **THEN** the result equals the entry's `sha256` and the file's size equals `bytes`

#### Scenario: Persona with optional fields missing
- **WHEN** a persona file has `custom_name` null and no `reference_libraries`
- **THEN** its entry exists with the remaining fields populated

### Requirement: Id aliases
Each persona entry's `aliases`, and each team entry's `aliases`, SHALL contain the file-name stem and the stem with trailing version suffix (such as `_v1.1`), then `_schema`, then `_persona` removed one at a time, excluding the entry's own `id`. An alias that maps to more than one persona (or team), or that equals a different persona's (or team's) `id`, SHALL be an error.

#### Scenario: Alias resolves a config id
- **WHEN** `personas/development/context_configuration.json` lists `ott_ux_persona` and the persona file is `ott_ux_persona_schema_v1.1.json` with `persona_name` `ux_designer`
- **THEN** `ott_ux_persona` appears in the `aliases` of the entry whose id is `ux_designer`

#### Scenario: Team alias resolves a config id
- **WHEN** `personas/development/context_configuration.json` lists `react_fullstack_team` and the team file `react_fullstack_team.json` has `team_name` `react_fullstack_development_team`
- **THEN** `react_fullstack_team` appears in the `aliases` of the team entry whose id is `react_fullstack_development_team`

#### Scenario: Ambiguous alias
- **WHEN** two different personas would receive the same alias
- **THEN** generation fails with an error naming the alias and both personas

### Requirement: Team entries
Each team file under a `teams/` directory inside `personas/` SHALL be indexed with: `id` (`team.team_name`), `name` (`team.display_name`), `summary` (`team.description`), `domain`, `members` (the ordered `team.members`), `default_primary`, `aliases`, `path`, `bytes`, `sha256` and `status`. Every member and the `default_primary` SHALL resolve to a persona `id`. A member that does not resolve SHALL be an error.

#### Scenario: Team with all members present
- **WHEN** every member of `retirement_planning_team` has a persona entry
- **THEN** the team entry lists its six members and generation succeeds

#### Scenario: Team with a missing member
- **WHEN** a team lists a member for which no persona file exists
- **THEN** generation fails with an error naming the team and the member

### Requirement: Context configuration references
Generation SHALL read each `context_configuration*.json` file and check its `available_personas`, `always_on_personas`, `default_primary_persona` and `available_teams` against persona ids, aliases and team ids. A reference that resolves only through an alias SHALL produce an informational note. A reference that does not resolve at all SHALL produce a warning. Neither SHALL fail generation or cause any context configuration file to be modified.

#### Scenario: Config id resolves via alias
- **WHEN** `available_personas` contains `design_expert`
- **THEN** generation notes that `design_expert` resolves via alias to `ux_ui_strategist` and succeeds

#### Scenario: Config lists a team that has no file
- **WHEN** `available_teams` contains `security_review_team` and no team file defines it
- **THEN** generation emits a warning naming the config file and the team id and succeeds

### Requirement: Index freshness check
The repository SHALL provide a check mode that regenerates the index in memory, compares it with the committed `index.json`, and exits non-zero without modifying any file when they differ or when generation has errors. A continuous-integration workflow SHALL run this check on pull requests and pushes to the default branch.

#### Scenario: Persona file edited without regenerating
- **WHEN** a persona file changes and `index.json` is not regenerated
- **THEN** the check exits non-zero and says the index is stale

#### Scenario: Clean repository
- **WHEN** `index.json` matches the generated output and there are no errors
- **THEN** the check exits zero

### Requirement: Source files are read-only to generation
Generation and the check mode SHALL NOT modify any persona, team or context configuration file.

#### Scenario: Files unchanged after generation
- **WHEN** generation runs
- **THEN** the only file written is `index.json`
