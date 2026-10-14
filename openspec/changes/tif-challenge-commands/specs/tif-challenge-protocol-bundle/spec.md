## Purpose

Lets anyone who installs the `tif` plugin run the two-phase challenge/synthesis protocol, with each phase isolated from the other, without needing a checkout of this repository.

## ADDED Requirements

### Requirement: Challenge and synthesis commands
The plugin SHALL provide the commands `/tif:challenge` and `/tif:synthesize`. `/tif:challenge` SHALL run Phase 1 only and return a Challenge Artifact. `/tif:synthesize` SHALL run Phase 2 only and consume a Challenge Artifact together with the original request.

#### Scenario: Commands are listed after install
- **WHEN** the plugin is installed
- **THEN** `/tif:challenge` and `/tif:synthesize` are available

#### Scenario: Challenge does not synthesize
- **WHEN** `/tif:challenge` is run with a request
- **THEN** the output is a Challenge Artifact and contains no synthesized answer

### Requirement: Phase isolation
Each command SHALL run its phase in its own subagent (`challenger` for Phase 1, `synthesizer` for Phase 2), and SHALL pass the subagent only the inputs the protocol defines for that phase: for Phase 1 the request and the `challenge_focus`; for Phase 2 the request, the verbatim Challenge Artifact and, when one exists, the domain configuration path. The subagents SHALL be limited to the read-only file tool.

#### Scenario: Challenger sees no conversation
- **WHEN** `/tif:challenge` is run after a long conversation
- **THEN** the `challenger` subagent receives only the `challenge_focus` and the request

#### Scenario: Subagents cannot modify anything
- **WHEN** either subagent's tool list is inspected
- **THEN** it contains the read tool only

### Requirement: Framework files resolve inside the plugin
The subagents SHALL read the framework files they need (the Phase 1 prompt, the collaboration framework and the protocol) from a copy inside the plugin, not from the user's project, and the commands SHALL tell the subagents where that copy is.

#### Scenario: Installed in an unrelated project
- **WHEN** `/tif:synthesize` is run in a project that contains no `config/` directory
- **THEN** the synthesizer finds the framework files and completes

### Requirement: No domain configuration is required
When no domain `context_configuration.json` path is supplied, the commands SHALL use "first principles: correctness, completeness, and coherence" as the `challenge_focus`, and the synthesizer SHALL proceed without a domain configuration and SHALL state in its output that it did.

#### Scenario: Synthesis without a domain
- **WHEN** `/tif:synthesize` is run with no domain configuration path
- **THEN** it returns a synthesis that traces every `RC-n` and `AF-n` and notes that no domain configuration was used

### Requirement: Repo-local commands unchanged
The repository's own `/challenge` and `/synthesize` commands and the `challenger` and `synthesizer` agents under `.claude/` SHALL continue to work as before, and SHALL be the source from which the plugin's agent bodies are generated.

#### Scenario: Plugin copy matches its source
- **WHEN** the body of `plugin/agents/challenger.md` is compared with `.claude/agents/challenger.md`
- **THEN** they are identical except for the documented framework path substitution
