## Purpose

Gives every persona that a team names but nobody has yet written a real file: a minimal valid placeholder that is visible in the index and prompts the user to complete it when invoked, so improvised roles do not stay undocumented.

## ADDED Requirements

### Requirement: Stub personas for missing team members
For each persona id listed as a member of a team in the repository that has no persona file, the repository SHALL contain a stub persona file. At the time of this change those ids are `system_architect`, `data_scientist`, `backend_developer` and `product_manager`, all members of `intelligence_framework_team`.

#### Scenario: Team resolves fully
- **WHEN** the index is generated after the stubs are added
- **THEN** no member of `intelligence_framework_team` is reported as unresolved

### Requirement: Stub files conform to the current persona schema
A stub SHALL contain every top-level key and every `persona` key that existing 1.2 persona files provide, with `schema_version` "1.2", a populated `role`, `expertise` and `approach` seeded from what the team file already states about that role, and a `custom_name` of null. A stub SHALL be loadable by the existing framework with no changes to the framework.

#### Scenario: Stub loads like any other persona
- **WHEN** a stub is added to a session using the same procedure as any other persona file
- **THEN** it activates and can be addressed by its `persona_name` using the `@persona_name` convention

#### Scenario: Stub seeded from team context
- **WHEN** the `data_scientist` stub is created
- **THEN** its role and approach reflect the team file's statement that the data scientist provides model evaluation and performance insights

### Requirement: Stub marking
A stub SHALL carry the optional top-level key `"stub": true` and SHALL state in its `metadata.description` that it is a stub. A persona file without the key SHALL be treated as complete. The index SHALL set a persona entry's `status` to `"stub"` for a file with `"stub": true` and `"complete"` otherwise, and a team entry's `status` to `"contains_stubs"` when any member is a stub and `"complete"` otherwise.

#### Scenario: Index reflects stub status
- **WHEN** the index is generated
- **THEN** the four stub personas have status `stub`, every other persona has status `complete`, and `intelligence_framework_team` has status `contains_stubs`

#### Scenario: Completing a stub
- **WHEN** a stub file is edited to remove `"stub": true`
- **THEN** after regeneration its index status is `complete`

### Requirement: Stub prompts for completion on invocation
A stub's `behavioral_rules` SHALL include a rule instructing the persona, the first time it is invoked in a session, to tell the user plainly that it is a placeholder with limited defined expertise, and to offer to help flesh out the persona definition from the work being done. The rule SHALL NOT prevent the persona from helping with the task.

#### Scenario: First invocation of a stub
- **WHEN** a user addresses `@backend_developer` for the first time in a session
- **THEN** the response includes a notice that the persona is a stub and an offer to define it, and also helps with the request

#### Scenario: Later invocation in the same session
- **WHEN** the same stub is addressed again in that session
- **THEN** the notice is not repeated

### Requirement: Stub location and naming
Stub files SHALL be placed under `personas/` in the domain directory of the team that references them, and named `<persona_name>_persona_schema.json`.

#### Scenario: File placement
- **WHEN** the `product_manager` stub is created for `intelligence_framework_team` in `personas/ai_development/teams/`
- **THEN** the file is `personas/ai_development/product_manager_persona_schema.json`
