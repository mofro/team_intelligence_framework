## Why

Using TIF today means reading the README, copying files by hand, and typing conventions such as `personas on` that Claude then interprets step by step. That costs tokens, varies run to run, and has no `--help`. It also only works for someone who has cloned the repo.

A Claude Code plugin gives TIF one deterministic, discoverable entry point that works wherever plugins work. A script does the listing, lookup and copying; the model only relays the output.

The plugin name must not be `persona`, which another plugin already uses. This proposal uses `tif`.

## What Changes

- Add a Claude Code plugin named `tif` with a single skill, `catalog`, invoked as `/tif:catalog <subcommand>`.
- Subcommands in the first version: `help`, `list [--domain D]`, `teams`, `info <id|alias>`, `install <persona|team>`. `update` is deferred.
- Add `plugin/scripts/tif.py` (Python 3 standard library only) that implements every subcommand deterministically.
- Install copies verified files into the user's project: personas into `.persona/personas/`, teams into `.persona/teams/`. Installing a team also installs its member personas.
- Install verifies each file against the sha256 in `index.json` before copying, and does not overwrite a changed local file unless `--force` is given.
- Install never refuses on content. It warns on stub personas (count and names), on missing team members, and loudly when a team's primary voice is missing.
- Add a generated copy of the catalog at `plugin/catalog/` (index, persona files, team files) so the installed plugin, which runs from a cache copy, can install without network access. `build_persona_index.py` gains a step to emit it and `--check` fails on drift.
- One command table drives `tif.py --help`, the SKILL.md help text and the README Quick Start; a `--check` mode fails when they drift.
- Add `.claude-plugin/marketplace.json` at the repo root pointing at `./plugin`, and `plugin/.claude-plugin/plugin.json`.

Not changed: TIF's standalone convention (config documents, `personas on`) stays as is. The plugin adds no hooks. It does not read team collaboration fields.

## Capabilities

### New Capabilities
- `tif-catalog-browse`: read-only subcommands (`help`, `list`, `teams`, `info`) answered from the catalog index by script.
- `tif-catalog-install`: copying personas and teams into a project with hash verification, overwrite protection and warn-only disclosure of stubs and incomplete teams.
- `tif-plugin-packaging`: plugin manifest, marketplace entry, bundled catalog copy and the drift checks that keep it and the command documentation in sync.

### Modified Capabilities
- None in this draft. The generator change (emitting the bundled catalog) is specified under `tif-plugin-packaging`. Whether it should instead be a delta on the existing `persona-index` capability is an open question in the design.

## Impact

- New: `.claude-plugin/marketplace.json`, `plugin/` (manifest, skill, `scripts/tif.py`, `catalog/`), tests for `tif.py`.
- Changed: `scripts/build_persona_index.py` (emit and check the bundled copy), `README.md` (Quick Start generated from the command table).
- Repository size grows by roughly 150 KB for the bundled catalog. It is never loaded into model context.
- Relationship with Conductor: Conductor reads `.persona/personas/*.json` and skips other JSON, so installed team files are ignored by it today. Honoring team files is a later decision and is out of scope. The two plugins share no code and no hooks.
- Requires `python3` on the user's machine, the same as Conductor.
