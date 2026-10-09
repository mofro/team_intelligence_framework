## 1. Stub personas

- [x] 1.1 Create `personas/ai_development/{system_architect,data_scientist,backend_developer,product_manager}_persona_schema.json` with all 1.2 top-level and `persona` keys, `"stub": true`, a stub notice in `metadata.description`, and role/expertise/approach seeded only from `intelligence_framework_team.json` (`decision_hierarchy` and `collaboration_patterns`). Verify each parses as JSON and has the same key set as `estate_planner_schema.json` plus `stub`.
- [x] 1.2 Add the first-invocation notice rule to each stub's `behavioral_rules` (announce stub status once per session, offer to define the persona, still help with the task). Verify the rule text is present in all four and read it against the persona-stubs spec scenarios.
- [ ] 1.3 In a scratch session, load one stub through the normal persona procedure and address it with `@<persona_name>`. Verify the notice appears once on first use and is not repeated, and that the task is still answered.

## 2. Generator

- [x] 2.1 Create `scripts/build_persona_index.py` (Python 3 standard library only) that discovers persona files per the persona-index qualification rules and writes nothing but `index.json`. Verify by running it and confirming `git status` shows only `index.json` (and the new stub/script files) changed.
- [x] 2.2 Build persona entries (id, name, summary, role, domain, subdomain, schema_version, version, path, bytes, sha256, aliases, expertise, status) with deterministic ordering and formatting and no timestamps. Verify two consecutive runs produce byte-identical output (`diff` of two outputs is empty).
- [x] 2.3 Implement alias derivation and the collision checks. Verify with unit tests that `ott_ux_persona`, `10_foot_ui_designer`, `design_expert` and `developer_coding_persona` resolve to `ux_designer`, `ui_designer`, `ux_ui_strategist` and `experienced_developer`, and that two fixture personas producing the same alias cause an error.
- [x] 2.4 Build team entries with `members`, `default_primary`, `aliases`, member resolution and stub flagging. Verify against fixtures: all members present passes, a missing member produces an error naming team and member, and a team with a stub member is flagged.
- [x] 2.5 Read `context_configuration*.json` files and emit notes for alias-resolved references and warnings for unresolved ones, without failing or modifying them. Verify `security_review_team` is a warning and the four stale ids are notes, and that the context files are byte-identical before and after (checksum).
- [x] 2.6 Implement `--check`: regenerate in memory, compare with committed `index.json`, exit non-zero without writing on stale or errored state. Verify by editing a persona's description, running `--check` (non-zero, says stale), reverting the edit, and running it again (zero).
- [x] 2.7 Add unit tests (`scripts/test_build_persona_index.py`, standard `unittest`) covering qualification and exclusions (template, `examples/`, non-JSON), missing optional fields (null `custom_name`, absent `reference_libraries`), error and warning severities, and determinism. Verify `python3 -m unittest` passes.

## 3. Index and CI

- [x] 3.1 Run the generator and commit `index.json`. Verify it contains 28 personas (24 existing personas, excluding the template, plus 4 stubs), 6 team entries, zero errors, and that every entry's `sha256` matches `shasum -a 256` of its file for a sample of five.
- [x] 3.2 Add `.github/workflows/persona-index.yml` that runs the unit tests and `--check` on pull requests and pushes to the default branch. Leave `collect-context.yml` untouched. Verify with a test branch push that the workflow passes on the clean tree and fails after an unregenerated persona edit.

## 4. Documentation

- [x] 4.1 Add a "Retrieving personas" section to `README.md` describing `index.json`, how to regenerate it, how to look up personas by id or alias and teams by id, the stub marker, and a pointer to `.devnotes/persona-index-roadmap.md`. Verify every command in the section runs as written.
- [x] 4.2 Record the deferred decisions in `TODO.md`: reconcile development context ids (needs the `@developer_coding_persona` vs `@experienced_developer` decision, and a manual check of current framework behavior with the mismatched ids), `security_review_team` fate, and tags. Verify the entries link to `design.md` and the roadmap file.

## 5. Acceptance

- [x] 5.1 Simulate a consumer without Conductor: using only `index.json`, look up `retirement_planning_team` and `design_expert`, fetch those files from the working tree by `path` into a clean temp directory, and check the result contains exactly the team file and seven persona files. Verify with a script and a directory listing.
- [x] 5.2 Run `openspec validate persona-index --strict` and confirm it passes, then confirm none of the existing persona, team, or context files differ from `main` (`git diff --stat main -- personas` shows only the 4 added stubs).
