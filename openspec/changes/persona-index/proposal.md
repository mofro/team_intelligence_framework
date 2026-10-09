## Why

`persona-conductor-proto` needs personas from this repo to work, but the only install path today is copying files by hand from a downloaded copy of the repo. Nothing in this repo lists what personas and teams exist, where they live, or what they depend on, so neither Conductor nor anyone else can query the repo and fetch only what they want.

Auditing the repo for this change also found that the catalog has gaps a machine-readable index would expose: persona ids are referenced two different ways, and four team members have no persona file because they were improvised in sessions.

## What Changes

- Add a generated, committed `index.json` at the repo root listing every persona and team, with path, domain, summary, role, expertise, `schema_version`, byte size, content hash, `aliases` and (for teams) members.
- Add a generator script (`scripts/build_persona_index.py`, Python 3 standard library only) with a `--check` mode, and a CI workflow that fails when `index.json` is stale or the catalog has errors.
- Define **id resolution**: `persona.persona_name` is the canonical id, matching the existing documented convention. Each entry also carries `aliases` (derived from the file name) so a consumer reading the index can resolve the ids used in the older `context_configuration.json` files. This helps index consumers only; it does not change how the framework itself treats those ids.
- Add **stub personas** for the four team members that have no file (`system_architect`, `data_scientist`, `backend_developer`, `product_manager`). A stub is a valid persona file in the current 1.2 schema, seeded from what the team file already says about the role. It tells the user it is a stub the first time it is invoked and proposes fleshing it out.
- Define the minimal **retrieval contract**: a consumer fetches `index.json` at a git ref, selects personas by id or alias and/or teams by id, and fetches only those files by path. A team entry lists its members, so a team works as a one-step bundle. Further consumer behavior (hash verification, tag pinning, compatibility checks, stub disclosure, install layout) is recorded as recommendations in `docs/persona-index-roadmap.md` rather than required here.
- **No change** to any existing persona, team or `context_configuration.json` file. The id mismatches in `personas/development/context_configuration.json` are reported by the generator as warnings and resolved through aliases. Whether to edit that config is deferred to a separate change (see design.md, "Decision: do not edit context_configuration").
- Tags are explicitly out of scope for this change.

## Capabilities

### New Capabilities

- `persona-index`: the format, generation rules, validation rules and CI freshness check for the root `index.json` covering personas, teams and id aliases.
- `persona-stubs`: how a placeholder persona is represented, how the index marks it, and how it prompts for completion when invoked.
- `persona-retrieval`: what a consumer (Conductor or any other tool) can rely on from the index to select personas or teams and fetch only those files.

### Modified Capabilities

None. `openspec/specs/` is empty, so there are no existing capability requirements to modify.

## Impact

- **New files:** `index.json`, `scripts/build_persona_index.py`, `.github/workflows/persona-index.yml`, four stub persona files under `personas/ai_development/`, and a README section on retrieval, and `docs/persona-index-roadmap.md`.
- **Existing files:** the existing 24 persona files, the template, 6 team files and 7 `context_configuration.json` files are not modified.
- **Not touched:** the existing `.github/workflows/collect-context.yml`.
- **Other repos:** `persona-conductor-proto` needs a follow-up change to use the retrieval contract. That change is out of scope here, and this proposal has not examined that repo's loading code, so the contract is written from this repo's side only and kept minimal. The roadmap file lists additions to pass to that work.
- **Compatibility:** the index is purely additive and no persona file format changes. The only schema-adjacent addition is the stub marker, which sits in a new optional top-level key that existing readers can ignore.
