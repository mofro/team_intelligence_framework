## 1. Bundled catalog generation

- [ ] 1.1 Extend `scripts/build_persona_index.py` to emit `plugin/catalog/` containing `index.json` and copies of every persona and team file listed in it, preserving relative paths. Verify by running it and diffing the copied files against their sources.
- [ ] 1.2 Extend `--check` to fail when `plugin/catalog/` is missing, has extra files, or differs from the sources, and to print the regeneration command. Verify with a test that edits one bundled file and expects a nonzero exit.
- [ ] 1.3 Add generator tests for the new behavior alongside the existing generator tests. Verify the whole test suite passes.

## 2. Command table and `tif.py`

- [ ] 2.1 Create `plugin/scripts/tif.py` with the single command table (name, arguments, one-line description) and argument parsing. Verify `tif.py --help` and `tif.py help` print the same text, generated from the table.
- [ ] 2.2 Implement `list [--domain D]` and `teams` from the bundled index, with status markers. Verify against the current index (28 personas, 6 teams) and with an unknown domain.
- [ ] 2.3 Implement `info <id|alias>` for personas and teams, including ambiguous and unknown names. Verify with an alias, an id, an ambiguous alias and an unknown name.
- [ ] 2.4 Implement `install <persona|team>` with sha256 verification, no-overwrite-without-`--force`, `.persona/personas/` and `.persona/teams/` targets, member installation, and warn-only disclosure. Verify in a temporary directory: fresh install, repeat install, locally edited file, `--force`, corrupted bundled file, team with stubs, team with unresolved members, team with a missing primary voice, virtual team.
- [ ] 2.5 Add `--check` that compares the command table with the SKILL.md help block and the README Quick Start block. Verify it fails when either is edited by hand.
- [ ] 2.6 Write `unittest` tests for all of the above using the standard library only. Verify the suite passes with `python3 -m unittest`.

## 3. Skill and documentation

- [ ] 3.1 Write `plugin/skills/catalog/SKILL.md`: a thin wrapper that runs `tif.py` with the user's arguments and relays the output without reading the catalog. Verify the file contains the generated help block and no instruction to read catalog files.
- [ ] 3.2 Generate the README Quick Start block from the command table and note that Conductor ignores installed team files for now. Verify `tif.py --check` passes.

## 4. Manifest, marketplace and validation

- [ ] 4.1 Add `plugin/.claude-plugin/plugin.json` (name, version, description, author, license) and `.claude-plugin/marketplace.json` pointing to `./plugin`. Verify with `claude plugin validate`.

## 5. End-to-end check

- [ ] 5.1 In a clean project, add the marketplace, install the plugin with the CLI, and run `/tif:catalog help`, `list`, `info`, and `install` for one persona and one team. Verify files land in `.persona/personas/` and `.persona/teams/` and that Conductor still starts without error when both are installed.
- [ ] 5.2 Record that the desktop app was not tested. Verify the note appears in the README.

## 6. Spec hygiene

- [ ] 6.1 Run `openspec validate tif-plugin --strict`. Verify it passes.
