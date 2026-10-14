## Why

`/challenge` and `/synthesize` (with the `challenger` and `synthesizer` subagents) work only inside this repository: they read `config/` files by repo-relative path. The `tif` plugin installs from a cache copy of `plugin/`, so anyone who installs it cannot use the protocol. The protocol is runtime-agnostic and already validated live, so the only gap is packaging.

## What Changes

- Add `plugin/commands/challenge.md` and `plugin/commands/synthesize.md`, invoked as `/tif:challenge` and `/tif:synthesize`.
- Add `plugin/agents/challenger.md` and `plugin/agents/synthesizer.md`, generated from the repo-local agents.
- Bundle the three framework files the agents need (`challenge_phase_prompt.md`, `persona_collaboration_framework_v2.md`, `challenge_synthesis_protocol.md`) as a generated `plugin/framework/`.
- Extend the generator so it writes these copies, and `--check` (run in CI) fails when any is missing, extra or stale. Extend the challenger drift test to cover the plugin copy.
- The synthesizer falls back to first-principles synthesis when no domain `context_configuration.json` path is given, because an installed plugin may have no domain config.
- The repo-local `.claude/commands/` and `.claude/agents/` stay exactly as they are and remain the source for the generated plugin copies.
- **BREAKING (spec only)**: the plugin no longer exposes "exactly one skill"; its identity requirement changes.

## Capabilities

### New Capabilities
- `tif-challenge-protocol-bundle`: the plugin ships the challenge/synthesis commands, agents and framework files, generated from repo sources and kept in sync.

### Modified Capabilities
- `tif-plugin-packaging`: the plugin identity requirement (currently "exactly one skill, `catalog`") must allow the two commands and two agents; the self-contained-runtime and sync requirements extend to the framework bundle.

## Impact

- New: `plugin/commands/`, `plugin/agents/`, `plugin/framework/` (all generated except the commands, which are derived from the repo-local ones).
- Changed: `scripts/build_persona_index.py` (generate and check the new files), `scripts/test_challenge_agents.py`, `.github/workflows/persona-index.yml` only if a new step is needed, the plugin version in `plugin.json`, and the README plugin section.
- Unchanged: `.claude/commands/`, `.claude/agents/`, `config/*`, the catalog.
- No new dependencies (standard library only).
