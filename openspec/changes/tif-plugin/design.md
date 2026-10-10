## Context

TIF is a set of persona and team JSON files plus a generated `index.json` (28 personas, 6 teams at the time of writing). Persona files total roughly 99 KB and team files roughly 21 KB. The index carries id, name, summary, role, domain, subdomain, schema_version, version, path, bytes, sha256, aliases, expertise and status; team entries add members, default_primary, unresolved_members, aliases and status.

Today a user adopts TIF by cloning the repo and following the README. Conventions such as `personas on` are interpreted by the model step by step.

Conductor (a separate Claude Code plugin) is the lean runtime. It reads `.persona/personas/*.json`, compiles personas to prompt blocks without a model, and skips JSON that is not a persona. Its SessionStart hook is the only hook in the picture.

An installed plugin runs from a cache copy of the plugin directory, not from the repository. Anything the plugin needs at runtime must therefore live inside `plugin/`.

## Goals / Non-Goals

**Goals:**
- One discoverable, deterministic entry point with a real `--help`.
- Works wherever Claude Code plugins work, with no network needed after install.
- Token-light: the model relays script output and does not read the catalog.
- A clean, loose relationship with Conductor.

**Non-Goals:**
- Replacing TIF's standalone convention. It stays untouched.
- Hooks in the TIF plugin. Conductor owns session start.
- Reading or acting on team collaboration fields (`primary_voice`, `decision_pattern`). The files are installed so they are available later.
- An `update` subcommand. Deferred until a real need appears.
- Deciding the voice policy (one unified voice versus labeled voices). That is a separate layer from packaging.

## Decisions

**Plugin name `tif`, one skill `catalog`.** Short, unique, and not `persona`. One skill with subcommands keeps the surface at a single slash command, `/tif:catalog`. Alternatives considered: several skills (`/tif:list`, `/tif:install`), which spreads the help across the command list and costs more description tokens at session start; naming it after the framework in full, which is long to type.

**A script does the work; the skill is a thin wrapper.** `tif.py` parses arguments, reads the bundled index, and prints. SKILL.md tells Claude to run the script with the user's arguments and relay the output. This is the deterministic, low-token property the proposal exists for. Alternative: let the model read the index and copy files itself, which is what happens today and is the problem.

**Bundle a generated catalog inside `plugin/catalog/`.** Because the plugin runs from a cache copy, the catalog cannot be referenced from the repo root. A generated copy costs about 150 KB and removes any network dependency. Alternative: fetch from GitHub at install time, which needs network, needs a pin to avoid drift, and fails offline.

**Generated copy is kept honest by a check.** `build_persona_index.py --check` already guards the index. It is extended to compare `plugin/catalog/` with the sources. Same pattern, same failure mode.

**Marketplace entry at the repo root pointing to `./plugin`.** This is Conductor's pattern. This repository's marketplace lists only this plugin; Conductor keeps its own marketplace in its own repository. The two plugins are installed independently.

**Install verifies hashes and protects local edits.** Each file is checked against the sha256 in the index before it is copied. A file already present that differs from the catalog is not overwritten without `--force`, because Conductor's documentation tells users they may edit their project copies. A present file identical to the catalog is reported as already installed.

**Warn, never refuse.** A half-filled team can still be useful, and "incomplete" depends on what the user needs. So install always proceeds and discloses: the count and names of stub personas, any missing members, and, loudly, a missing primary voice. This follows the index status values (`complete`, `contains_stubs`, `incomplete` for teams; `complete`, `stub` for personas).

**Team install pulls member personas.** A team file without its members is not usable. Members that exist are installed; members that do not exist are named in a warning. Virtual teams (no file by design, for example `security_review_team`) install their members only and say so.

**One command table.** The subcommand names, arguments and one-line descriptions live in one table in `tif.py`. `--help`, the SKILL.md help block and the README Quick Start are generated from it, and `--check` fails if any of the three differ. This avoids the usual drift between code and docs.

**Python 3 standard library only.** Same requirement as Conductor, nothing to install.

## Risks / Trade-offs

- Stale bundled catalog: mitigated by the extended `--check` in CI, but a contributor can still forget to regenerate locally. The check message names the command to run.
- Desktop-app behavior is untested, as with Conductor. Only the CLI will be exercised.
- Installed team files are inert until Conductor honors them. Users could expect more. The install output states that Conductor currently ignores team files.
- Stubs install by design, so a user may adopt a persona with little content. The warning is the mitigation; blocking is rejected as the user's call to make.

## Migration Plan

No migration. Everything is additive. Existing users of the standalone convention see no change. Rollback is removing `plugin/` and the marketplace file.

## Open Questions

- Should the generator change be described as a modification of the `persona-index` capability, or kept as packaging-only? Check the existing spec wording.
- Should `list` show status markers by default or behind a flag?
- When Conductor eventually honors team files, which side owns the team-file location? Current assumption: `.persona/teams/`.
