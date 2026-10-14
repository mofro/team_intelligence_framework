## 1. Generator and checks

- [ ] 1.1 Extend `scripts/build_persona_index.py` to emit `plugin/framework/` (the three files) and `plugin/agents/` (challenger, synthesizer), and to check them in `--check` mode with the same missing/extra/differs reporting as the catalog
- [ ] 1.2 Add unit tests in `scripts/` for the new generation: missing, stale, extra, and clean cases; confirm no source file is modified

## 2. Plugin files

- [ ] 2.1 Write `plugin/commands/challenge.md` (challenge_focus fallback, passes only focus + request)
- [ ] 2.2 Write `plugin/commands/synthesize.md` (passes request, artifact, `framework_dir`, optional domain config path)
- [ ] 2.3 Write the plugin synthesizer template: reads from `framework_dir`, proceeds without a domain config and says so
- [ ] 2.4 Bump `plugin/.claude-plugin/plugin.json` to 0.2.0

## 3. Drift tests

- [ ] 3.1 Extend `scripts/test_challenge_agents.py`: plugin challenger body equals the phase prompt slice; plugin and repo-local commands name the same subagents; synthesizer rules sections match

## 4. Verification

- [ ] 4.1 Run `python3 -m unittest discover -s scripts`, `python3 -m unittest discover -s plugin/scripts`, `python3 plugin/scripts/tif.py --check`, `python3 scripts/build_persona_index.py --check`
- [ ] 4.2 Copy `plugin/` to a temp directory in an empty project, load it with `--plugin-dir`, run `/tif:challenge` and `/tif:synthesize` headless, and confirm no `config/` read and the synthesis traces every RC and AF
- [ ] 4.3 Run both with a domain config path and without; confirm the no-domain note
- [ ] 4.4 Run `claude plugin validate` on the repository
- [ ] 4.5 Check name clash behavior when the plugin is loaded inside this repo
- [ ] 4.6 Try `/tif:challenge` in the desktop app (manual, by the user) and record the result

## 5. Docs

- [ ] 5.1 Update the README plugin section and `plugin/skills/catalog` docs if they list the exposed surface
- [ ] 5.2 Update the protocol's runtime table row for Claude Code to mention the plugin
