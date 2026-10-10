## Purpose

Copy personas and teams from the bundled catalog into a user's project safely and predictably, telling the user what they are getting without ever blocking them.

## ADDED Requirements

### Requirement: Install targets
The `install` subcommand SHALL copy a persona into `.persona/personas/` and a team into `.persona/teams/` under the current project, creating directories as needed.

#### Scenario: Install a persona
- **WHEN** a user runs `install` with a persona id
- **THEN** that persona's file exists under `.persona/personas/` and the output names the path

#### Scenario: Install a team
- **WHEN** a user runs `install` with a team id
- **THEN** the team file exists under `.persona/teams/` and each member persona that exists in the catalog exists under `.persona/personas/`

### Requirement: Verify before copying
Install SHALL compare each source file's sha256 with the value in the bundled index before copying and SHALL NOT copy a file that does not match.

#### Scenario: Corrupted bundled file
- **WHEN** a bundled file's hash differs from the index
- **THEN** that file is not copied, the output names it, and the exit status is nonzero

### Requirement: Protect local edits
Install SHALL NOT overwrite an existing destination file whose content differs from the catalog unless `--force` is given. An identical existing file SHALL be reported as already installed.

#### Scenario: Locally edited persona
- **WHEN** the destination file exists with different content and `--force` is absent
- **THEN** the file is left unchanged and the output says it was skipped and how to override

#### Scenario: Forced overwrite
- **WHEN** the destination file exists with different content and `--force` is given
- **THEN** the file is replaced with the catalog version

#### Scenario: Repeat install
- **WHEN** install is run twice with no local changes
- **THEN** the second run reports everything already installed and changes nothing

### Requirement: Warn about stubs without refusing
Install SHALL proceed when the item or any team member is a stub, and SHALL print the number of stubs and their names.

#### Scenario: Team containing stubs
- **WHEN** a user installs a team whose status is `contains_stubs`
- **THEN** the install completes and the output states how many stub personas were installed and names each

### Requirement: Warn about missing members without refusing
Install SHALL proceed when a team lists members that have no catalog file, and SHALL name each missing member.

#### Scenario: Incomplete team
- **WHEN** a user installs a team whose status is `incomplete`
- **THEN** the available files are installed and each unresolved member is named in a warning

### Requirement: Call out a missing primary voice
When a team's default primary voice is missing from the catalog, install SHALL print a prominent warning that is visually distinct from other warnings and SHALL still complete.

#### Scenario: Primary voice missing
- **WHEN** a user installs a team whose default primary is not in the catalog
- **THEN** the output contains a distinct primary-voice warning and the install completes

### Requirement: Virtual teams
Install SHALL handle a team that has no file by design by installing its member personas only and stating that no team file exists.

#### Scenario: Virtual team
- **WHEN** a user installs a virtual team
- **THEN** its members are installed, no file is written under `.persona/teams/`, and the output says why

### Requirement: State what installed team files do
After installing a team, the output SHALL state that Conductor currently ignores team files.

#### Scenario: Team install note
- **WHEN** a team install finishes
- **THEN** the output includes a one-line note that team files are stored for later use and not yet read by Conductor

### Requirement: Unknown names
Install SHALL fail with a nonzero status and write nothing when the name matches no catalog item, and SHALL treat an ambiguous alias as an error that lists candidates.

#### Scenario: Unknown name
- **WHEN** a user runs `install` with a name that matches nothing
- **THEN** no files are written and the exit status is nonzero
