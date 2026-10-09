## Purpose

Defines what a consumer such as persona-conductor-proto can rely on from this repository to select personas or whole teams and fetch only those files, so users no longer copy files from a downloaded copy of the repo.

## ADDED Requirements

### Requirement: Retrieval entry point
The repository SHALL publish its catalog as `index.json` at the repository root, readable by a plain HTTP fetch of the file at any git tag, branch or commit. Every entry's `path` SHALL be relative to the repository root so the file can be fetched at the same ref as the index.

#### Scenario: Fetch a persona at the index's ref
- **WHEN** a consumer fetches `index.json` at ref `v0.2` and then fetches an entry's `path` at ref `v0.2`
- **THEN** the file exists and its sha256 equals the entry's `sha256`

### Requirement: Select by persona
Each persona SHALL be selectable from the index by its `id` or by any value in its `aliases`, and the entry SHALL give everything needed to fetch exactly that persona's file.

#### Scenario: Select by canonical id
- **WHEN** a consumer looks up `tax_strategist`
- **THEN** it finds one entry whose `path` is `personas/financial/tax_strategist_schema.json`

#### Scenario: Select by legacy id
- **WHEN** a consumer looks up `design_expert`
- **THEN** it finds the entry whose `id` is `ux_ui_strategist`

#### Scenario: Unknown id
- **WHEN** a consumer looks up a value that is neither an `id` nor an alias
- **THEN** no entry matches

### Requirement: Select by team
Each team SHALL be selectable from the index by its `id` or any value in its `aliases`, and its entry SHALL list its `members` by persona `id` and give the team file's `path`, so a consumer can resolve a team to the team file plus its member persona files.

#### Scenario: Team bundle
- **WHEN** a consumer looks up `retirement_planning_team`
- **THEN** the entry gives the team file path and six member ids, each of which matches a persona entry

#### Scenario: Team looked up by legacy id
- **WHEN** a consumer looks up `react_fullstack_team`
- **THEN** it finds the entry whose `id` is `react_fullstack_development_team`

#### Scenario: Team with stub members
- **WHEN** a consumer looks up `intelligence_framework_team`
- **THEN** its entry has status `contains_stubs` and each stub member's persona entry has status `stub`
