#!/usr/bin/env python3
"""tif: browse and install TIF personas and teams from the bundled catalog.

Run `tif.py help` for the subcommands. Standard library only.
"""

import argparse
import json
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
            (Arg("name", "persona or team id, or an alias"),
             Arg("force", "overwrite files that differ from the catalog", "flag"))),
)


def help_text():
    width = max(len(c.usage()) for c in COMMANDS)
    lines = ["Usage: tif.py <command> [arguments]", "", "Commands:"]
    lines += [f"  {c.usage():<{width}}  {c.description}" for c in COMMANDS]
    return "\n".join(lines) + "\n"


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


HANDLERS = {"list": cmd_list, "teams": cmd_teams, "info": cmd_info}


def main(argv=None, catalog=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv in (["help"], ["--help"]):
        sys.stdout.write(help_text())
        return 0
    try:
        ns = parse(argv)
    except ParseError as exc:
        print(f"tif.py: {exc}. Run 'tif.py help' for usage.", file=sys.stderr)
        return 2
    handler = HANDLERS.get(ns.command)
    if handler is None:
        print(f"tif.py: '{ns.command}' is not implemented yet.", file=sys.stderr)
        return 1
    try:
        index = load_index(DEFAULT_CATALOG if catalog is None else catalog)
    except CatalogError as exc:
        print(f"tif.py: {exc}", file=sys.stderr)
        return 1
    return handler(index, ns)


if __name__ == "__main__":
    sys.exit(main())
