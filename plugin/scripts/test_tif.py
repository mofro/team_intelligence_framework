#!/usr/bin/env python3
"""Tests for tif.py. Run: python3 -m unittest discover -s plugin/scripts"""

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tif  # noqa: E402


def run(*argv, catalog=None):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = tif.main(list(argv), catalog=catalog)
    return code, out.getvalue(), err.getvalue()


def fake_catalog(personas, teams):
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name)
    (root / "index.json").write_text(json.dumps({"index_version": 1, "personas": personas, "teams": teams}))
    return tmp, root


def P(pid, domain="dev", status="complete", role="a role", aliases=(), **extra):
    d = {"id": pid, "name": f"{pid} name", "summary": f"{pid} summary", "role": role, "domain": domain,
         "subdomain": None, "version": "1.2", "status": status, "aliases": list(aliases)}
    d.update(extra)
    return d


def T(tid, members, status="complete", aliases=(), **extra):
    d = {"id": tid, "name": f"{tid} name", "summary": f"{tid} summary", "members": members, "status": status,
         "aliases": list(aliases), "domain": "dev", "default_primary": members[0], "unresolved_members": []}
    d.update(extra)
    return d


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


class ListTests(unittest.TestCase):
    def setUp(self):
        tmp, self.cat = fake_catalog(
            [P("alpha", "dev"), P("beta", "writing", "stub", "Beta role"), P("gamma", "dev")],
            [T("t1", ["alpha", "gamma"]), T("t2", ["alpha", "beta"], "contains_stubs")])
        self.addCleanup(tmp.cleanup)

    def lines(self, *argv):
        code, out, err = run(*argv, catalog=self.cat)
        return code, out.splitlines(), err

    def test_each_persona_once_in_index_order_with_fields(self):
        code, lines, _ = self.lines("list")
        self.assertEqual(code, 0)
        self.assertEqual(len(lines), 3)
        self.assertEqual([l.split()[0] for l in lines], ["alpha", "beta", "gamma"])
        self.assertIn("Beta role", lines[1])
        self.assertIn("writing", lines[1])

    def test_stub_is_marked_and_complete_is_not(self):
        _, lines, _ = self.lines("list")
        self.assertIn("stub", lines[1])
        self.assertNotIn("stub", lines[0])

    def test_domain_filter(self):
        code, lines, _ = self.lines("list", "--domain", "dev")
        self.assertEqual(code, 0)
        self.assertEqual([l.split()[0] for l in lines], ["alpha", "gamma"])

    def test_unknown_domain_lists_available_and_fails(self):
        code, lines, err = self.lines("list", "--domain", "nope")
        self.assertNotEqual(code, 0)
        self.assertEqual(lines, [])
        self.assertIn("nope", err)
        self.assertIn("dev", err)
        self.assertIn("writing", err)

    def test_teams_lists_each_with_count_and_status(self):
        code, lines, _ = self.lines("teams")
        self.assertEqual(code, 0)
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0].split(), ["t1", "2", "complete"])
        self.assertEqual(lines[1].split(), ["t2", "2", "contains_stubs"])

    def test_output_is_deterministic(self):
        self.assertEqual(run("list", catalog=self.cat), run("list", catalog=self.cat))

    def test_missing_catalog_is_a_clear_error(self):
        with tempfile.TemporaryDirectory() as empty:
            code, out, err = run("list", catalog=Path(empty))
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("index.json", err)


class InfoTests(unittest.TestCase):
    def setUp(self):
        tmp, self.cat = fake_catalog(
            [P("alpha", aliases=["alpha_file", "shared"], role="Alpha role", subdomain="sub"),
             P("beta", aliases=["shared"]),
             P("stubby", status="stub", aliases=["stubby_file"]),
             P("both")],
            [T("team_one", ["alpha", "ghost"], "incomplete", aliases=["team_file"], unresolved_members=["ghost"]),
             T("both", ["alpha"], aliases=[])])
        self.addCleanup(tmp.cleanup)

    def info(self, name):
        return run("info", name, catalog=self.cat)

    def test_persona_by_id_shows_the_required_fields(self):
        code, out, _ = self.info("alpha")
        self.assertEqual(code, 0)
        for text in ("alpha", "alpha summary", "Alpha role", "dev", "1.2", "complete"):
            self.assertIn(text, out)

    def test_persona_by_alias(self):
        code, out, _ = self.info("alpha_file")
        self.assertEqual(code, 0)
        self.assertIn("alpha summary", out)
        self.assertNotIn("beta summary", out)

    def test_stub_status_shown(self):
        self.assertIn("stub", self.info("stubby")[1])

    def test_team_shows_members_primary_status_and_unresolved(self):
        code, out, _ = self.info("team_one")
        self.assertEqual(code, 0)
        for text in ("team_one summary", "alpha", "ghost", "incomplete", "unresolved"):
            self.assertIn(text, out)
        self.assertIn("default primary", out.lower())

    def test_team_by_alias(self):
        self.assertIn("team_one summary", self.info("team_file")[1])

    def test_ambiguous_alias_lists_candidates_and_fails(self):
        code, out, err = self.info("shared")
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertIn("alpha", err)
        self.assertIn("beta", err)

    def test_id_shared_by_persona_and_team_is_ambiguous(self):
        code, out, err = self.info("both")
        self.assertNotEqual(code, 0)
        self.assertIn("persona", err)
        self.assertIn("team", err)

    def test_unknown_name_fails_and_points_to_listing(self):
        code, out, err = self.info("nonesuch")
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertIn("nonesuch", err)
        self.assertIn("list", err)

    def test_exact_id_wins_over_an_alias_of_another_item(self):
        tmp, cat = fake_catalog([P("x"), P("y", aliases=["x"])], [])
        self.addCleanup(tmp.cleanup)
        code, out, _ = run("info", "x", catalog=cat)
        self.assertEqual(code, 0)
        self.assertIn("x summary", out)


class RealCatalogTests(unittest.TestCase):
    """Facts about the bundled catalog on 2026-10-10 (28 personas, 6 teams)."""

    def test_list_has_every_persona_once_and_marks_stubs(self):
        code, out, _ = run("list")
        ids = [l.split()[0] for l in out.splitlines()]
        self.assertEqual((code, len(ids), len(set(ids))), (0, 28, 28))
        stubs = [l.split()[0] for l in out.splitlines() if "stub" in l]
        self.assertEqual(sorted(stubs), ["backend_developer", "data_scientist", "product_manager", "system_architect"])

    def test_teams_has_six_with_one_contains_stubs(self):
        code, out, _ = run("teams")
        self.assertEqual((code, len(out.splitlines())), (0, 6))
        self.assertEqual(sum("contains_stubs" in l for l in out.splitlines()), 1)

    def test_info_by_alias_on_real_catalog(self):
        code, out, _ = run("info", "ott_ux_persona")
        self.assertEqual(code, 0)
        self.assertIn("ux_designer", out)

    def test_info_on_team_with_stubs(self):
        code, out, _ = run("info", "intelligence_framework_team")
        self.assertEqual(code, 0)
        self.assertIn("contains_stubs", out)
        self.assertIn("system_architect", out)

    def test_domain_filter_on_real_catalog(self):
        _, out, _ = run("list", "--domain", "writing")
        self.assertTrue(out.splitlines())
        self.assertTrue(all("writing" in l for l in out.splitlines()))


if __name__ == "__main__":
    unittest.main()
