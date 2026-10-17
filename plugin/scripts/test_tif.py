#!/usr/bin/env python3
"""Tests for tif.py. Run: python3 -m unittest discover -s plugin/scripts"""

import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tif  # noqa: E402


def run(*argv, catalog=None, project=None, framework=None):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = tif.main(list(argv), catalog=catalog, project=project, framework=framework)
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
        for name in ("help", "list", "teams", "info", "install", "resolve"):
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

    def test_install_takes_no_force_flag(self):
        with self.assertRaises(tif.ParseError):
            self.parse("install", "lore_keeper", "--force")

    def test_unknown_subcommand_exits_nonzero_with_hint(self):
        code, out, err = run("frobnicate")
        self.assertNotEqual(code, 0)
        self.assertIn("help", err)
        self.assertEqual(out, "")

    def test_bare_name_is_info(self):
        code, out, _ = run("ux_designer")
        code2, out2, _ = run("info", "ux_designer")
        self.assertEqual((code, out), (code2, out2))
        self.assertEqual(code, 0)

    def test_bare_name_with_extra_argument_is_usage_error(self):
        code, out, err = run("ux_designer", "extra")
        self.assertEqual(code, 2)
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


class CatalogFixture(unittest.TestCase):
    """A fake catalog directory and an empty project, shared by the install and uninstall tests."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.cat = Path(self._tmp.name) / "catalog"
        self.proj = Path(self._tmp.name) / "project"
        self.proj.mkdir()
        self.personas, self.teams = [], []

    def add_persona(self, pid, status="complete", body=None, **extra):
        rel = f"personas/dev/{pid}_persona.json"
        data = (body or f'{{"persona": "{pid}"}}').encode()
        (self.cat / rel).parent.mkdir(parents=True, exist_ok=True)
        (self.cat / rel).write_bytes(data)
        self.personas.append(P(pid, status=status, path=rel, sha256=hashlib.sha256(data).hexdigest(), **extra))

    def add_team(self, tid, members, primary=None, unresolved=(), status="complete", **extra):
        rel = f"personas/dev/teams/{tid}.json"
        data = f'{{"team": "{tid}"}}'.encode()
        (self.cat / rel).parent.mkdir(parents=True, exist_ok=True)
        (self.cat / rel).write_bytes(data)
        t = T(tid, list(members) + list(unresolved), status, path=rel, sha256=hashlib.sha256(data).hexdigest(),
              unresolved_members=list(unresolved), default_primary=primary or members[0], **extra)
        self.teams.append(t)

    def write_index(self):
        self.cat.mkdir(parents=True, exist_ok=True)
        (self.cat / "index.json").write_text(json.dumps(
            {"index_version": 1, "personas": self.personas, "teams": self.teams}))

    def install(self, *argv):
        self.write_index()
        return run("install", *argv, catalog=self.cat, project=self.proj)

    def files(self):
        base = self.proj / ".persona"
        return sorted(p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file()) if base.exists() else []



class InstallTests(CatalogFixture):
    """install copies files from a catalog directory into <project>/.persona/."""

    # -- targets
    def test_persona_installs_under_personas_and_names_the_path(self):
        self.add_persona("alpha")
        code, out, _ = self.install("alpha")
        self.assertEqual(code, 0)
        self.assertEqual(self.files(), ["personas/alpha_persona.json"])
        self.assertIn(".persona/personas/alpha_persona.json", out)
        self.assertEqual((self.proj / ".persona/personas/alpha_persona.json").read_bytes(),
                         (self.cat / "personas/dev/alpha_persona.json").read_bytes())

    def test_install_by_alias(self):
        self.add_persona("alpha", aliases=["alpha_file"])
        self.assertEqual(self.install("alpha_file")[0], 0)
        self.assertEqual(self.files(), ["personas/alpha_persona.json"])

    def test_team_installs_file_and_members(self):
        self.add_persona("alpha"); self.add_persona("beta"); self.add_persona("other")
        self.add_team("t", ["alpha", "beta"])
        code, out, _ = self.install("t")
        self.assertEqual(code, 0)
        self.assertEqual(self.files(), ["personas/alpha_persona.json", "personas/beta_persona.json", "teams/t.json"])

    def test_team_note_says_conductor_ignores_team_files(self):
        self.add_persona("alpha"); self.add_team("t", ["alpha"])
        out = self.install("t")[1]
        self.assertIn("Conductor", out)
        self.assertIn("not yet", out)

    def test_persona_install_has_no_team_note(self):
        self.add_persona("alpha")
        self.assertNotIn("Conductor", self.install("alpha")[1])

    # -- verification
    def test_corrupted_bundled_file_is_not_copied_and_fails(self):
        self.add_persona("alpha"); self.add_persona("beta")
        self.add_team("t", ["alpha", "beta"])
        (self.cat / "personas/dev/beta_persona.json").write_bytes(b"corrupt")
        code, out, err = self.install("t")
        self.assertNotEqual(code, 0)
        self.assertNotIn("personas/beta_persona.json", self.files())
        self.assertIn("beta_persona.json", out + err)
        self.assertIn("personas/alpha_persona.json", self.files())

    def test_missing_bundled_file_is_reported_and_fails(self):
        self.add_persona("alpha")
        (self.cat / "personas/dev/alpha_persona.json").unlink()
        code, out, err = self.install("alpha")
        self.assertNotEqual(code, 0)
        self.assertEqual(self.files(), [])
        self.assertIn("alpha_persona.json", out + err)

    # -- local edits
    def test_repeat_install_reports_already_installed_and_changes_nothing(self):
        self.add_persona("alpha")
        self.install("alpha")
        dest = self.proj / ".persona/personas/alpha_persona.json"
        before = dest.stat().st_mtime_ns
        code, out, _ = self.install("alpha")
        self.assertEqual(code, 0)
        self.assertIn("already installed", out)
        self.assertEqual(dest.stat().st_mtime_ns, before)

    def test_file_that_differs_is_replaced_and_reported_as_updated(self):
        self.add_persona("alpha")
        self.install("alpha")
        dest = self.proj / ".persona/personas/alpha_persona.json"
        dest.write_text("older copy")
        code, out, _ = self.install("alpha")
        self.assertEqual(code, 0)
        self.assertEqual(dest.read_bytes(), (self.cat / "personas/dev/alpha_persona.json").read_bytes())
        self.assertIn("updated", out)
        self.assertNotIn("already installed", out)

    # -- disclosure, never refusing
    def test_team_with_stubs_installs_and_names_them(self):
        self.add_persona("alpha"); self.add_persona("s1", status="stub"); self.add_persona("s2", status="stub")
        self.add_team("t", ["alpha", "s1", "s2"], status="contains_stubs")
        code, out, _ = self.install("t")
        self.assertEqual(code, 0)
        self.assertIn("2 stub", out)
        self.assertIn("s1", out)
        self.assertIn("s2", out)
        self.assertEqual(len(self.files()), 4)

    def test_persona_stub_is_disclosed(self):
        self.add_persona("s1", status="stub")
        code, out, _ = self.install("s1")
        self.assertEqual(code, 0)
        self.assertIn("1 stub", out)

    def test_no_stub_line_when_there_are_none(self):
        self.add_persona("alpha")
        self.assertNotIn("stub", self.install("alpha")[1].lower())

    def test_unresolved_members_named_and_install_completes(self):
        self.add_persona("alpha"); self.add_persona("beta")
        self.add_team("t", ["alpha", "beta"], unresolved=["ghost"], status="incomplete")
        code, out, _ = self.install("t")
        self.assertEqual(code, 0)
        self.assertIn("ghost", out)
        self.assertIn("teams/t.json", self.files())

    def test_missing_primary_voice_gets_a_distinct_warning_and_completes(self):
        self.add_persona("alpha")
        self.add_team("t", ["alpha"], primary="ghost", unresolved=["ghost"], status="incomplete")
        code, out, _ = self.install("t")
        self.assertEqual(code, 0)
        self.assertIn("PRIMARY VOICE MISSING", out)
        self.assertIn("ghost", out)
        self.assertIn("teams/t.json", self.files())

    def test_no_primary_warning_when_primary_present(self):
        self.add_persona("alpha"); self.add_team("t", ["alpha"])
        self.assertNotIn("PRIMARY", self.install("t")[1])

    # -- unknown / ambiguous
    def test_unknown_name_writes_nothing_and_fails(self):
        self.add_persona("alpha")
        code, out, err = self.install("nonesuch")
        self.assertNotEqual(code, 0)
        self.assertEqual(self.files(), [])
        self.assertFalse((self.proj / ".persona").exists())
        self.assertIn("nonesuch", err)

    def test_ambiguous_alias_lists_candidates_and_writes_nothing(self):
        self.add_persona("alpha", aliases=["shared"]); self.add_persona("beta", aliases=["shared"])
        code, out, err = self.install("shared")
        self.assertNotEqual(code, 0)
        self.assertEqual(self.files(), [])
        self.assertIn("alpha", err)
        self.assertIn("beta", err)


class UninstallTests(CatalogFixture):
    """uninstall removes installed files; it keeps no state beyond the files and the catalog."""

    def install(self, *argv):
        self.write_index()
        return run("install", *argv, catalog=self.cat, project=self.proj)

    def uninstall(self, *argv):
        self.write_index()
        return run("uninstall", *argv, catalog=self.cat, project=self.proj)

    def test_persona_removed_and_path_named(self):
        self.add_persona("alpha"); self.add_persona("beta")
        self.install("alpha"); self.install("beta")
        code, out, _ = self.uninstall("alpha")
        self.assertEqual(code, 0)
        self.assertEqual(self.files(), ["personas/beta_persona.json"])
        self.assertIn(".persona/personas/alpha_persona.json", out)

    def test_team_uninstall_removes_team_and_members_no_other_team_lists(self):
        self.add_persona("alpha"); self.add_persona("beta"); self.add_team("t", ["alpha", "beta"])
        self.install("t")
        code, out, _ = self.uninstall("t")
        self.assertEqual(code, 0)
        self.assertEqual(self.files(), [])
        self.assertNotIn("kept", out)

    def test_team_uninstall_keeps_members_shared_with_another_installed_team(self):
        self.add_persona("alpha"); self.add_persona("beta")
        self.add_team("t", ["alpha", "beta"]); self.add_team("u", ["alpha"])
        self.install("t"); self.install("u")
        code, out, _ = self.uninstall("t")
        self.assertEqual(code, 0)
        self.assertEqual(self.files(), ["personas/alpha_persona.json", "teams/u.json"])
        self.assertRegex(out, r"kept .*alpha_persona\.json.*also in installed teams: u")

    def test_shared_member_is_removed_once_the_last_team_goes(self):
        self.add_persona("alpha"); self.add_team("t", ["alpha"]); self.add_team("u", ["alpha"])
        self.install("t"); self.install("u")
        self.uninstall("t")
        self.uninstall("u")
        self.assertEqual(self.files(), [])

    def test_members_that_differ_from_the_catalog_are_removed_with_the_team(self):
        self.add_persona("alpha"); self.add_team("t", ["alpha"])
        self.install("t")
        (self.proj / ".persona/personas/alpha_persona.json").write_text("{}")
        self.uninstall("t")
        self.assertEqual(self.files(), [])

    def test_team_not_installed_removes_nothing_else(self):
        self.add_persona("alpha"); self.add_team("t", ["alpha"])
        self.install("alpha")
        code, out, _ = self.uninstall("t")
        self.assertEqual(code, 0)
        self.assertEqual(self.files(), ["personas/alpha_persona.json"])

    def test_persona_uninstall_names_installed_teams_that_list_it(self):
        self.add_persona("alpha"); self.add_team("t", ["alpha"]); self.add_team("u", ["alpha"])
        self.install("t")
        code, out, _ = self.uninstall("alpha")
        self.assertEqual(code, 0)
        self.assertIn("installed teams that list alpha: t", out)
        self.assertEqual(self.files(), ["teams/t.json"])

    def test_file_that_differs_from_the_catalog_is_still_removed(self):
        self.add_persona("alpha")
        self.install("alpha")
        f = self.proj / ".persona/personas/alpha_persona.json"
        f.write_text('{"older or edited": true}')
        self.assertEqual(self.uninstall("alpha")[0], 0)
        self.assertFalse(f.exists())

    def test_repeat_uninstall_is_a_no_op(self):
        self.add_persona("alpha")
        self.install("alpha")
        self.uninstall("alpha")
        code, out, _ = self.uninstall("alpha")
        self.assertEqual(code, 0)
        self.assertIn("not installed", out)
        self.assertEqual(self.files(), [])

    def test_unknown_ambiguous_and_virtual_names_delete_nothing(self):
        self.add_persona("alpha", aliases=["x"]); self.add_persona("beta", aliases=["x"])
        self.install("alpha")
        for name in ("nonsense", "x", "security_review_team"):
            code, _, err = self.uninstall(name)
            self.assertEqual(code, 1, name)
            self.assertTrue(err)
        self.assertEqual(self.files(), ["personas/alpha_persona.json"])

    def test_unrelated_files_untouched(self):
        self.add_persona("alpha")
        self.install("alpha")
        other = self.proj / ".persona/personas/mine_persona.json"
        other.write_text("{}")
        self.uninstall("alpha")
        self.assertTrue(other.exists())

    def test_uninstall_does_not_need_catalog_files(self):
        self.add_persona("alpha")
        self.install("alpha")
        (self.cat / "personas/dev/alpha_persona.json").unlink()
        self.assertEqual(self.uninstall("alpha")[0], 0)
        self.assertEqual(self.files(), [])


class ResolveTests(unittest.TestCase):
    DOMAINS = {"domains": {
        "gaming": {"challenge_focus": "narrative_goals", "description": "games"},
        "writing": {"challenge_focus": "story_goals", "description": "words"},
        "bare": {"description": "no focus declared"}}}

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.project = Path(tmp.name) / "proj"
        self.project.mkdir()
        self.framework = Path(tmp.name) / "framework"
        self.framework.mkdir()
        (self.framework / "domains.json").write_text(json.dumps(self.DOMAINS))

    def context(self, text):
        (self.project / ".persona").mkdir(exist_ok=True)
        (self.project / ".persona" / "context.md").write_text(text)

    def persona(self, name, role="a role", expertise=("x", "y"), raw=None):
        d = self.project / ".persona" / "personas"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{name}.json").write_text(raw if raw is not None else json.dumps(
            {"persona": {"persona_name": name, "role": role, "expertise": list(expertise)}}))

    def resolve(self, *argv):
        return run("resolve", *argv, project=self.project, framework=self.framework)

    def lens(self, out):
        lines = out.splitlines()
        return lines[0].removeprefix("LENS: "), lines[1].removeprefix("LENS SOURCE: ")

    def test_nothing_available_uses_first_principles_and_says_so(self):
        code, out, _ = self.resolve()
        self.assertEqual(code, 0)
        lens, source = self.lens(out)
        self.assertEqual(lens, "correctness, completeness, and coherence")
        self.assertIn("first principles", source)
        self.assertIn("NOTE: no project context found", out)
        self.assertIn("NOTE: no personas installed", out)

    def test_focus_flag_overrides_context_focus_and_domain(self):
        self.context("---\nfocus: from file\ndomain: gaming\n---\nbody")
        lens, source = self.lens(self.resolve("--focus", "mine", "--domain", "writing")[1])
        self.assertEqual((lens, source), ("mine", "--focus"))

    def test_context_focus_beats_domain_flag(self):
        self.context("---\nfocus: from file\n---\nbody")
        lens, source = self.lens(self.resolve("--domain", "writing")[1])
        self.assertEqual(lens, "from file")
        self.assertIn("focus in .persona/context.md", source)

    def test_domain_flag_beats_context_domain(self):
        self.context("---\ndomain: gaming\n---\nbody")
        lens, source = self.lens(self.resolve("--domain", "writing")[1])
        self.assertEqual((lens, source), ("story_goals", "--domain (writing)"))

    def test_domain_from_context_file(self):
        self.context("---\ndomain: gaming\n---\nbody")
        lens, source = self.lens(self.resolve()[1])
        self.assertEqual(lens, "narrative_goals")
        self.assertIn("domain in .persona/context.md (gaming)", source)

    def test_sources_are_never_combined(self):
        self.context("---\nfocus: from file\ndomain: gaming\n---\nbody")
        out = self.resolve()[1]
        self.assertNotIn("narrative_goals", out)

    def test_domain_without_focus_is_reported_and_falls_through(self):
        self.context("---\ndomain: gaming\n---\nbody")
        lens, source = self.lens(self.resolve("--domain", "bare")[1])
        self.assertEqual(lens, "narrative_goals")
        self.assertIn("domain 'bare' from --domain has no challenge_focus", self.resolve("--domain", "bare")[1])

    def test_domain_without_focus_and_nothing_else_is_first_principles(self):
        code, out, _ = self.resolve("--domain", "bare")
        self.assertEqual(code, 0)
        self.assertIn("first principles", self.lens(out)[1])
        self.assertIn("has no challenge_focus", out)

    def test_unknown_domain_flag_is_error_listing_names(self):
        code, out, err = self.resolve("--domain", "nonsense")
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        for name in ("bare", "gaming", "writing"):
            self.assertIn(name, err)

    def test_unknown_domain_in_context_file_is_error_even_if_focus_flag_wins(self):
        self.context("---\ndomain: nonsense\n---\nbody")
        code, _, err = self.resolve("--focus", "mine")
        self.assertEqual(code, 1)
        self.assertIn("nonsense", err)
        self.assertIn("gaming", err)

    def test_project_facts_printed_without_front_matter(self):
        self.context("---\ndomain: gaming\n---\n# Goal\nShip the thing.\n")
        out = self.resolve()[1]
        self.assertIn("=== PROJECT CONTEXT ===\n# Goal\nShip the thing.", out)
        self.assertNotIn("domain: gaming", out)

    def test_context_without_front_matter_is_all_facts(self):
        self.context("# Goal\nJust facts.\n")
        out = self.resolve()[1]
        self.assertIn("Just facts.", out)
        self.assertIn("first principles", self.lens(out)[1])

    def test_hand_edit_is_used_next_time(self):
        self.context("# Goal\nfirst")
        self.assertIn("first", self.resolve()[1])
        self.context("# Goal\nsecond")
        self.assertIn("second", self.resolve()[1])

    def test_empty_context_file_is_reported_not_an_error(self):
        self.context("")
        code, out, _ = self.resolve()
        self.assertEqual(code, 0)
        self.assertIn("NOTE: .persona/context.md is empty", out)

    def test_unclosed_front_matter_is_error(self):
        self.context("---\ndomain: gaming\nbody")
        code, _, err = self.resolve()
        self.assertEqual(code, 1)
        self.assertIn("never closed", err)

    def test_front_matter_line_without_colon_is_error(self):
        self.context("---\njust words\n---\nbody")
        code, _, err = self.resolve()
        self.assertEqual(code, 1)
        self.assertIn("line 2", err)

    def test_quoted_values_and_unknown_keys(self):
        self.context("---\nfocus: \"quoted lens\"\nowner: me\n---\nbody")
        self.assertEqual(self.lens(self.resolve()[1])[0], "quoted lens")

    def test_persona_digest(self):
        self.persona("zed", role="Last one", expertise=("a",))
        self.persona("amy", role="First one", expertise=("b", "c"))
        out = self.resolve()[1]
        self.assertIn("=== ACTIVE PERSONAS ===\n- amy: First one (expertise: b, c)\n- zed: Last one (expertise: a)", out)
        self.assertNotIn("no personas installed", out)

    def test_unreadable_persona_file_is_skipped_and_reported(self):
        self.persona("good")
        self.persona("bad", raw="{nope")
        code, out, _ = self.resolve()
        self.assertEqual(code, 0)
        self.assertIn("- good:", out)
        self.assertIn("NOTE: skipped .persona/personas/bad.json", out)

    def test_empty_personas_directory(self):
        (self.project / ".persona" / "personas").mkdir(parents=True)
        out = self.resolve()[1]
        self.assertIn("NOTE: no personas installed", out)
        self.assertIn("=== ACTIVE PERSONAS ===\n(none)", out)

    def test_resolve_writes_nothing(self):
        self.context("# Goal\nx")
        self.persona("amy")
        before = {p: p.read_bytes() for p in self.project.rglob("*") if p.is_file()}
        self.resolve()
        self.assertEqual({p: p.read_bytes() for p in self.project.rglob("*") if p.is_file()}, before)

    def test_missing_domain_table_is_error(self):
        (self.framework / "domains.json").unlink()
        code, _, err = self.resolve()
        self.assertEqual(code, 1)
        self.assertIn("domain table", err)

    def test_takes_no_positional_argument(self):
        self.assertEqual(self.resolve("extra")[0], 2)


class DocBlockTests(unittest.TestCase):
    """--check compares generated help blocks in SKILL.md and README.md with the command table."""

    SKILL_BODY = "# skill\n\nintro\n\n<!-- tif:help:start (generated) -->\nold\n<!-- tif:help:end -->\n\ntail\n"
    README_BODY = "# readme\n\n<!-- tif:quickstart:start (generated) -->\nold\n<!-- tif:quickstart:end -->\n\nmore\n"

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        root = Path(self._tmp.name)
        self.plugin = root / "plugin"
        self.skill = self.plugin / "skills" / "catalog" / "SKILL.md"
        self.readme = root / "README.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text(self.SKILL_BODY)
        self.readme.write_text(self.README_BODY)

    def doc(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = tif.main(list(argv), plugin_dir=self.plugin, readme=self.readme)
        return code, out.getvalue(), err.getvalue()

    def synced(self):
        self.assertEqual(self.doc("--sync")[0], 0)

    def test_check_fails_before_sync_and_passes_after(self):
        self.assertEqual(self.doc("--check")[0], 1)
        self.synced()
        self.assertEqual(self.doc("--check")[0], 0)

    def test_sync_replaces_only_the_block_and_embeds_the_table(self):
        self.synced()
        text = self.skill.read_text()
        self.assertTrue(text.startswith("# skill\n\nintro\n\n<!-- tif:help:start"))
        self.assertTrue(text.endswith("<!-- tif:help:end -->\n\ntail\n"))
        for cmd in tif.COMMANDS:
            self.assertIn(cmd.usage(), text)
            self.assertIn(cmd.description, text)
        quick = self.readme.read_text()
        self.assertIn("/tif:catalog list [--domain D]", quick)
        self.assertTrue(quick.endswith("<!-- tif:quickstart:end -->\n\nmore\n"))

    def test_sync_is_idempotent(self):
        self.synced()
        first = (self.skill.read_text(), self.readme.read_text())
        self.synced()
        self.assertEqual((self.skill.read_text(), self.readme.read_text()), first)

    def test_hand_edited_skill_block_fails_and_names_the_file(self):
        self.synced()
        self.skill.write_text(self.skill.read_text().replace("Show this help", "Show some help"))
        code, _, err = self.doc("--check")
        self.assertEqual(code, 1)
        self.assertIn("SKILL.md", err)
        self.assertIn("--sync", err)

    def test_hand_edited_readme_block_fails_and_names_the_file(self):
        self.synced()
        self.readme.write_text(self.readme.read_text().replace("/tif:catalog teams", "/tif:catalog TEAMS"))
        code, _, err = self.doc("--check")
        self.assertEqual(code, 1)
        self.assertIn("README.md", err)

    def test_text_outside_the_blocks_may_change_freely(self):
        self.synced()
        self.skill.write_text(self.skill.read_text().replace("intro", "different intro"))
        self.assertEqual(self.doc("--check")[0], 0)

    def test_missing_markers_fail_check_and_sync(self):
        self.skill.write_text("# no markers\n")
        self.assertEqual(self.doc("--check")[0], 1)
        code, _, err = self.doc("--sync")
        self.assertEqual(code, 1)
        self.assertIn("SKILL.md", err)
        self.assertEqual(self.skill.read_text(), "# no markers\n")

    def test_missing_file_fails(self):
        self.readme.unlink()
        code, _, err = self.doc("--check")
        self.assertEqual(code, 1)
        self.assertIn("README.md", err)

    def test_check_writes_nothing(self):
        before = (self.skill.read_text(), self.readme.read_text())
        self.doc("--check")
        self.assertEqual((self.skill.read_text(), self.readme.read_text()), before)


class RealFrameworkTests(unittest.TestCase):
    def test_bundled_domain_table_resolves_every_domain(self):
        domains = tif.load_domains(tif.DEFAULT_FRAMEWORK)
        self.assertTrue(domains)
        for name, entry in domains.items():
            with tempfile.TemporaryDirectory() as proj:
                code, out, err = run("resolve", "--domain", name, project=Path(proj))
                self.assertEqual(code, 0, (name, err))
                if entry.get("challenge_focus"):
                    self.assertIn(f"LENS: {entry['challenge_focus']}", out)


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

    def test_virtual_team_name_is_unknown_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as proj:
            code, out, err = run("install", "security_review_team", project=Path(proj))
            self.assertNotEqual(code, 0)
            self.assertEqual(out, "")
            self.assertIn("security_review_team", err)
            self.assertFalse(Path(proj, ".persona").exists())

    def test_install_every_real_item_into_a_clean_project(self):
        index = json.loads((tif.DEFAULT_CATALOG / "index.json").read_text())
        for item in index["personas"] + index["teams"]:
            with tempfile.TemporaryDirectory() as proj:
                code, out, err = run("install", item["id"], project=Path(proj))
                self.assertEqual(code, 0, (item["id"], err))
                self.assertTrue(any(Path(proj, ".persona").rglob("*.json")), item["id"])

    def test_domain_filter_on_real_catalog(self):
        _, out, _ = run("list", "--domain", "writing")
        self.assertTrue(out.splitlines())
        self.assertTrue(all("writing" in l for l in out.splitlines()))


if __name__ == "__main__":
    unittest.main()
