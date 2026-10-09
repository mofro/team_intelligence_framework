# persona-index roadmap

Items deliberately left out of `openspec/changes/persona-index/` to keep that change small. Each can be handed to `persona-conductor-proto` as consumer behavior, or implemented in this repo's index/generator when a consumer needs it. Source: design discussion of 2026-10-09.

Rule of thumb: pull an item in when a real consumer needs it, not before.

## Consumer-side (suggestions for persona-conductor-proto)

| Item | What it is | Why it might matter | Cost |
|---|---|---|---|
| Hash verification | Check each fetched file's sha256 against its index entry before installing; refuse on mismatch. | Detects corrupted or tampered downloads and a mismatched index/file ref. | Small. The hashes are already in the index. |
| Tag pinning | Fetch `index.json` and files from a release tag, not `main`. | Stable installs. Needs this repo to cut tags. | Small. |
| Compatibility checks | Compare `index_version` and each entry's `schema_version` to supported values; warn or refuse on unknown. | Protects against future schema changes. | Small, but only useful once a second schema exists. |
| Stub disclosure | Before installing, list selected personas with status `stub` (and teams that contain stubs). | The user knows they are installing a placeholder. | Small. Status is already in the index. |
| Install layout | Install files at the same relative paths as in the repo so existing team and persona files keep working. | Avoids a second layout to support. | Small, but it is Conductor's design choice. |
| De-duplication | When a team and an individual persona overlap, fetch the shared file once. | Avoids double installs. | Trivial. |

## Index-side (candidates for this repo)

| Item | What it is | Why it might matter | Cost |
|---|---|---|---|
| `dependencies` per persona | List each `reference_libraries` item (type, description, url, depth) with a `resolvable` flag, false for `internal://` URLs that match no repo file. | Shows which personas rely on knowledge files that cannot be fetched. Several personas reference `internal://` files that do not exist. | Medium: needs a resolution rule for `internal://` names. |
| Context config listing | List each domain's `context_configuration*.json` with path, bytes and sha256. | Lets a consumer fetch domain activation behavior if it wants it. Unknown whether Conductor needs it. | Small. |
| Tags | A `tags` field per persona and team for discovery. | Better browsing and search. Needs a tagging source: derive from `expertise`/`specializations` or add to files. | Medium. Deferred by decision. |
| Compact persona profile | A smaller derived form of a persona for token-constrained sessions. | Cheaper sessions. | High risk: a second format that could diverge from the real one. Rejected for now to protect compatibility. |
| Browse page | A GitHub Pages view generated from the index. | Easier human discovery. | Small to medium. |

## Repo hygiene follow-ups (not index work)

- Reconcile the four stale ids in `personas/development/context_configuration.json`. Needs a decision on which handle users should type, and a before/after behavior check. See design.md "Decision: do not edit context_configuration".
- Decide `security_review_team`: write a real team file or remove it from `available_teams`.
- Rename `personas/examples/*.json` (Markdown content) to `.md`.
