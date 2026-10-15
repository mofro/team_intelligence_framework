#!/usr/bin/env python3
"""tif: browse and install TIF personas and teams from the bundled catalog.

Run `tif.py help` for the subcommands. Standard library only.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Arg:
    """One argument of a subcommand. `flag` is a switch, `option` takes a value, otherwise positional."""
    name: str
    help: str = ""
    kind: str = "positional"  # positional | option | flag
    metavar: str = ""

    def usage(self):
        if self.kind == "positional":
            return f"<{self.name}>"
        if self.kind == "flag":
            return f"[--{self.name}]"
        return f"[--{self.name} {self.metavar or self.name.upper()}]"


@dataclass(frozen=True)
class Command:
    name: str
    description: str
    args: tuple = field(default_factory=tuple)

    def usage(self):
        return " ".join([self.name] + [a.usage() for a in self.args])


# The single source of the subcommand names, arguments and descriptions.
# --help, the SKILL.md help block and the README Quick Start are generated from it.
COMMANDS = (
    Command("help", "Show this help"),
    Command("list", "List personas with role, domain and status",
            (Arg("domain", "only personas in this domain", "option", "D"),)),
    Command("teams", "List teams with member count and status"),
    Command("info", "Show details for one persona or team, by id or alias",
            (Arg("name", "persona or team id, or an alias"),)),
    Command("install", "Copy a persona or team into .persona/ in the current project",
            (Arg("name", "persona or team id, or an alias"),)),
    Command("uninstall", "Remove an installed persona, or a team and its unshared members, from .persona/",
            (Arg("name", "persona or team id, or an alias"),)),
)


def help_text():
    width = max(len(c.usage()) for c in COMMANDS)
    lines = ["Usage: tif.py <command> [arguments]", "", "Commands:"]
    lines += [f"  {c.usage():<{width}}  {c.description}" for c in COMMANDS]
    return "\n".join(lines) + "\n"


PLUGIN_DIR = Path(__file__).resolve().parent.parent
FENCE = "```"


def quickstart_text():
    width = max(len(c.usage()) for c in COMMANDS)
    return "\n".join(f"/tif:catalog {c.usage():<{width}}  {c.description}" for c in COMMANDS) + "\n"


def doc_blocks(plugin_dir, readme):
    """(label, file, block name, generated content) for every block derived from the command table."""
    return [
        ("SKILL.md help block", Path(plugin_dir) / "skills" / "catalog" / "SKILL.md", "help", help_text()),
        ("README.md Quick Start block", Path(readme), "quickstart", quickstart_text()),
    ]


def _block_pattern(name):
    return re.compile(rf"(<!-- tif:{name}:start[^\n]*-->\n)(.*?)(<!-- tif:{name}:end -->)", re.DOTALL)


def _render(content):
    return f"{FENCE}text\n{content}{FENCE}\n"


def check_docs(plugin_dir, readme):
    problems = []
    for label, path, name, content in doc_blocks(plugin_dir, readme):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            problems.append(f"{path}: cannot read ({exc.strerror or exc}); expected the {label}")
            continue
        m = _block_pattern(name).search(text)
        if not m:
            problems.append(f"{path}: the {label} markers (tif:{name}:start / tif:{name}:end) are missing")
        elif m.group(2) != _render(content):
            problems.append(f"{path}: the {label} differs from the command table")
    return problems


def sync_docs(plugin_dir, readme):
    problems = check_docs(plugin_dir, readme)
    missing = [p for p in problems if "differs" not in p]
    if missing:
        return missing
    for label, path, name, content in doc_blocks(plugin_dir, readme):
        text = path.read_text(encoding="utf-8")
        new = _block_pattern(name).sub(lambda m: m.group(1) + _render(content) + m.group(3), text, count=1)
        if new != text:
            path.write_text(new, encoding="utf-8")
    return []


def run_docs(flag, plugin_dir, readme):
    if flag == "--check":
        problems = check_docs(plugin_dir, readme)
        action = "tif.py --check:"
    else:
        problems = sync_docs(plugin_dir, readme)
        action = "tif.py --sync:"
    for problem in problems:
        print(f"{action} {problem}", file=sys.stderr)
    if problems:
        if flag == "--check":
            print("fix: run python3 plugin/scripts/tif.py --sync and commit the result", file=sys.stderr)
        return 1
    print("docs are in sync with the command table" if flag == "--check" else "docs synced from the command table")
    return 0


class ParseError(Exception):
    pass


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ParseError(message)


def build_parser():
    parser = _Parser(prog="tif.py", add_help=False)
    sub = parser.add_subparsers(dest="command", parser_class=_Parser)
    for cmd in COMMANDS:
        p = sub.add_parser(cmd.name, add_help=False, prog=f"tif.py {cmd.name}")
        for a in cmd.args:
            if a.kind == "positional":
                p.add_argument(a.name, help=a.help)
            elif a.kind == "flag":
                p.add_argument(f"--{a.name}", action="store_true", help=a.help)
            else:
                p.add_argument(f"--{a.name}", default=None, metavar=a.metavar, help=a.help)
    return parser


def parse(argv):
    return build_parser().parse_args(argv)


DEFAULT_CATALOG = Path(__file__).resolve().parent.parent / "catalog"


class CatalogError(Exception):
    pass


def load_index(catalog):
    path = Path(catalog) / "index.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise CatalogError(f"cannot read the bundled catalog index {path}: {exc.strerror or exc}")
    except ValueError as exc:
        raise CatalogError(f"the bundled catalog index {path} is not valid JSON: {exc}")


def table(rows):
    """Left-aligned columns separated by two spaces; the last column is not padded."""
    if not rows:
        return []
    widths = [max(len(str(r[i])) for r in rows) for i in range(len(rows[0]) - 1)]
    return ["  ".join([str(c).ljust(w) for c, w in zip(r, widths)] + [str(r[-1])]) for r in rows]


def cmd_list(index, ns):
    personas = index["personas"]
    if ns.domain is not None:
        domains = sorted({p["domain"] for p in personas})
        personas = [p for p in personas if p["domain"] == ns.domain]
        if not personas:
            print(f"tif.py: no personas matched domain '{ns.domain}'. Available domains: {', '.join(domains)}",
                  file=sys.stderr)
            return 1
    for line in table([(p["id"], p["domain"], p["status"], p["role"]) for p in personas]):
        print(line)
    return 0


def cmd_teams(index, ns):
    for line in table([(t["id"], len(t["members"]), t["status"]) for t in index["teams"]]):
        print(line)
    return 0


def resolve(index, name):
    """Items matching `name`: exact id first, otherwise aliases. Each item is (kind, entry)."""
    items = [("persona", p) for p in index["personas"]] + [("team", t) for t in index["teams"]]
    by_id = [(k, e) for k, e in items if e["id"] == name]
    return by_id or [(k, e) for k, e in items if name in e["aliases"]]


def field_lines(pairs):
    width = max(len(k) for k, _ in pairs)
    return [f"{k + ':':<{width + 1}} {v}" for k, v in pairs]


def cmd_info(index, ns):
    matches = resolve(index, ns.name)
    if not matches:
        print(f"tif.py: no persona or team matches '{ns.name}'. Run 'tif.py list' or 'tif.py teams' to see what exists.",
              file=sys.stderr)
        return 1
    if len(matches) > 1:
        candidates = ", ".join(f"{e['id']} ({k})" for k, e in matches)
        print(f"tif.py: '{ns.name}' matches more than one item: {candidates}. Ask again with one of these ids.",
              file=sys.stderr)
        return 1
    kind, e = matches[0]
    if kind == "persona":
        domain = e["domain"] + (f"/{e['subdomain']}" if e.get("subdomain") else "")
        pairs = [("id", f"{e['id']} (persona)"), ("name", e["name"]), ("summary", e["summary"]),
                 ("role", e["role"]), ("domain", domain), ("version", e["version"]), ("status", e["status"])]
    else:
        pairs = [("id", f"{e['id']} (team)"), ("name", e["name"]), ("summary", e["summary"]),
                 ("domain", e["domain"]), ("members", ", ".join(e["members"])),
                 ("default primary", e["default_primary"]), ("status", e["status"])]
        if e["unresolved_members"]:
            pairs.append(("unresolved", ", ".join(e["unresolved_members"])))
    if e["aliases"]:
        pairs.append(("aliases", ", ".join(e["aliases"])))
    print("\n".join(field_lines(pairs)))
    return 0


PERSONAS_DIR = ".persona/personas"
TEAMS_DIR = ".persona/teams"


def copy_one(catalog, project, kind, entry):
    """Verify one catalog file against the index and copy it. Returns (outcome, path shown to the user)."""
    dest_dir = PERSONAS_DIR if kind == "persona" else TEAMS_DIR
    rel_dest = f"{dest_dir}/{Path(entry['path']).name}"
    try:
        data = (Path(catalog) / entry["path"]).read_bytes()
    except OSError as exc:
        return "unreadable", rel_dest, exc.strerror or str(exc)
    if hashlib.sha256(data).hexdigest() != entry["sha256"]:
        return "corrupt", rel_dest, "bundled file does not match the sha256 in the index"
    dest = Path(project) / rel_dest
    updating = dest.exists()
    if updating and dest.read_bytes() == data:
        return "already", rel_dest, ""
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return ("updated" if updating else "installed"), rel_dest, ""


def cmd_install(index, ns, catalog, project):
    matches = resolve(index, ns.name)
    if not matches:
        print(f"tif.py: no persona or team matches '{ns.name}'. Nothing was installed. "
              "Run 'tif.py list' or 'tif.py teams' to see what exists.", file=sys.stderr)
        return 1
    if len(matches) > 1:
        candidates = ", ".join(f"{e['id']} ({k})" for k, e in matches)
        print(f"tif.py: '{ns.name}' matches more than one item: {candidates}. Nothing was installed. "
              "Ask again with one of these ids.", file=sys.stderr)
        return 1

    kind, item = matches[0]
    by_id = {p["id"]: p for p in index["personas"]}
    personas = [by_id[m] for m in item["members"] if m in by_id] if kind == "team" else [item]
    work = [("persona", p) for p in personas] + ([("team", item)] if kind == "team" else [])

    failed = False
    for k, entry in work:
        outcome, shown, why = copy_one(catalog, project, k, entry)
        if outcome == "installed":
            print(f"installed          {shown}")
        elif outcome == "already":
            print(f"already installed  {shown}")
        elif outcome == "updated":
            print(f"updated            {shown} (replaced a file that differed from the catalog)")
        else:
            failed = True
            print(f"NOT COPIED         {shown}: {why}")

    stubs = [p["id"] for p in personas if p["status"] == "stub"]
    if stubs:
        noun = "persona" if len(stubs) == 1 else "personas"
        print(f"note: {len(stubs)} stub {noun} (placeholders, not yet fleshed out): {', '.join(stubs)}")
    if kind == "team":
        if item["unresolved_members"]:
            print(f"warning: no catalog file for team members: {', '.join(item['unresolved_members'])}")
        if item["default_primary"] not in by_id:
            print("!!! WARNING: PRIMARY VOICE MISSING !!!")
            print(f"!!! The team's default primary, '{item['default_primary']}', has no catalog file. "
                  "The team has no lead voice until you add that persona. !!!")
        print("note: team files are stored for later use and not yet read by Conductor.")
    return 1 if failed else 0


def _installed(project, kind, entry):
    return (Path(project) / (PERSONAS_DIR if kind == "persona" else TEAMS_DIR) / Path(entry["path"]).name)


def _installed_teams_listing(index, project, persona_id, skip=None):
    return [t["id"] for t in index["teams"]
            if t["id"] != skip and persona_id in t["members"] and _installed(project, "team", t).exists()]


def _remove_one(project, kind, entry):
    """Delete one installed file. Returns (outcome, path shown)."""
    dest = _installed(project, kind, entry)
    shown = f"{TEAMS_DIR if kind == 'team' else PERSONAS_DIR}/{dest.name}"
    if not dest.exists():
        return "absent", shown
    dest.unlink()
    return "removed", shown


def cmd_uninstall(index, ns, project):
    matches = resolve(index, ns.name)
    if not matches:
        print(f"tif.py: no persona or team matches '{ns.name}'. Nothing was removed. "
              "Run 'tif.py list' or 'tif.py teams' to see what exists.", file=sys.stderr)
        return 1
    if len(matches) > 1:
        candidates = ", ".join(f"{e['id']} ({k})" for k, e in matches)
        print(f"tif.py: '{ns.name}' matches more than one item: {candidates}. Nothing was removed. "
              "Ask again with one of these ids.", file=sys.stderr)
        return 1

    kind, item = matches[0]
    by_id = {p["id"]: p for p in index["personas"]}
    # Team: the team file first; members follow only when it was actually removed,
    # and only those that no other installed team lists.
    work, kept = [(kind, item)], []
    if kind == "team":
        outcome, shown = _remove_one(project, "team", item)
        work = []
        if outcome == "removed":
            print(f"removed           {shown}")
            for m in item["members"]:
                if m not in by_id:
                    continue
                others = _installed_teams_listing(index, project, m, skip=item["id"])
                if not others:
                    work.append(("persona", by_id[m]))
                elif _installed(project, "persona", by_id[m]).exists():
                    kept.append((by_id[m], others))
        else:
            print(f"not installed     {shown}")

    for k, entry in work:
        outcome, shown = _remove_one(project, k, entry)
        if outcome == "removed":
            print(f"removed           {shown}")
        elif k == kind:
            print(f"not installed     {shown}")
    for p, others in kept:
        print(f"kept              {PERSONAS_DIR}/{_installed(project, 'persona', p).name} "
              f"(also in installed teams: {', '.join(others)})")

    if kind == "persona":
        teams = _installed_teams_listing(index, project, item["id"])
        if teams:
            print(f"note: installed teams that list {item['id']}: {', '.join(teams)}")
    return 0


HANDLERS = {"list": cmd_list, "teams": cmd_teams, "info": cmd_info}


def main(argv=None, catalog=None, project=None, plugin_dir=None, readme=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv in (["help"], ["--help"]):
        sys.stdout.write(help_text())
        return 0
    if argv in (["--check"], ["--sync"]):
        plugin_dir = PLUGIN_DIR if plugin_dir is None else plugin_dir
        readme = PLUGIN_DIR.parent / "README.md" if readme is None else readme
        return run_docs(argv[0], plugin_dir, readme)
    try:
        ns = parse(argv)
    except ParseError as exc:
        print(f"tif.py: {exc}. Run 'tif.py help' for usage.", file=sys.stderr)
        return 2
    catalog = DEFAULT_CATALOG if catalog is None else catalog
    project = Path.cwd() if project is None else project
    try:
        index = load_index(catalog)
    except CatalogError as exc:
        print(f"tif.py: {exc}", file=sys.stderr)
        return 1
    if ns.command == "install":
        return cmd_install(index, ns, catalog, project)
    if ns.command == "uninstall":
        return cmd_uninstall(index, ns, project)
    return HANDLERS[ns.command](index, ns)


if __name__ == "__main__":
    sys.exit(main())
