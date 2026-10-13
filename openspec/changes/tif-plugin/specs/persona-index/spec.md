## MODIFIED Requirements

### Requirement: Source files are read-only to generation
Generation and the check mode SHALL NOT modify any persona, team or context configuration file. Generation SHALL write only its own generated outputs, which are `index.json` and the bundled catalog under `plugin/catalog/`. The check mode SHALL NOT write any file.

#### Scenario: Files unchanged after generation
- **WHEN** generation runs
- **THEN** every persona, team and context configuration file is byte-identical to its state before the run, and the only paths written are `index.json` and files under `plugin/catalog/`

#### Scenario: Check mode writes nothing
- **WHEN** the check mode runs
- **THEN** no file in the repository is created, modified or deleted
