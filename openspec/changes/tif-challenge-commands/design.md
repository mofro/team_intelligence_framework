## Context

See proposal.md for motivation. Current state:

- The repo-local commands delegate to subagents (`.claude/agents/challenger.md`, `synthesizer.md`). The challenger body is a verbatim copy of `config/challenge_phase_prompt.md`, held in sync by `scripts/test_challenge_agents.py`. The synthesizer reads `config/persona_collaboration_framework_v2.md`, the protocol's Phase 2 section and a domain config path by repo-relative path.
- The plugin bundles a generated catalog; `scripts/build_persona_index.py` writes it and `--check` (CI) fails on drift.
- In the framework, Layer 2 has a domain level (`personas/<domain>/context_configuration.json`) and an optional project level that extends it. A domain is an affinity group, not a boundary on personas or teams. Nothing merges them in code; the model reads prose.
- Experiments (headless `claude -p`): no context ≈ generic; persona digest adds moderate breadth; project facts add the most and move required clarifications to decision level.
- Verified on the CLI: `${CLAUDE_PLUGIN_ROOT}` substitution in command and agent bodies. Verified on the desktop app (2026-10-14): `/tif:catalog` runs `tif.py` from the plugin cache and installs into the project. UNVERIFIED: a subagent's Read of files in the plugin cache on the desktop app.

## Goals / Non-Goals

**Goals:**
- An installed plugin runs both phases with real context, with no checkout of this repository.
- The project layer is created where the user works and grown by the user; the domain layer ships with the plugin.
- Lens and context are resolved deterministically and shown, never guessed.
- One source of truth per file; plugin copies are generated and drift fails CI.

**Non-Goals:**
- No change to the protocol's phases or the phase prompt.
- No project-level JSON configuration for users (the project file is prose).
- No uninstall, persona id change or Conductor integration.

## Decisions

1. **The project layer is `.persona/context.md`.** Markdown with an optional front matter (`domain`, `focus`) and fixed headings (Goal, Current state and decisions, World and vocabulary, Constraints and non-goals). Project facts are prose, which the framework's JSON schema has no field for; markdown stays editable by hand. Alternative: a JSON project config mirroring `context_configuration_<project>.json`. Rejected: its fields are routing and behavior settings, not facts, and the facts are what produced the gain.
2. **`/tif:context` is an interview, not a template.** It asks in short rounds (goal, what exists and is decided, vocabulary and world facts, constraints and non-goals), then proposes a domain from the bundled table (suggested from the `reference_context` of installed personas, user decides, "none" allowed), shows the drafted file and writes it only after a yes. If the file exists it proposes edits and never overwrites silently. It records only what the user said; it does not invent facts. Alternatives: a blank template (blank-page problem), capture from sessions (later).
3. **The domain layer is `plugin/framework/domains.json`, generated** from the domain-level configs: name → `challenge_focus` and description. A domain without a `challenge_focus` is listed without one. The table is a snapshot shipped with the plugin version. A domain is chosen by the project's `domain` field (or `--domain`), never by which personas are installed; installed personas' `reference_context` is used only to suggest a value during the interview.
4. **Resolution is a script.** `tif.py resolve [--focus F] [--domain D]` prints, in order: the lens and its source, the project facts, and the persona digest (id, role, expertise for each installed persona). Lens precedence is an entry-level replace: `--focus` over the context file's `focus` over `--domain` over the context file's `domain` over first-principles. The first source that has a value wins and nothing is combined, which is the framework's merge rule applied to a single entry. An unknown domain name is an error that lists the known names; a missing or empty context file or an empty persona directory is reported, not an error. Alternative: let the command or model compose the lens. Rejected: that is the guessing the repo-local command already does.
5. **Inputs map onto the protocol without new fields.** `domain_context` carries the resolved lens plus the project facts; `active_personas` carries the digest. Both are optional in the protocol, so with neither the first-principles lens is used and the output says so. Phase 1 receives only: the request, `domain_context` and `active_personas`. The challenger reads no files.
6. **The synthesizer receives the same three inputs plus the Challenge Artifact and `framework_dir`.** The command computes `${CLAUDE_PLUGIN_ROOT}/framework` and passes it, so the synthesizer reads the collaboration framework and the Phase 2 protocol from there. This does not depend on agent-body path substitution.
7. **Generate, do not hand-copy.** The generator that writes `plugin/catalog/` also writes `plugin/framework/` and `plugin/agents/`; `--check` compares them. Commands are hand-written plugin files, kept aligned with the repo-local ones by a drift test (same subagent names, same pass-only-these-inputs rule).
8. **Plugin version 0.2.0.** The surface grows, and the plugin cache is keyed by version, so an unchanged version could leave an installed copy stale (UNVERIFIED, not tested).
9. **`domain_context` and `active_personas` become optional in the protocol.** The first is marked required while the phase prompt defines a fallback and R-2 requires manual orchestration to work.

## Risks / Trade-offs

- [The interview records thin or wrong facts, and the challenger then challenges against them] → it writes only user statements, shows the draft before writing, and the file is plain text the user can edit.
- [A subagent's Read of the plugin cache may be blocked or prompt on the desktop app] → the script path works there (verified); task 5.5 tests the subagent read, and if blocked the command can inline the framework text instead.
- [The domain table drifts from the domain configs] → generated and checked.
- [Project facts contain sensitive content that reaches the challenger and the transcript] → documented in the command; the file lives in the user's project.
- [The synthesizer template drifts from the repo-local agent's rules] → the drift test compares the shared rules section.
- [Plugin agents named `challenger` / `synthesizer` clash with repo-local ones inside this repository] → plugin agents are namespaced; the commands name them explicitly. Verified in task 5.4.

## Migration Plan

Ship in one PR after `layering-consistency` merges. No data migration; `.persona/context.md` is new. Rollback is reverting the PR; the version bump makes the change visible to installers.
