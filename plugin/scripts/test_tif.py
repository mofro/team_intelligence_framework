#!/usr/bin/env python3
"""Tests for tif.py. Run: python3 -m unittest discover -s plugin/scripts"""

import contextlib
import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tif  # noqa: E402


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = tif.main(list(argv))
    return code, out.getvalue(), err.getvalue()


class HelpTests(unittest.TestCase):
    def test_help_and_flag_print_identical_text(self):
        c1, o1, _ = run("help")
        c2, o2, _ = run("--help")
        self.assertEqual((c1, c2), (0, 0))
        self.assertEqual(o1, o2)
        self.assertTrue(o1.strip())

    def test_no_arguments_prints_help(self):
        code, out, _ = run()
        self.assertEqual(code, 0)
        self.assertEqual(out, run("help")[1])

    def test_lists_every_subcommand_with_arguments_and_description(self):
        out = run("help")[1]
        for cmd in tif.COMMANDS:
            self.assertIn(cmd.usage(), out)
            self.assertIn(cmd.description, out)
        for name in ("help", "list", "teams", "info", "install"):
            self.assertIn(name, [c.name for c in tif.COMMANDS])

    def test_help_text_comes_from_table(self):
        self.assertEqual(run("help")[1], tif.help_text())


class ParseTests(unittest.TestCase):
    def parse(self, *argv):
        return tif.parse(list(argv))

    def test_list_domain(self):
        ns = self.parse("list", "--domain", "writing")
        self.assertEqual((ns.command, ns.domain), ("list", "writing"))

    def test_list_without_domain(self):
        self.assertIsNone(self.parse("list").domain)

    def test_teams(self):
        self.assertEqual(self.parse("teams").command, "teams")

    def test_info_name(self):
        ns = self.parse("info", "ux_designer")
        self.assertEqual((ns.command, ns.name), ("info", "ux_designer"))

    def test_install_force(self):
        ns = self.parse("install", "lore_keeper", "--force")
        self.assertEqual((ns.command, ns.name, ns.force), ("install", "lore_keeper", True))
        self.assertFalse(self.parse("install", "lore_keeper").force)

    def test_unknown_subcommand_exits_nonzero_with_hint(self):
        code, out, err = run("frobnicate")
        self.assertNotEqual(code, 0)
        self.assertIn("help", err)
        self.assertEqual(out, "")

    def test_missing_required_argument_exits_nonzero_with_hint(self):
        for argv in (("info",), ("install",)):
            code, _, err = run(*argv)
            self.assertNotEqual(code, 0, argv)
            self.assertIn("help", err)


if __name__ == "__main__":
    unittest.main()
