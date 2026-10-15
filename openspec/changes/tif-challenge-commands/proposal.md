## Why

`/challenge` and `/synthesize` work only inside this repository: they read `config/` files by repo-relative path and take their domain context from a configuration the repository loads. The `tif` plugin installs from a cache copy of `plugin/`, so an installed plugin has neither. Testing showed that without context the challenger is close to a generic chat prompt; with a persona digest it gains moderate breadth; with project facts its required clarifications move from intake questions to decision-level ones. The plugin therefore needs the same layering the framework has (a domain layer and a project layer), with the project layer authored where the user works, not copied from this repository.

## What Changes

- **Project layer**: a project context file `.persona/context.md` in the user's project (goals, what exists and is decided, world and vocabulary, constraints and non-goals; optional `domain` and `focus` fields), created by a new interview command `/tif:context` and editable by hand.
- **Domain layer**: a generated `plugin/framework/domains.json` (domain name → `challenge_focus` and description) built from the domain-level `context_configuration.json` files. A domain is an optional parent of a project, named by the project's `domain` field. It is never inferred from which personas are installed.
- **Deterministic resolution**: a new `tif.py resolve` subcommand reads `.persona/context.md`, the domain table and the installed personas, and prints the resolved lens (with where it came from), the project facts and a persona digest. The commands pass that output on; no model decides the lens.
- **Commands and agents**: `/tif:challenge` and `/tif:synthesize` (with `challenger` and `synthesizer` agents) run the two phases in isolation using the resolved context. The framework files they need ship as a generated `plugin/framework/`.
- **Protocol**: the `domain_context` and `active_personas` inputs are both optional; project facts travel inside `domain_context`.
- The repo-local `.claude/commands/` and `.claude/agents/` stay as they are and remain the source for the generated plugin agents.
- Plugin version becomes 0.2.0.
- **BREAKING (spec only)**: the plugin no longer exposes "exactly one skill"; its identity requirement changes.

## Capabilities

### New Capabilities
- `tif-project-context`: the project context file, the interview command that creates it, the bundled domain table, and the deterministic resolution step.
- `tif-challenge-protocol-bundle`: the plugin ships the challenge/synthesis commands, agents and framework files, generated from repo sources and kept in sync.

### Modified Capabilities
- `tif-plugin-packaging`: the identity requirement allows the commands and agents; the sync requirement extends to the framework bundle.

## Impact

- New: `plugin/commands/` (`challenge.md`, `synthesize.md`, `context.md`), `plugin/agents/`, `plugin/framework/` (generated, including `domains.json`).
- Changed: `scripts/build_persona_index.py` (generate and check the new files), `plugin/scripts/tif.py` (`resolve` subcommand) and its tests, `scripts/test_challenge_agents.py`, `config/challenge_synthesis_protocol.md` (inputs optional), the plugin version, and the README plugin section.
- Depends on the layering rules in `config/framework_configuration_overview.md` (Layer 2), drafted on branch `layering-consistency` (pushed, no PR yet). The domain table is generated from the domain-level configs that rule describes.
- Unchanged: `.claude/commands/`, `.claude/agents/`, the catalog, and every `config/` file except the protocol's input definitions.
- Out of scope: uninstalling personas, generating a project-level JSON config for users, and persona id changes.
- No new dependencies (standard library only).
