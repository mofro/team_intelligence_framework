#!/usr/bin/env python3
"""Generate index.json: a catalog of the personas and teams in this repository.

Usage:
    python3 scripts/build_persona_index.py            # write index.json
    python3 scripts/build_persona_index.py --check    # exit 1 if index.json is stale or errors exist

The index is derived only from files under personas/. Nothing else is read or
modified. Spec: openspec/changes/persona-index/.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

INDEX_VERSION = 1
TEMPLATE_PATH = "personas/persona_schema_example.json"
EXAMPLES_PREFIX = "personas/examples/"

ERROR, WARNING, NOTE = "error", "warning", "note"


def sha256_of(data):
    return hashlib.sha256(data).hexdigest()


def derive_aliases(path):
    """File-name stem, then with version suffix, `_schema`, `_persona` stripped one at a time."""
    stem = Path(path).name[: -len(".json")]
    aliases = [stem]
    shorter = re.sub(r"_v\d+(\.\d+)*$", "", stem)
    if shorter != stem:
        aliases.append(shorter)
        stem = shorter
    for suffix in ("_schema", "_persona"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            aliases.append(stem)
    return aliases


def domain_parts(rel_path):
    """(domain, subdomain) from a path below personas/. A `teams` directory is not a subdomain."""
    parts = Path(rel_path).parts[1:-1]  # drop leading "personas" and the file name
    parts = [p for p in parts if p != "teams"]
    domain = parts[0] if parts else None
    subdomain = "/".join(parts[1:]) if len(parts) > 1 else None
    return domain, subdomain


def classify(rel_path):
    name = Path(rel_path).name
    if rel_path == TEMPLATE_PATH or rel_path.startswith(EXAMPLES_PREFIX):
        return "skip"
    if name.startswith("context_configuration"):
        return "context"
    if "teams" in Path(rel_path).parts[:-1]:
        return "team"
    return "persona"


def load_json(root, rel_path, diagnostics):
    data = (root / rel_path).read_bytes()
    try:
        return data, json.loads(data.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        diagnostics.append((ERROR, f"{rel_path}: cannot parse as JSON ({exc})"))
        return data, None


def require(diagnostics, rel_path, obj, dotted, label):
    cur = obj
    for key in dotted.split("."):
        if not isinstance(cur, dict) or key not in cur or cur[key] in (None, ""):
            diagnostics.append((ERROR, f"{rel_path}: missing required field {label}"))
            return None
        cur = cur[key]
    return cur


def build_index(root):
    """Return (index_dict, diagnostics). Diagnostics are (level, message) tuples."""
    root = Path(root)
    diagnostics = []
    files = sorted(
        p.relative_to(root).as_posix() for p in (root / "personas").rglob("*.json")
    )

    persona_entries, team_files, context_files = [], [], []
    for rel in files:
        kind = classify(rel)
        if kind == "skip":
            continue
        raw, obj = load_json(root, rel, diagnostics)
        if obj is None:
            continue
        if kind == "context":
            context_files.append((rel, obj))
        elif kind == "team":
            team_files.append((rel, raw, obj))
        else:
            if not (isinstance(obj.get("metadata"), dict) and isinstance(obj.get("persona"), dict)):
                diagnostics.append((WARNING, f"{rel}: not indexed (no top-level metadata and persona objects)"))
                continue
            entry = persona_entry(rel, raw, obj, diagnostics)
            if entry:
                persona_entries.append(entry)

    # Unique ids
    by_id = {}
    for e in persona_entries:
        if e["id"] in by_id:
            diagnostics.append((ERROR, f"duplicate persona id '{e['id']}': {by_id[e['id']]['path']} and {e['path']}"))
        else:
            by_id[e["id"]] = e

    # Alias collisions
    alias_owner = {}
    for e in persona_entries:
        for a in e["aliases"]:
            if a in by_id and by_id[a]["id"] != e["id"]:
                diagnostics.append((ERROR, f"alias '{a}' of '{e['id']}' equals the id of a different persona ({by_id[a]['path']})"))
            if a in alias_owner and alias_owner[a] != e["id"]:
                diagnostics.append((ERROR, f"alias '{a}' maps to both '{alias_owner[a]}' and '{e['id']}'"))
            alias_owner.setdefault(a, e["id"])

    team_entries = []
    for rel, raw, obj in team_files:
        entry = team_entry(rel, raw, obj, by_id, diagnostics)
        if entry:
            team_entries.append(entry)
    team_alias_owner = {}
    team_ids = {t["id"] for t in team_entries}
    for t in team_entries:
        for a in t["aliases"]:
            if a in team_ids:
                diagnostics.append((ERROR, f"alias '{a}' of team '{t['id']}' equals the id of a different team"))
            if a in team_alias_owner and team_alias_owner[a] != t["id"]:
                diagnostics.append((ERROR, f"team alias '{a}' maps to both '{team_alias_owner[a]}' and '{t['id']}'"))
            team_alias_owner.setdefault(a, t["id"])

    for rel, obj in context_files:
        check_context(rel, obj, by_id, alias_owner, team_ids, team_alias_owner, diagnostics)

    persona_entries.sort(key=lambda e: e["id"])
    team_entries.sort(key=lambda e: e["id"])
    index = {"index_version": INDEX_VERSION, "personas": persona_entries, "teams": team_entries}
    return index, diagnostics


def persona_entry(rel, raw, obj, diagnostics):
    pid = require(diagnostics, rel, obj, "persona.persona_name", "persona.persona_name")
    name = require(diagnostics, rel, obj, "metadata.name", "metadata.name")
    summary = require(diagnostics, rel, obj, "metadata.description", "metadata.description")
    role = require(diagnostics, rel, obj, "persona.role", "persona.role")
    schema_version = require(diagnostics, rel, obj, "schema_version", "schema_version")
    version = require(diagnostics, rel, obj, "metadata.version", "metadata.version")
    if None in (pid, name, summary, role, schema_version, version):
        return None
    domain, subdomain = domain_parts(rel)
    aliases = []
    for a in derive_aliases(rel):
        if a != pid and a not in aliases:
            aliases.append(a)
    return {
        "id": pid,
        "name": name,
        "summary": summary,
        "role": role,
        "domain": domain,
        "subdomain": subdomain,
        "schema_version": schema_version,
        "version": version,
        "path": rel,
        "bytes": len(raw),
        "sha256": sha256_of(raw),
        "aliases": aliases,
        "expertise": obj["persona"].get("expertise") or [],
        "status": "stub" if obj.get("stub") is True else "complete",
    }


def team_entry(rel, raw, obj, by_id, diagnostics):
    tid = require(diagnostics, rel, obj, "team.team_name", "team.team_name")
    name = require(diagnostics, rel, obj, "team.display_name", "team.display_name")
    summary = require(diagnostics, rel, obj, "team.description", "team.description")
    members = require(diagnostics, rel, obj, "team.members", "team.members")
    primary = require(diagnostics, rel, obj, "team.default_primary", "team.default_primary")
    if None in (tid, name, summary, members, primary):
        return None
    for m in members:
        if m not in by_id:
            diagnostics.append((ERROR, f"team '{tid}' ({rel}): member '{m}' has no persona file"))
    if primary not in by_id:
        diagnostics.append((ERROR, f"team '{tid}' ({rel}): default_primary '{primary}' has no persona file"))
    has_stub = any(m in by_id and by_id[m]["status"] == "stub" for m in members)
    domain, _ = domain_parts(rel)
    aliases = []
    for a in derive_aliases(rel):
        if a != tid and a not in aliases:
            aliases.append(a)
    return {
        "id": tid,
        "name": name,
        "summary": summary,
        "domain": domain,
        "members": members,
        "default_primary": primary,
        "aliases": aliases,
        "path": rel,
        "bytes": len(raw),
        "sha256": sha256_of(raw),
        "status": "contains_stubs" if has_stub else "complete",
    }


def check_context(rel, obj, by_id, alias_owner, team_ids, team_alias_owner, diagnostics):
    refs = []
    for key in ("available_personas", "always_on_personas"):
        refs += [(key, v) for v in obj.get(key) or []]
    if obj.get("default_primary_persona"):
        refs.append(("default_primary_persona", obj["default_primary_persona"]))
    for key, value in refs:
        if value in by_id:
            continue
        if value in alias_owner:
            diagnostics.append((NOTE, f"{rel}: {key} '{value}' resolves via alias to '{alias_owner[value]}'"))
        else:
            diagnostics.append((WARNING, f"{rel}: {key} '{value}' does not match any persona"))
    for value in obj.get("available_teams") or []:
        if value in team_ids:
            continue
        if value in team_alias_owner:
            diagnostics.append((NOTE, f"{rel}: available_teams '{value}' resolves via alias to '{team_alias_owner[value]}'"))
        else:
            diagnostics.append((WARNING, f"{rel}: available_teams '{value}' does not match any team file"))


def render(index):
    return json.dumps(index, indent=2, ensure_ascii=False) + "\n"


def report(diagnostics, stream):
    order = {ERROR: 0, WARNING: 1, NOTE: 2}
    for level, msg in sorted(diagnostics, key=lambda d: (order[d[0]], d[1])):
        print(f"{level.upper()}: {msg}", file=stream)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--check", action="store_true", help="do not write; exit 1 if index.json is stale or errors exist")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent.parent), help="repository root")
    args = parser.parse_args(argv)

    root = Path(args.root)
    index, diagnostics = build_index(root)
    report(diagnostics, sys.stderr)
    if any(level == ERROR for level, _ in diagnostics):
        print("index not written: fix the errors above", file=sys.stderr)
        return 1

    rendered = render(index)
    target = root / "index.json"
    if args.check:
        current = target.read_text(encoding="utf-8") if target.exists() else None
        if current != rendered:
            print("index.json is stale: run python3 scripts/build_persona_index.py and commit the result", file=sys.stderr)
            return 1
        print("index.json is up to date", file=sys.stderr)
        return 0

    target.write_text(rendered, encoding="utf-8")
    print(f"wrote index.json ({len(index['personas'])} personas, {len(index['teams'])} teams)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
