## Purpose

Gives the installed `tif` plugin a project layer (what this body of work is, what exists, what is decided) authored in the user's own project, and an optional bundled domain layer, resolved deterministically before any challenge runs.

## ADDED Requirements

### Requirement: Project context file
A project's context SHALL live in `.persona/context.md` in the user's project. It SHALL be plain markdown with an optional front matter holding `domain` and `focus`, and the headings Goal, Current state and decisions, World and vocabulary, and Constraints and non-goals. The plugin SHALL NOT require the file to exist.

#### Scenario: File absent
- **WHEN** `resolve` is run in a project with no `.persona/context.md`
- **THEN** it reports that no project context was found and continues with the remaining sources

#### Scenario: Hand edited
- **WHEN** the user edits the file by hand
- **THEN** the next `resolve` uses the edited text

### Requirement: Interview command
`/tif:context` SHALL create the project context file by interviewing the user in short rounds (goal; what exists and is decided; vocabulary and world facts; constraints and non-goals), SHALL propose a domain from the bundled table (with "none" allowed), SHALL show the drafted file, and SHALL write it only after the user confirms. It SHALL record only what the user stated. If the file exists, it SHALL propose changes to it and SHALL NOT overwrite it without confirmation.

#### Scenario: New file
- **WHEN** `/tif:context` completes and the user confirms the draft
- **THEN** `.persona/context.md` contains the confirmed text and no other file is written

#### Scenario: Declined draft
- **WHEN** the user declines the draft
- **THEN** no file is written

#### Scenario: Existing file
- **WHEN** `/tif:context` is run and `.persona/context.md` exists
- **THEN** it shows proposed edits and leaves the file unchanged until confirmed

### Requirement: Domain table
The plugin SHALL bundle a generated `plugin/framework/domains.json` mapping each domain name to its description and, where declared, its `challenge_focus`, built from the domain-level `context_configuration.json` files. A domain without a `challenge_focus` SHALL be listed without one. Duplicate domain names SHALL be a generation error. A domain SHALL be selected only by name (the context file's `domain` or `--domain`) and SHALL NOT be inferred from installed personas.

#### Scenario: Table matches sources
- **WHEN** a domain-level configuration changes and the plugin is not regenerated
- **THEN** the generator's `--check` fails

### Requirement: Deterministic resolution
`tif.py resolve [--focus F] [--domain D]` SHALL print the lens and its source, the project facts, and a digest of the installed personas (id, role, expertise). The lens SHALL come from the first source that has a value, in this order: `--focus`, the context file's `focus`, `--domain`, the context file's `domain`, then the first-principles lens "correctness, completeness, and coherence". Sources SHALL NOT be combined. An unknown domain name SHALL be an error listing the known names. A missing context file, a domain without a `challenge_focus`, or an empty persona directory SHALL be reported and SHALL NOT be an error.

#### Scenario: Focus overrides everything
- **WHEN** `--focus X` is given and the context file declares a `focus` and a `domain`
- **THEN** the lens is `X` and its source is `--focus`

#### Scenario: Domain from context file
- **WHEN** the context file declares `domain: gaming` and no flag is given
- **THEN** the lens is the `challenge_focus` of `gaming` and its source names the context file

#### Scenario: Domain without a focus
- **WHEN** the selected domain has no `challenge_focus`
- **THEN** resolution reports that and falls to the next source

#### Scenario: Unknown domain
- **WHEN** `--domain nonsense` is given
- **THEN** it exits nonzero and lists the known domain names

#### Scenario: Nothing available
- **WHEN** there is no flag, no context file and no personas
- **THEN** the lens is the first-principles lens and the output says no context or personas were found
