## Purpose

Lets anyone who installs the `tif` plugin run the two-phase challenge/synthesis protocol, with each phase isolated from the other and fed by the resolved project context, without needing a checkout of this repository.

## ADDED Requirements

### Requirement: Challenge and synthesis commands
The plugin SHALL provide the commands `/tif:challenge` and `/tif:synthesize`. `/tif:challenge` SHALL run Phase 1 only and return a Challenge Artifact. `/tif:synthesize` SHALL run Phase 2 only and consume a Challenge Artifact together with the original request. Both SHALL obtain their context by running `tif.py resolve` and SHALL show the lens and its source in the output.

#### Scenario: Commands are listed after install
- **WHEN** the plugin is installed
- **THEN** `/tif:challenge` and `/tif:synthesize` are available

#### Scenario: Challenge does not synthesize
- **WHEN** `/tif:challenge` is run with a request
- **THEN** the output is a Challenge Artifact and contains no synthesized answer

### Requirement: Phase isolation
Each command SHALL run its phase in its own subagent (`challenger` for Phase 1, `synthesizer` for Phase 2). The challenger SHALL receive only the request, `domain_context` (lens plus project facts) and `active_personas` (the digest). The synthesizer SHALL receive those three, the verbatim Challenge Artifact and the framework directory. The subagents SHALL be limited to the read-only file tool.

#### Scenario: Challenger sees no conversation
- **WHEN** `/tif:challenge` is run after a long conversation
- **THEN** the `challenger` subagent receives only the request, `domain_context` and `active_personas`

#### Scenario: Subagents cannot modify anything
- **WHEN** either subagent's tool list is inspected
- **THEN** it contains the read tool only

### Requirement: Context is optional
Both commands SHALL work with no project context file and no installed personas, using the first-principles lens, and the protocol SHALL define `domain_context` and `active_personas` as optional inputs.

#### Scenario: Bare run
- **WHEN** `/tif:challenge <request>` is run in a project with neither context nor personas
- **THEN** a Challenge Artifact is returned and states that the first-principles lens was used

### Requirement: Framework files resolve inside the plugin
The synthesizer SHALL read the collaboration framework and the protocol from a copy inside the plugin, not from the user's project, and `/tif:synthesize` SHALL pass it the location of that copy.

#### Scenario: Installed in an unrelated project
- **WHEN** `/tif:synthesize` is run in a project that contains no `config/` directory
- **THEN** the synthesizer finds the framework files and completes

### Requirement: Synthesis traceability
The synthesizer SHALL trace every `RC-n` and `AF-n` of the Challenge Artifact and SHALL state which lens and whether project context was used.

#### Scenario: Synthesis without context
- **WHEN** `/tif:synthesize` is run with no context file
- **THEN** it traces every `RC-n` and `AF-n` and states that the first-principles lens was used

### Requirement: Repo-local commands unchanged
The repository's own `/challenge` and `/synthesize` commands and the `challenger` and `synthesizer` agents under `.claude/` SHALL continue to work as before, and the plugin's challenger body SHALL be generated from the same source.

#### Scenario: Plugin copy matches its source
- **WHEN** the body of `plugin/agents/challenger.md` is compared with `.claude/agents/challenger.md`
- **THEN** they are identical except for the documented framework path substitution
