#!/usr/bin/env python3
"""tif: browse and install TIF personas and teams from the bundled catalog.

Run `tif.py help` for the subcommands. Standard library only.
"""

import argparse
import sys
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


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv in (["help"], ["--help"]):
        sys.stdout.write(help_text())
        return 0
    try:
        ns = parse(argv)
    except ParseError as exc:
        print(f"tif.py: {exc}. Run 'tif.py help' for usage.", file=sys.stderr)
        return 2
    print(f"tif.py: '{ns.command}' is not implemented yet.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
