## 1. Generator and checks

- [x] 1.1 Extend `scripts/build_persona_index.py` to emit `plugin/framework/` (the three framework files) and `plugin/agents/` (challenger only; the synthesizer is hand-written), and to check them in `--check` mode with the same missing/extra/differs reporting as the catalog
- [x] 1.2 Generate `plugin/framework/domains.json` (domain name → `challenge_focus` or absent, plus description) from the domain-level `context_configuration.json` files and check it in `--check` mode; the name is the directory name and a `context_name` that disagrees with it is an error
- [x] 1.3 Add unit tests in `scripts/` for the new generation: missing, stale, extra and clean cases; confirm no source file is modified

## 2. Resolution script

- [x] 2.1 Add `resolve [--focus F] [--domain D]` to `plugin/scripts/tif.py`: lens precedence (`--focus` > context `focus` > `--domain` > context `domain` > first-principles) with its source printed, project facts from `.persona/context.md`, persona digest from `.persona/personas/*.json`
- [x] 2.2 Handle the edge cases: no context file, empty file, unparseable front matter, unknown domain (error listing known names), domain without a `challenge_focus`, empty or missing `.persona/personas/`
- [x] 2.3 Add tests to `plugin/scripts/test_tif.py` for each precedence step and each edge case; update the generated help table (`tif.py --sync`)

## 3. Plugin files

- [x] 3.1 Write `plugin/commands/context.md` (the interview: short rounds, domain suggestion from the bundled table, draft shown, written only after a yes, existing file edited not overwritten, records only what the user says)
- [x] 3.2 Write `plugin/commands/challenge.md` (runs `resolve`, passes only request + `domain_context` + `active_personas` to the `challenger`)
- [x] 3.3 Write `plugin/commands/synthesize.md` (same, plus the Challenge Artifact and `framework_dir`)
- [x] 3.4 Write the plugin synthesizer template: reads from `framework_dir`, states which lens and whether project context was used
- [x] 3.5 Bump `plugin/.claude-plugin/plugin.json` one minor version above the version on main (0.3.0 if the uninstall change has merged)

## 4. Drift tests

- [x] 4.1 Extend `scripts/test_challenge_agents.py`: plugin challenger body equals the phase prompt slice; plugin and repo-local commands name the same subagents and pass-only rules; synthesizer rules sections match

## 5. Verification

- [x] 5.1 Run `python3 -m unittest discover -s scripts`, `python3 -m unittest discover -s plugin/scripts`, `python3 plugin/scripts/tif.py --check`, `python3 scripts/build_persona_index.py --check`
- [x] 5.2 In a temp project with the plugin loaded via `--plugin-dir`: run `/tif:context` headless against a scripted set of answers and confirm the file written matches them and nothing else
- [ ] 5.3 (done: context run, synthesize with context; remaining: personas-only synthesize) Run `/tif:challenge` and `/tif:synthesize` headless with no context, with personas only, and with a context file; repeat the earlier comparison and confirm the context run's required clarifications are decision-level; confirm no `config/` read and every RC and AF is traced
- [x] 5.4 Run `claude plugin validate` on the repository and check agent name behavior when the plugin is loaded inside this repository
- [ ] 5.5 Desktop app (manual, by the user): run `/tif:context`, `/tif:challenge` and `/tif:synthesize` in a scratch project, including the synthesizer's read of the framework files in the plugin cache; record the result

## 6. Docs

- [x] 6.1 Update the README plugin section and `plugin/skills/catalog` docs where they list the exposed surface; document `.persona/context.md` and what leaves the project when the commands run
- [x] 6.2 Update the protocol's runtime table row for Claude Code to mention the plugin
- [x] 6.3 Make `domain_context` and `active_personas` optional in `config/challenge_synthesis_protocol.md` (with a changelog entry) and state the first-principles default
