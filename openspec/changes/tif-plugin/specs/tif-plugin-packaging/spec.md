## Purpose

Make TIF installable as a Claude Code plugin that is self-contained at runtime and whose bundled catalog and command documentation cannot silently drift from their sources.

## ADDED Requirements

### Requirement: Plugin identity
The plugin SHALL be named `tif` and SHALL expose exactly one skill, `catalog`, invoked as `/tif:catalog`.

#### Scenario: Manifest content
- **WHEN** `plugin/.claude-plugin/plugin.json` is read
- **THEN** it contains the name `tif`, a version, a description, an author and a license

### Requirement: Marketplace entry
The repository SHALL provide `.claude-plugin/marketplace.json` listing the plugin with source `./plugin`.

#### Scenario: Validation
- **WHEN** `claude plugin validate` is run against the repository
- **THEN** it reports no errors

### Requirement: Self-contained runtime
Everything the plugin needs at runtime SHALL live inside `plugin/`, including a generated copy of the catalog at `plugin/catalog/`, because an installed plugin runs from a cache copy of that directory.

#### Scenario: Run from a copy
- **WHEN** the `plugin/` directory is copied elsewhere and `tif.py list` is run from the copy
- **THEN** it succeeds using only files inside the copy

### Requirement: Bundled catalog stays in sync
The generator SHALL emit `plugin/catalog/` from the repository's index, persona files and team files, and its `--check` mode SHALL fail when the bundled copy is missing, has extra files, or differs from the sources.

#### Scenario: Drift detected
- **WHEN** a persona file changes and the bundled copy is not regenerated
- **THEN** `--check` exits nonzero and names the regeneration command

### Requirement: Command documentation stays in sync
The subcommand names, arguments and descriptions SHALL be defined once, and `tif.py --check` SHALL fail when the SKILL.md help block or the README Quick Start block differs from what that definition generates.

#### Scenario: Hand-edited help
- **WHEN** the SKILL.md help block is edited by hand
- **THEN** `tif.py --check` exits nonzero

### Requirement: No hooks and no collaboration-field reading
The plugin SHALL NOT register hooks and SHALL NOT read or act on team collaboration fields.

#### Scenario: Plugin contents
- **WHEN** the plugin directory is inspected
- **THEN** it contains no `hooks/` directory and `tif.py` has no code path that interprets `primary_voice` or `decision_pattern` beyond reporting a missing default primary at install

### Requirement: Standard library only
`tif.py` SHALL require only Python 3 and its standard library.

#### Scenario: Imports
- **WHEN** `tif.py` is inspected
- **THEN** every import is from the standard library
