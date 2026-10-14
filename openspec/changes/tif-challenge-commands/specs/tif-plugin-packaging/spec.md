## MODIFIED Requirements

### Requirement: Plugin identity
The plugin SHALL be named `tif`. It SHALL expose the skill `catalog` (invoked as `/tif:catalog`), the commands `challenge` and `synthesize` (invoked as `/tif:challenge` and `/tif:synthesize`), and the agents `challenger` and `synthesizer`, and nothing else.

#### Scenario: Manifest content
- **WHEN** `plugin/.claude-plugin/plugin.json` is read
- **THEN** it contains the name `tif`, a version, a description, an author and a license

#### Scenario: Exposed surface
- **WHEN** the plugin directory is inspected
- **THEN** it contains one skill, two commands and two agents, and no other skills, commands or agents

## ADDED Requirements

### Requirement: Bundled framework files stay in sync
The generator SHALL emit `plugin/framework/` (a copy of the three framework files the challenge agents read, and the domain table `domains.json`) and the plugin's agent files from their repository sources, and its `--check` mode SHALL fail when any of them is missing, has extra files, or differs from what the sources produce.

#### Scenario: Phase prompt edited without regenerating
- **WHEN** `config/challenge_phase_prompt.md` changes and the plugin copies are not regenerated
- **THEN** `--check` exits nonzero and names the regeneration command

#### Scenario: Plugin agent hand-edited
- **WHEN** `plugin/agents/challenger.md` is edited by hand
- **THEN** `--check` exits nonzero
