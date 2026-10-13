## Purpose

Let a user discover what TIF offers through deterministic, read-only subcommands answered from the bundled catalog index, without the model reading the catalog.

## ADDED Requirements

### Requirement: Help lists every subcommand
The `help` subcommand and the `--help` flag SHALL print the same text, listing each subcommand with its arguments and a one-line description, generated from a single command table.

#### Scenario: Help and flag agree
- **WHEN** a user runs `help` and then `--help`
- **THEN** both print identical text containing `help`, `list`, `teams`, `info` and `install`

### Requirement: List personas
The `list` subcommand SHALL print one line per persona from the bundled index, showing id, role, domain and status, and SHALL accept `--domain` to filter by domain.

#### Scenario: Unfiltered list
- **WHEN** a user runs `list`
- **THEN** every persona in the bundled index appears exactly once, and stub personas are marked as stubs

#### Scenario: Domain filter
- **WHEN** a user runs `list --domain` with a domain present in the index
- **THEN** only personas in that domain appear

#### Scenario: Unknown domain
- **WHEN** a user runs `list --domain` with a domain not in the index
- **THEN** the output states that nothing matched and lists the available domains, and the exit status is nonzero

### Requirement: List teams
The `teams` subcommand SHALL print one line per team from the bundled index, showing id, member count and status (`complete`, `contains_stubs` or `incomplete`).

#### Scenario: Teams with differing status
- **WHEN** a user runs `teams`
- **THEN** each team appears once with its status, including any team whose status is `contains_stubs`

### Requirement: Show details for one item
The `info` subcommand SHALL accept an id or an alias and print that item's summary, role, domain, version, status and, for teams, members and default primary.

#### Scenario: Lookup by alias
- **WHEN** a user runs `info` with an alias that maps to exactly one item
- **THEN** that item's details are printed

#### Scenario: Ambiguous alias
- **WHEN** a user runs `info` with an alias that maps to more than one item
- **THEN** the output lists the candidate ids and asks for one, and the exit status is nonzero

#### Scenario: Unknown name
- **WHEN** a user runs `info` with a name that matches no id or alias
- **THEN** the output says so and the exit status is nonzero

### Requirement: Browse needs no network and no model reading
The browse subcommands SHALL read only the bundled `plugin/catalog/index.json`, SHALL NOT make network requests, and SHALL produce the same output for the same catalog.

#### Scenario: Offline use
- **WHEN** a browse subcommand is run with no network access
- **THEN** it succeeds with normal output
