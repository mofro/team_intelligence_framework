# tif-catalog-install Specification

## Purpose
Copy personas and teams from the bundled catalog into a user's project safely and predictably, telling the user what they are getting without ever blocking them.

## Requirements

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

### Requirement: Update differing files
Install SHALL replace an existing destination file whose content differs from the catalog and SHALL report it as updated, because a differing file is as likely to be an older catalog version as a local change. An identical existing file SHALL be reported as already installed. Install SHALL take no `--force` option.

#### Scenario: Older or changed persona
- **WHEN** the destination file exists with different content
- **THEN** the file is replaced with the catalog version and the output says it was updated

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

### Requirement: State what installed team files do
After installing a team, the output SHALL state that Conductor currently ignores team files.

#### Scenario: Team install note
- **WHEN** a team install finishes
- **THEN** the output includes a one-line note that team files are stored for later use and not yet read by Conductor

### Requirement: Unknown names
Install SHALL fail with a nonzero status and write nothing when the name matches no catalog item, and SHALL treat an ambiguous alias as an error that lists candidates. A virtual team (a team named in a `context_configuration*.json` `available_teams` list with no team file, such as `security_review_team`) has no catalog entry and no member list, so it is an unknown name here; installing virtual teams is out of scope.

#### Scenario: Unknown name
- **WHEN** a user runs `install` with a name that matches nothing
- **THEN** no files are written and the exit status is nonzero

#### Scenario: Virtual team name
- **WHEN** a user runs `install` with the name of a virtual team such as `security_review_team`
- **THEN** it is reported as unknown, no files are written and the exit status is nonzero

### Requirement: Uninstall targets
The `uninstall` subcommand SHALL delete the installed file for a persona from `.persona/personas/`, or for a team the team file from `.persona/teams/` together with each member persona that no other installed team lists, and SHALL record and read no state beyond those files and the bundled index.

#### Scenario: Uninstall a persona
- **WHEN** a user runs `uninstall` with the id of an installed persona
- **THEN** that persona's file no longer exists under `.persona/personas/` and the output names the path

#### Scenario: Uninstall a team
- **WHEN** a user runs `uninstall` with the id of an installed team
- **THEN** the team file no longer exists under `.persona/teams/` and each member persona that no other installed team lists is removed

#### Scenario: Shared member
- **WHEN** a team is uninstalled and a member is also listed by another installed team
- **THEN** that member's file is kept and the output names the other team

#### Scenario: Team not installed
- **WHEN** a team is uninstalled but its team file is absent
- **THEN** no persona file is removed

#### Scenario: Last team removed
- **WHEN** the last installed team that lists a persona is uninstalled
- **THEN** that persona is removed with it

### Requirement: Uninstall does not compare against the catalog
Uninstall SHALL delete an installed file whether or not its content matches the bundled catalog, because a differing file is as likely to be an older catalog version or a copy changed elsewhere as a local edit, and the user asked for its removal.

#### Scenario: File differs from the catalog
- **WHEN** an installed persona's content differs from the bundled catalog
- **THEN** uninstall deletes it

### Requirement: Uninstall is idempotent
Uninstalling something that is not installed SHALL report that it is not installed, change nothing and exit with status 0.

#### Scenario: Repeat uninstall
- **WHEN** uninstall is run twice for the same name
- **THEN** the second run reports not installed, changes nothing and exits 0

### Requirement: Report what remains
After removing a persona, uninstall SHALL name each installed team that lists it. After removing a team, uninstall SHALL name each member kept because another installed team lists it, together with that team. Neither report SHALL block or undo the removal.

#### Scenario: Persona used by a team
- **WHEN** a persona that an installed team lists is uninstalled
- **THEN** the persona is removed and the output names that team

#### Scenario: Shared members named
- **WHEN** a team is uninstalled while another installed team lists one of its members
- **THEN** that member is reported as kept, with the other team named

### Requirement: Unknown names on uninstall
Uninstall SHALL fail with a nonzero status and delete nothing when the name matches no catalog item, SHALL treat an ambiguous alias as an error listing candidates, and SHALL treat a virtual team name as unknown.

#### Scenario: Unknown name
- **WHEN** a user runs `uninstall` with a name that matches nothing
- **THEN** no files are deleted and the exit status is nonzero
