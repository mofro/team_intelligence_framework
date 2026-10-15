#!/usr/bin/env python3
"""Generate index.json: a catalog of the personas and teams in this repository.

Usage:
    python3 scripts/build_persona_index.py            # write index.json and the generated plugin files
    python3 scripts/build_persona_index.py --check    # exit 1 if any generated file is stale, or errors exist

The index is derived only from files under personas/. Persona, team and context
configuration files are never modified; the only paths written are index.json and
the generated plugin files: plugin/catalog/ (a byte-for-byte copy of index.json and every
file it lists), plugin/framework/ (copies of the framework files the plugin's challenge
commands read, plus domains.json derived from the domain-level context configurations) and
plugin/agents/challenger.md (the challenge phase prompt wrapped in agent front matter).
Specs: openspec/specs/; design: openspec/changes/archive/2026-10-10-persona-index/.
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

BUNDLE_DIR = "plugin/catalog"
FRAMEWORK_DIR = "plugin/framework"
AGENTS_DIR = "plugin/agents"

# Framework files copied byte for byte into plugin/framework/.
FRAMEWORK_SOURCES = (
    "config/challenge_phase_prompt.md",
    "config/persona_collaboration_framework_v2.md",
    "config/challenge_synthesis_protocol.md",
)
PHASE_PROMPT = "config/challenge_phase_prompt.md"
CHALLENGER_FRONT_MATTER = """---
name: challenger
description: Phase 1 of the challenge/synthesis protocol. Adversarially challenges a request and returns a Challenge Artifact. Use only via /tif:challenge. Read-only (no shell, write, web or agent tools), and it never sees the calling conversation.
tools: Read
---
"""

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
    unresolved = []
    for m in members:
        if m not in by_id and m not in unresolved:
            unresolved.append(m)
            diagnostics.append((WARNING, f"team '{tid}' ({rel}): member '{m}' has no persona file"))
    if primary not in by_id:
        if primary not in unresolved:
            unresolved.append(primary)
        diagnostics.append((WARNING, f"team '{tid}' ({rel}): default_primary '{primary}' has no persona file"))
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
        "unresolved_members": unresolved,
        "aliases": aliases,
        "path": rel,
        "bytes": len(raw),
        "sha256": sha256_of(raw),
        "status": "incomplete" if unresolved else ("contains_stubs" if has_stub else "complete"),
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
            diagnostics.append((NOTE, f"{rel}: available_teams '{value}' has no team file (treated as a virtual team)"))


def render(index):
    return json.dumps(index, indent=2, ensure_ascii=False) + "\n"


def bundle_contents(root, index, rendered):
    """Map of path (relative to plugin/catalog/) -> bytes for the bundled catalog."""
    files = {"index.json": rendered.encode("utf-8")}
    for entry in index["personas"] + index["teams"]:
        files[entry["path"]] = (root / entry["path"]).read_bytes()
    return files


def challenger_body(prompt_text):
    """The system prompt and output format, without the runtime-implementer notes."""
    start = prompt_text.index("You are operating in **Challenge Phase**")
    end = prompt_text.index("---\n\n## Notes for Runtime Implementers")
    return prompt_text[start:end].strip()


def domains_table(root, diagnostics):
    """Domain name (its directory, as in the index) -> challenge_focus and description, from personas/<domain>/context_configuration.json."""
    domains = {}
    for path in sorted((root / "personas").glob("*/context_configuration.json")):
        rel = path.relative_to(root).as_posix()
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            diagnostics.append((ERROR, f"{rel}: cannot parse as JSON ({exc})"))
            continue
        if not isinstance(obj, dict):
            diagnostics.append((ERROR, f"{rel}: not a JSON object"))
            continue
        name = path.parent.name
        declared = obj.get("context_name")
        if declared and declared != name:
            diagnostics.append((ERROR, f"{rel}: context_name '{declared}' differs from its directory '{name}'"))
            continue
        entry = {}
        protocols = obj.get("context_behavioral_protocols")
        focus = protocols.get("challenge_focus") if isinstance(protocols, dict) else None
        if focus:
            entry["challenge_focus"] = focus
        entry["description"] = obj.get("description") or ""
        domains[name] = entry
    return {"domains": domains}


def plugin_outputs(root, diagnostics):
    """[(directory, {relative path: bytes}, prune)] for the generated plugin files other than the catalog.

    `prune` is True when the directory holds only generated files, so extra files are errors.
    """
    framework, agents = {}, {}
    for rel in FRAMEWORK_SOURCES:
        src = root / rel
        if not src.is_file():
            diagnostics.append((ERROR, f"{rel}: missing; the plugin's framework files are copied from it"))
            continue
        framework[Path(rel).name] = src.read_bytes()
    framework["domains.json"] = json.dumps(domains_table(root, diagnostics), indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
    prompt = root / PHASE_PROMPT
    if prompt.is_file():
        body = challenger_body(prompt.read_text(encoding="utf-8"))
        agents["challenger.md"] = (CHALLENGER_FRONT_MATTER + "\n" + body + "\n").encode("utf-8")
    return [(FRAMEWORK_DIR, framework, True), (AGENTS_DIR, agents, False)]


def write_files(root, directory, files, prune=True):
    base = root / directory
    if prune and base.exists():
        for stale in sorted(base.rglob("*"), reverse=True):
            rel = stale.relative_to(base).as_posix()
            if stale.is_file() and rel not in files:
                stale.unlink()
            elif stale.is_dir() and not any(stale.iterdir()):
                stale.rmdir()
    for rel, data in files.items():
        dest = base / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists() or dest.read_bytes() != data:
            dest.write_bytes(data)


def file_problems(root, directory, files, prune=True):
    """Differences between the expected files and `directory` on disk."""
    base = root / directory
    problems = []
    for rel, data in sorted(files.items()):
        dest = base / rel
        if not dest.is_file():
            problems.append(f"{directory}/{rel} is missing")
        elif dest.read_bytes() != data:
            problems.append(f"{directory}/{rel} differs from its source")
    if prune and base.is_dir():
        for found in sorted(p for p in base.rglob("*") if p.is_file()):
            rel = found.relative_to(base).as_posix()
            if rel not in files:
                problems.append(f"{directory}/{rel} is not generated from any source")
    return problems


def report(diagnostics, stream):
    order = {ERROR: 0, WARNING: 1, NOTE: 2}
    for level, msg in sorted(diagnostics, key=lambda d: (order[d[0]], d[1])):
        print(f"{level.upper()}: {msg}", file=stream)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--check", action="store_true", help="do not write; exit 1 if a generated file is stale or errors exist")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent.parent), help="repository root")
    args = parser.parse_args(argv)

    root = Path(args.root)
    index, diagnostics = build_index(root)
    rendered = render(index)
    outputs = [(BUNDLE_DIR, bundle_contents(root, index, rendered), True)] + plugin_outputs(root, diagnostics)
    report(diagnostics, sys.stderr)
    if any(level == ERROR for level, _ in diagnostics):
        print("index not written: fix the errors above", file=sys.stderr)
        return 1

    target = root / "index.json"
    if args.check:
        regenerate = "run python3 scripts/build_persona_index.py and commit the result"
        status = 0
        current = target.read_text(encoding="utf-8") if target.exists() else None
        if current != rendered:
            print(f"index.json is stale: {regenerate}", file=sys.stderr)
            status = 1
        for directory, files, prune in outputs:
            problems = file_problems(root, directory, files, prune)
            for problem in problems:
                print(f"ERROR: {problem}", file=sys.stderr)
            if problems:
                print(f"{directory}/ is stale: {regenerate}", file=sys.stderr)
                status = 1
        if status == 0:
            print("index.json and " + ", ".join(f"{d}/" for d, _, _ in outputs) + " are up to date", file=sys.stderr)
        return status

    target.write_text(rendered, encoding="utf-8")
    for directory, files, prune in outputs:
        write_files(root, directory, files, prune)
    print(f"wrote index.json and " + ", ".join(f"{d}/" for d, _, _ in outputs)
          + f" ({len(index['personas'])} personas, {len(index['teams'])} teams)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
