## 1. Generator and checks

- [ ] 1.1 Extend `scripts/build_persona_index.py` to emit `plugin/framework/` (the three files) and `plugin/agents/` (challenger, synthesizer), and to check them in `--check` mode with the same missing/extra/differs reporting as the catalog
- [ ] 1.2 Generate `plugin/framework/domains.json` from the context configurations (name → `challenge_focus`, project inherits from its domain, name collision is an error) and check it in `--check` mode
- [ ] 1.3 Add unit tests in `scripts/` for the new generation: missing, stale, extra, and clean cases; confirm no source file is modified

## 2. Plugin files

- [ ] 2.1 Write `plugin/commands/challenge.md` (`--focus` / `--domain` / first-principles resolution, unknown-domain error, passes only the resolved focus + request)
- [ ] 2.2 Write `plugin/commands/synthesize.md` (same flags; passes request, artifact, `framework_dir` and the resolved lens)
- [ ] 2.3 Write the plugin synthesizer template: reads from `framework_dir`, takes the resolved lens and states which lens it used
- [ ] 2.4 Bump `plugin/.claude-plugin/plugin.json` to 0.2.0

## 3. Drift tests

- [ ] 3.1 Extend `scripts/test_challenge_agents.py`: plugin challenger body equals the phase prompt slice; plugin and repo-local commands name the same subagents; synthesizer rules sections match

## 4. Verification

- [ ] 4.1 Run `python3 -m unittest discover -s scripts`, `python3 -m unittest discover -s plugin/scripts`, `python3 plugin/scripts/tif.py --check`, `python3 scripts/build_persona_index.py --check`
- [ ] 4.2 Copy `plugin/` to a temp directory in an empty project, load it with `--plugin-dir`, run `/tif:challenge` and `/tif:synthesize` headless, and confirm no `config/` read and the synthesis traces every RC and AF
- [ ] 4.3 Run both with `--focus`, with `--domain` (including an inheriting project), and with neither; confirm the lens is reported and an unknown domain errors
- [ ] 4.4 Run `claude plugin validate` on the repository
- [ ] 4.5 Check name clash behavior when the plugin is loaded inside this repo
- [ ] 4.6 Try `/tif:challenge` in the desktop app (manual, by the user) and record the result

## 5. Docs

- [ ] 5.1 Update the README plugin section and `plugin/skills/catalog` docs if they list the exposed surface
- [ ] 5.2 Update the protocol's runtime table row for Claude Code to mention the plugin
- [ ] 5.3 Change `domain_context` from required to optional in `config/challenge_synthesis_protocol.md` (with a changelog entry) and state the first-principles default
