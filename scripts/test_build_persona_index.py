#!/usr/bin/env python3
"""Tests for build_persona_index.py. Run: python3 -m unittest discover -s scripts"""

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_persona_index as bpi  # noqa: E402

REPO = Path(__file__).resolve().parent.parent


def persona(pid, **extra):
    d = {
        "schema_version": "1.2",
        "metadata": {"name": f"{pid} name", "description": f"{pid} desc", "version": "1.0"},
        "persona": {"persona_name": pid, "role": f"{pid} role", "expertise": ["a", "b"], "custom_name": None},
    }
    d.update(extra)
    return d


def team(tid, members, primary=None):
    return {"team": {"team_name": tid, "display_name": tid, "description": f"{tid} desc",
                     "members": members, "default_primary": primary or members[0]}}


PROMPT_TEXT = ("# Prompt\n\nYou are operating in **Challenge Phase** of a protocol.\n\n"
               "## Output Format\n\nformat\n\n---\n\n## Notes for Runtime Implementers\n\nnotes\n")
FRAMEWORK_TEXT = {rel: (PROMPT_TEXT if rel == bpi.PHASE_PROMPT else f"# {rel}\n") for rel in bpi.FRAMEWORK_SOURCES}


class Fixture:
    def __init__(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        for rel in bpi.FRAMEWORK_SOURCES:
            self.write(rel, FRAMEWORK_TEXT[rel])

    def write(self, rel, obj):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(obj if isinstance(obj, str) else json.dumps(obj), encoding="utf-8")

    def build(self):
        return bpi.build_index(self.root)

    def close(self):
        self._tmp.cleanup()


def levels(diags, level):
    return [m for lv, m in diags if lv == level]


class FixtureTests(unittest.TestCase):
    def setUp(self):
        self.f = Fixture()
        self.addCleanup(self.f.close)

    def test_template_and_examples_excluded(self):
        self.f.write("personas/persona_schema_example.json", persona("tmpl"))
        self.f.write("personas/examples/notjson.json", "# markdown, not json")
        self.f.write("personas/dev/a_persona_schema.json", persona("a"))
        index, diags = self.f.build()
        self.assertEqual([e["id"] for e in index["personas"]], ["a"])
        self.assertEqual(levels(diags, bpi.ERROR), [])

    def test_unparseable_persona_outside_examples_is_error(self):
        self.f.write("personas/dev/broken.json", "{not json")
        _, diags = self.f.build()
        self.assertTrue(any("broken.json" in m for m in levels(diags, bpi.ERROR)))

    def test_missing_optional_fields_still_indexed(self):
        self.f.write("personas/dev/a.json", persona("a"))  # custom_name null, no reference_libraries
        index, diags = self.f.build()
        self.assertEqual(len(index["personas"]), 1)
        self.assertEqual(levels(diags, bpi.ERROR), [])

    def test_missing_required_field_is_error(self):
        bad = persona("a")
        del bad["persona"]["role"]
        self.f.write("personas/dev/a.json", bad)
        index, diags = self.f.build()
        self.assertEqual(index["personas"], [])
        self.assertTrue(any("persona.role" in m for m in levels(diags, bpi.ERROR)))

    def test_domain_and_subdomain_from_path(self):
        self.f.write("personas/writing/screenplays/dp_persona_schema.json", persona("dp"))
        self.f.write("personas/financial/x.json", persona("x"))
        index, _ = self.f.build()
        by = {e["id"]: e for e in index["personas"]}
        self.assertEqual((by["dp"]["domain"], by["dp"]["subdomain"]), ("writing", "screenplays"))
        self.assertEqual((by["x"]["domain"], by["x"]["subdomain"]), ("financial", None))

    def test_hash_and_bytes_match_file(self):
        self.f.write("personas/dev/a.json", persona("a"))
        index, _ = self.f.build()
        e = index["personas"][0]
        raw = (self.f.root / e["path"]).read_bytes()
        self.assertEqual(e["sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(e["bytes"], len(raw))

    def test_duplicate_persona_id_is_error(self):
        self.f.write("personas/dev/a.json", persona("same"))
        self.f.write("personas/dev/b.json", persona("same"))
        _, diags = self.f.build()
        self.assertTrue(any("duplicate persona id" in m for m in levels(diags, bpi.ERROR)))

    def test_alias_derivation(self):
        self.assertEqual(bpi.derive_aliases("personas/d/ott_ux_persona_schema_v1.1.json"),
                         ["ott_ux_persona_schema_v1.1", "ott_ux_persona_schema", "ott_ux_persona", "ott_ux"])
        self.assertEqual(bpi.derive_aliases("personas/d/10_foot_ui_designer_persona_schema_v1.1.json")[-1], "10_foot_ui_designer")
        self.assertEqual(bpi.derive_aliases("personas/d/plain.json"), ["plain"])

    def test_alias_collision_between_personas_is_error(self):
        self.f.write("personas/dev/shared_persona_schema.json", persona("p1"))
        self.f.write("personas/ops/shared_persona_schema_v2.json", persona("p2"))
        _, diags = self.f.build()
        self.assertTrue(any("maps to both" in m for m in levels(diags, bpi.ERROR)))

    def test_alias_equal_to_other_personas_id_is_error(self):
        self.f.write("personas/dev/other.json", persona("other"))
        self.f.write("personas/dev/other_persona_schema.json", persona("p2"))  # alias 'other' == id of persona 'other'
        _, diags = self.f.build()
        self.assertTrue(any("equals the id of a different persona" in m for m in levels(diags, bpi.ERROR)))

    def test_team_resolution_and_aliases(self):
        self.f.write("personas/dev/a.json", persona("a"))
        self.f.write("personas/dev/b.json", persona("b"))
        self.f.write("personas/dev/teams/fullstack_team.json", team("fullstack_development_team", ["a", "b"]))
        index, diags = self.f.build()
        t = index["teams"][0]
        self.assertEqual(t["members"], ["a", "b"])
        self.assertEqual(t["aliases"], ["fullstack_team"])
        self.assertEqual(t["status"], "complete")
        self.assertEqual(t["domain"], "dev")
        self.assertEqual(levels(diags, bpi.ERROR), [])

    def test_team_missing_member_is_warning_and_incomplete(self):
        self.f.write("personas/dev/a.json", persona("a"))
        self.f.write("personas/dev/teams/t.json", team("my_team", ["a", "ghost"], primary="a"))
        index, diags = self.f.build()
        self.assertEqual(levels(diags, bpi.ERROR), [])
        self.assertTrue(any("my_team" in m and "ghost" in m for m in levels(diags, bpi.WARNING)))
        t = index["teams"][0]
        self.assertEqual(t["status"], "incomplete")
        self.assertEqual(t["unresolved_members"], ["ghost"])
        self.assertEqual(t["members"], ["a", "ghost"])

    def test_team_missing_default_primary_is_warning_and_incomplete(self):
        self.f.write("personas/dev/a.json", persona("a"))
        self.f.write("personas/dev/teams/t.json", team("my_team", ["a"], primary="ghost"))
        index, diags = self.f.build()
        self.assertEqual(levels(diags, bpi.ERROR), [])
        self.assertTrue(any("default_primary 'ghost'" in m for m in levels(diags, bpi.WARNING)))
        self.assertEqual(index["teams"][0]["unresolved_members"], ["ghost"])
        self.assertEqual(index["teams"][0]["status"], "incomplete")

    def test_incomplete_takes_precedence_over_contains_stubs(self):
        self.f.write("personas/dev/s.json", persona("s", stub=True))
        self.f.write("personas/dev/teams/t.json", team("my_team", ["s", "ghost"], primary="s"))
        self.assertEqual(self.f.build()[0]["teams"][0]["status"], "incomplete")

    def test_complete_team_has_no_unresolved_members(self):
        self.f.write("personas/dev/a.json", persona("a"))
        self.f.write("personas/dev/teams/t.json", team("my_team", ["a"]))
        t = self.f.build()[0]["teams"][0]
        self.assertEqual((t["status"], t["unresolved_members"]), ("complete", []))

    def test_team_with_stub_member_flagged(self):
        self.f.write("personas/dev/a.json", persona("a"))
        self.f.write("personas/dev/s.json", persona("s", stub=True))
        self.f.write("personas/dev/teams/t.json", team("my_team", ["a", "s"]))
        index, _ = self.f.build()
        self.assertEqual({e["id"]: e["status"] for e in index["personas"]}, {"a": "complete", "s": "stub"})
        self.assertEqual(index["teams"][0]["status"], "contains_stubs")

    def test_stub_completion_changes_status(self):
        self.f.write("personas/dev/s.json", persona("s", stub=True))
        self.assertEqual(self.f.build()[0]["personas"][0]["status"], "stub")
        self.f.write("personas/dev/s.json", persona("s"))
        self.assertEqual(self.f.build()[0]["personas"][0]["status"], "complete")

    def test_context_config_notes_and_warnings_never_fail(self):
        self.f.write("personas/dev/real_persona_schema.json", persona("real"))
        self.f.write("personas/dev/context_configuration.json", {
            "available_personas": ["real", "real_persona", "nobody"],
            "always_on_personas": ["real_persona"],
            "default_primary_persona": "real",
            "available_teams": ["no_such_team"]})
        before = (self.f.root / "personas/dev/context_configuration.json").read_bytes()
        index, diags = self.f.build()
        self.assertEqual(levels(diags, bpi.ERROR), [])
        self.assertTrue(any("'real_persona' resolves via alias to 'real'" in m for m in levels(diags, bpi.NOTE)))
        self.assertTrue(any("'nobody'" in m for m in levels(diags, bpi.WARNING)))
        self.assertTrue(any("'no_such_team'" in m for m in levels(diags, bpi.NOTE)))
        self.assertFalse(any("'no_such_team'" in m for m in levels(diags, bpi.WARNING)))
        self.assertEqual((self.f.root / "personas/dev/context_configuration.json").read_bytes(), before)

    def test_deterministic_output(self):
        self.f.write("personas/dev/b.json", persona("b"))
        self.f.write("personas/dev/a.json", persona("a"))
        self.assertEqual(bpi.render(self.f.build()[0]), bpi.render(self.f.build()[0]))
        self.assertEqual([e["id"] for e in self.f.build()[0]["personas"]], ["a", "b"])


class CheckModeTests(unittest.TestCase):
    def setUp(self):
        self.f = Fixture()
        self.addCleanup(self.f.close)
        self.f.write("personas/dev/a.json", persona("a"))
        self.args = ["--root", str(self.f.root)]

    def test_check_flow(self):
        self.assertEqual(bpi.main(["--check"] + self.args), 1)       # no index.json yet
        self.assertFalse((self.f.root / "index.json").exists())       # --check never writes
        self.assertEqual(bpi.main(self.args), 0)                      # generate
        self.assertEqual(bpi.main(["--check"] + self.args), 0)        # clean
        changed = persona("a")
        changed["metadata"]["description"] = "edited"
        self.f.write("personas/dev/a.json", changed)
        self.assertEqual(bpi.main(["--check"] + self.args), 1)        # stale
        self.assertEqual(bpi.main(self.args), 0)
        self.assertEqual(bpi.main(["--check"] + self.args), 0)

    def test_errors_block_write_and_check(self):
        self.f.write("personas/dev/broken.json", "{not json")
        self.assertEqual(bpi.main(self.args), 1)
        self.assertFalse((self.f.root / "index.json").exists())
        self.assertEqual(bpi.main(["--check"] + self.args), 1)

    def _snapshot(self, generated=()):
        """Bytes of every file except the generator's own outputs."""
        root = self.f.root
        def is_output(p):
            rel = p.relative_to(root).as_posix()
            return rel == "index.json" or any(rel.startswith(g) for g in generated)
        return {p: p.read_bytes() for p in root.rglob("*") if p.is_file() and not is_output(p)}

    def test_generation_writes_only_its_outputs(self):
        generated = ("plugin/catalog/", "plugin/framework/", "plugin/agents/")
        before = self._snapshot(generated=generated)
        bpi.main(self.args)
        self.assertEqual(self._snapshot(generated=generated), before)

    def test_check_mode_writes_nothing(self):
        bpi.main(self.args)
        def everything():
            return {p: p.read_bytes() for p in self.f.root.rglob("*") if p.is_file()}
        before = everything()
        bpi.main(["--check"] + self.args)
        self.assertEqual(everything(), before)


class BundleTests(unittest.TestCase):
    """plugin/catalog/ is a generated copy of index.json plus every file the index lists."""

    def setUp(self):
        self.f = Fixture()
        self.addCleanup(self.f.close)
        self.f.write("personas/dev/a.json", persona("a"))
        self.f.write("personas/dev/teams/t.json", team("t", ["a"]))
        self.f.write("personas/persona_schema_example.json", persona("tmpl"))
        self.f.write("personas/dev/context_configuration.json", {"available_personas": ["a"]})
        self.args = ["--root", str(self.f.root)]
        self.bundle = self.f.root / "plugin" / "catalog"

    def bundled(self):
        return sorted(p.relative_to(self.bundle).as_posix() for p in self.bundle.rglob("*") if p.is_file())

    def test_copies_index_and_listed_files_byte_identical(self):
        self.assertEqual(bpi.main(self.args), 0)
        self.assertEqual(self.bundled(), ["index.json", "personas/dev/a.json", "personas/dev/teams/t.json"])
        for rel in self.bundled():
            src = self.f.root / ("index.json" if rel == "index.json" else rel)
            self.assertEqual((self.bundle / rel).read_bytes(), src.read_bytes(), rel)

    def test_unlisted_files_not_bundled(self):
        bpi.main(self.args)
        self.assertNotIn("personas/persona_schema_example.json", self.bundled())
        self.assertNotIn("personas/dev/context_configuration.json", self.bundled())

    def test_regeneration_removes_stale_bundled_files(self):
        bpi.main(self.args)
        (self.f.root / "personas/dev/teams/t.json").unlink()
        bpi.main(self.args)
        self.assertEqual(self.bundled(), ["index.json", "personas/dev/a.json"])

    def test_errors_write_no_bundle(self):
        self.f.write("personas/dev/broken.json", "{not json")
        self.assertEqual(bpi.main(self.args), 1)
        self.assertFalse(self.bundle.exists())


class BundleCheckTests(unittest.TestCase):
    """--check also guards plugin/catalog/."""

    def check(self):
        import contextlib, io
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = bpi.main(["--check"] + self.args)
        return code, err.getvalue()

    def setUp(self):
        self.f = Fixture()
        self.addCleanup(self.f.close)
        self.f.write("personas/dev/a.json", persona("a"))
        self.f.write("personas/dev/teams/t.json", team("t", ["a"]))
        self.args = ["--root", str(self.f.root)]
        self.bundle = self.f.root / "plugin" / "catalog"
        bpi.main(self.args)

    def test_clean_bundle_passes(self):
        self.assertEqual(self.check()[0], 0)

    def test_missing_bundle_fails_with_command(self):
        import shutil
        shutil.rmtree(self.bundle)
        code, err = self.check()
        self.assertEqual(code, 1)
        self.assertIn("python3 scripts/build_persona_index.py", err)
        self.assertIn("plugin/catalog/index.json", err)

    def test_missing_one_file_fails(self):
        (self.bundle / "personas/dev/a.json").unlink()
        code, err = self.check()
        self.assertEqual(code, 1)
        self.assertIn("personas/dev/a.json", err)

    def test_extra_file_fails(self):
        (self.bundle / "stray.txt").write_text("x")
        code, err = self.check()
        self.assertEqual(code, 1)
        self.assertIn("stray.txt", err)
        self.assertIn("python3 scripts/build_persona_index.py", err)

    def test_edited_bundled_file_fails(self):
        (self.bundle / "personas/dev/a.json").write_text("{}")
        code, err = self.check()
        self.assertEqual(code, 1)
        self.assertIn("personas/dev/a.json", err)

    def test_edited_source_without_regeneration_fails(self):
        changed = persona("a")
        changed["metadata"]["description"] = "edited"
        self.f.write("personas/dev/a.json", changed)
        self.assertEqual(self.check()[0], 1)

    def test_check_does_not_repair_bundle(self):
        (self.bundle / "stray.txt").write_text("x")
        self.check()
        self.assertTrue((self.bundle / "stray.txt").exists())


class PluginFrameworkTests(unittest.TestCase):
    """plugin/framework/ and plugin/agents/challenger.md are generated and checked like the catalog."""

    def setUp(self):
        self.f = Fixture()
        self.addCleanup(self.f.close)
        self.f.write("personas/dev/a.json", persona("a"))
        self.f.write("personas/dev/context_configuration.json", {
            "context_name": "dev", "description": "Dev things",
            "context_behavioral_protocols": {"challenge_focus": "correctness_of_dev"}})
        self.f.write("personas/art/context_configuration.json", {"description": "Art things"})
        self.f.write("personas/art/hero/context_configuration_hero.json", {"description": "project level"})
        self.args = ["--root", str(self.f.root)]
        self.framework = self.f.root / "plugin" / "framework"
        self.agent = self.f.root / "plugin" / "agents" / "challenger.md"
        bpi.main(self.args)

    def check(self):
        import contextlib, io
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = bpi.main(["--check"] + self.args)
        return code, err.getvalue()

    def test_framework_files_copied_byte_identical(self):
        for rel in bpi.FRAMEWORK_SOURCES:
            self.assertEqual((self.framework / Path(rel).name).read_bytes(), (self.f.root / rel).read_bytes())

    def test_domains_table_lists_domain_level_configs_only(self):
        table = json.loads((self.framework / "domains.json").read_text())
        self.assertEqual(table, {"domains": {
            "art": {"description": "Art things"},
            "dev": {"challenge_focus": "correctness_of_dev", "description": "Dev things"}}})

    def test_domain_name_differing_from_directory_is_error(self):
        self.f.write("personas/art/context_configuration.json", {"context_name": "paint"})
        self.assertEqual(bpi.main(self.args), 1)

    def test_challenger_agent_is_front_matter_plus_prompt_body(self):
        text = self.agent.read_text()
        self.assertTrue(text.startswith("---\nname: challenger\n"))
        self.assertIn("tools: Read\n---\n\nYou are operating in **Challenge Phase**", text)
        self.assertNotIn("Notes for Runtime Implementers", text)

    def test_clean_passes(self):
        self.assertEqual(self.check()[0], 0)

    def test_missing_framework_file_fails(self):
        (self.framework / "domains.json").unlink()
        code, err = self.check()
        self.assertEqual(code, 1)
        self.assertIn("plugin/framework/domains.json is missing", err)

    def test_stale_framework_file_fails(self):
        self.f.write("config/challenge_synthesis_protocol.md", "# changed\n")
        code, err = self.check()
        self.assertEqual(code, 1)
        self.assertIn("plugin/framework/challenge_synthesis_protocol.md differs", err)

    def test_extra_framework_file_fails(self):
        (self.framework / "stray.md").write_text("x")
        code, err = self.check()
        self.assertEqual(code, 1)
        self.assertIn("stray.md", err)

    def test_edited_agent_fails_and_regeneration_repairs_it(self):
        self.agent.write_text("edited")
        self.assertEqual(self.check()[0], 1)
        bpi.main(self.args)
        self.assertEqual(self.check()[0], 0)

    def test_hand_written_agents_are_not_pruned_or_flagged(self):
        other = self.f.root / "plugin" / "agents" / "synthesizer.md"
        other.write_text("mine")
        self.assertEqual(self.check()[0], 0)
        bpi.main(self.args)
        self.assertEqual(other.read_text(), "mine")

    def test_missing_source_is_error(self):
        (self.f.root / "config/challenge_synthesis_protocol.md").unlink()
        self.assertEqual(bpi.main(self.args), 1)

    def test_check_changes_no_source_file(self):
        before = {p: p.read_bytes() for p in (self.f.root / "personas").rglob("*") if p.is_file()}
        bpi.main(self.args)
        self.assertEqual({p: p.read_bytes() for p in before}, before)


class RealRepoTests(unittest.TestCase):
    """Checks against the committed catalog. These encode facts about this repo on 2026-10-09."""

    @classmethod
    def setUpClass(cls):
        cls.index, cls.diags = bpi.build_index(REPO)

    def test_no_errors(self):
        self.assertEqual(levels(self.diags, bpi.ERROR), [])

    def test_counts(self):
        self.assertEqual(len(self.index["personas"]), 28)
        self.assertEqual(len(self.index["teams"]), 6)

    def test_template_not_indexed(self):
        self.assertFalse(any("persona_schema_example" in e["path"] for e in self.index["personas"]))

    def test_stale_config_ids_resolve_via_alias(self):
        owner = {a: e["id"] for e in self.index["personas"] for a in e["aliases"]}
        self.assertEqual(owner["ott_ux_persona"], "ux_designer")
        self.assertEqual(owner["10_foot_ui_designer"], "ui_designer")
        self.assertEqual(owner["design_expert"], "ux_ui_strategist")
        self.assertEqual(owner["developer_coding_persona"], "experienced_developer")

    def test_team_aliases(self):
        owner = {a: t["id"] for t in self.index["teams"] for a in t["aliases"]}
        self.assertEqual(owner["react_fullstack_team"], "react_fullstack_development_team")
        self.assertEqual(owner["news_aggregation_team"], "news_aggregation_app_team")

    def test_stubs(self):
        stubs = sorted(e["id"] for e in self.index["personas"] if e["status"] == "stub")
        self.assertEqual(stubs, ["backend_developer", "data_scientist", "product_manager", "system_architect"])
        teams = {t["id"]: t["status"] for t in self.index["teams"]}
        self.assertEqual(teams["intelligence_framework_team"], "contains_stubs")
        self.assertEqual([k for k, v in teams.items() if v == "contains_stubs"], ["intelligence_framework_team"])

    def test_security_review_team_is_a_note_not_a_warning(self):
        self.assertFalse([m for m in levels(self.diags, bpi.WARNING) if "available_teams" in m])
        notes = [m for m in levels(self.diags, bpi.NOTE) if "security_review_team" in m]
        self.assertEqual(len(notes), 1)

    def test_every_entry_hash_matches_file(self):
        for e in self.index["personas"] + self.index["teams"]:
            raw = (REPO / e["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), e["sha256"], e["path"])
            self.assertEqual(len(raw), e["bytes"], e["path"])

    def test_committed_index_is_current(self):
        self.assertEqual((REPO / "index.json").read_text(encoding="utf-8"), bpi.render(self.index))

    def test_team_members_all_resolve(self):
        ids = {e["id"] for e in self.index["personas"]}
        for t in self.index["teams"]:
            self.assertTrue(set(t["members"]) <= ids, t["id"])
            self.assertEqual(t["unresolved_members"], [], t["id"])
            self.assertNotEqual(t["status"], "incomplete", t["id"])


if __name__ == "__main__":
    unittest.main()
