## Why

`/challenge` and `/synthesize` (with the `challenger` and `synthesizer` subagents) work only inside this repository: they read `config/` files by repo-relative path. The `tif` plugin installs from a cache copy of `plugin/`, so anyone who installs it cannot use the protocol. The protocol is runtime-agnostic and already validated live, so the only gap is packaging.

## What Changes

- Add `plugin/commands/challenge.md` and `plugin/commands/synthesize.md`, invoked as `/tif:challenge` and `/tif:synthesize`.
- Add `plugin/agents/challenger.md` and `plugin/agents/synthesizer.md`, generated from the repo-local agents.
- Bundle the three framework files the agents need (`challenge_phase_prompt.md`, `persona_collaboration_framework_v2.md`, `challenge_synthesis_protocol.md`) as a generated `plugin/framework/`.
- Extend the generator so it writes these copies, and `--check` (run in CI) fails when any is missing, extra or stale. Extend the challenger drift test to cover the plugin copy.
- Domain context becomes an explicit input: `--focus "<text>"` (verbatim; also the manual path) or `--domain <name>` (looked up in a generated `plugin/framework/domains.json` of name → `challenge_focus`), else first-principles. A project-level config with no `challenge_focus` of its own inherits the one from the domain-level config it extends. Inference of an "active domain" from the conversation is dropped from the plugin commands.
- The synthesizer receives the resolved focus value, not a config path.
- The protocol's `domain_context` input changes from required to optional, matching the phase prompt's first-principles fallback and the manual-orchestration requirement (R-2).
- The repo-local `.claude/commands/` and `.claude/agents/` stay exactly as they are and remain the source for the generated plugin copies.
- **BREAKING (spec only)**: the plugin no longer exposes "exactly one skill"; its identity requirement changes.

## Capabilities

### New Capabilities
- `tif-challenge-protocol-bundle`: the plugin ships the challenge/synthesis commands, agents and framework files, generated from repo sources and kept in sync.

### Modified Capabilities
- `tif-plugin-packaging`: the plugin identity requirement (currently "exactly one skill, `catalog`") must allow the two commands and two agents; the self-contained-runtime and sync requirements extend to the framework bundle.

## Impact

- New: `plugin/commands/`, `plugin/agents/`, `plugin/framework/` (generated, except the two commands, which are hand-written).
- Changed: `scripts/build_persona_index.py` (generate and check the new files, including `domains.json`), `config/challenge_synthesis_protocol.md` (`domain_context` optional), `scripts/test_challenge_agents.py`, `.github/workflows/persona-index.yml` only if a new step is needed, the plugin version in `plugin.json`, and the README plugin section.
- Unchanged: `.claude/commands/`, `.claude/agents/`, the catalog, and every `config/` file except the protocol's input definition.
- No new dependencies (standard library only).
