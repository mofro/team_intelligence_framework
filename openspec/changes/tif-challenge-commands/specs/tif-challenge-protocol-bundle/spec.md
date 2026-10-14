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
Each command SHALL run its phase in its own subagent (`challenger` for Phase 1, `synthesizer` for Phase 2), and SHALL pass the subagent only the inputs the protocol defines for that phase: for Phase 1 the request and the `challenge_focus`; for Phase 2 the request, the verbatim Challenge Artifact and the resolved lens. The subagents SHALL be limited to the read-only file tool.

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

### Requirement: Explicit domain context
Each command SHALL take the domain lens as an explicit input and SHALL NOT infer an active domain from the conversation. The lens SHALL be resolved in this order: a `--focus` value, used verbatim; else a `--domain` name looked up in the plugin's bundled domain table; else the first-principles lens "correctness, completeness, and coherence". The resolved lens and how it was resolved SHALL appear in the output. An unknown `--domain` name SHALL be an error that lists the known names and SHALL NOT fall back silently.

#### Scenario: Manual focus
- **WHEN** `/tif:challenge --focus "narrative consistency" <request>` is run
- **THEN** the challenger receives that text verbatim as its `challenge_focus`

#### Scenario: Named domain
- **WHEN** `/tif:challenge --domain development <request>` is run
- **THEN** the challenger receives the `challenge_focus` recorded for `development` in the bundled table

#### Scenario: No context given
- **WHEN** `/tif:challenge <request>` is run with neither flag
- **THEN** the first-principles lens is used and the output says so

#### Scenario: Unknown domain
- **WHEN** `--domain nonsense` is given
- **THEN** the command fails and lists the known domain names

### Requirement: Domain table
The plugin SHALL bundle a generated table mapping each domain and project name to its `challenge_focus`. A project-level configuration that declares no `challenge_focus` of its own SHALL take the value from the domain-level configuration it extends, which is the configuration in the nearest enclosing `personas/` directory. A project-level configuration that declares its own value SHALL keep it. A name that would map to two configurations SHALL be a generation error.

#### Scenario: Project inherits
- **WHEN** `--domain hero_heaven` is used and the Hero Heaven configuration has no `challenge_focus`
- **THEN** the lens is the `gaming` domain's `challenge_focus`

#### Scenario: Project overrides
- **WHEN** a project-level configuration declares its own `challenge_focus`
- **THEN** that value is recorded for that project name

### Requirement: Synthesis input
`/tif:synthesize` SHALL take the same `--focus` and `--domain` inputs, SHALL pass the synthesizer the resolved lens in place of a configuration path, and the synthesizer SHALL state which lens it used.

#### Scenario: Synthesis without a domain
- **WHEN** `/tif:synthesize` is run with neither flag
- **THEN** it returns a synthesis that traces every `RC-n` and `AF-n` and states that the first-principles lens was used

### Requirement: Repo-local commands unchanged
The repository's own `/challenge` and `/synthesize` commands and the `challenger` and `synthesizer` agents under `.claude/` SHALL continue to work as before, and SHALL be the source from which the plugin's agent bodies are generated.

#### Scenario: Plugin copy matches its source
- **WHEN** the body of `plugin/agents/challenger.md` is compared with `.claude/agents/challenger.md`
- **THEN** they are identical except for the documented framework path substitution
