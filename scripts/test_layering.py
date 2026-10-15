"""The Layer 2 layout and merge rule in config/framework_configuration_overview.md must match the config files."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PERSONAS = ROOT / "personas"
OVERVIEW = ROOT / "config" / "framework_configuration_overview.md"

IDENTITY = ["context_name", "context_type", "description", "note", "notes", "created_date", "updated_date"]
KEYED = ["activation_triggers", "context_behavioral_protocols"]
LISTS = ["available_personas", "reference_libraries", "always_on_personas", "available_teams"]


def config_files():
    return sorted(PERSONAS.rglob("context_configuration*.json"))


def domain_level():
    return [p for p in config_files() if p.name == "context_configuration.json"]


def project_level():
    return [p for p in config_files() if p.name != "context_configuration.json"]


class LayoutTests(unittest.TestCase):
    def test_domain_level_files_sit_directly_under_a_domain(self):
        for p in domain_level():
            self.assertEqual(p.parent.parent, PERSONAS, f"{p.relative_to(ROOT)} is not personas/<domain>/")

    def test_project_level_files_follow_the_pattern(self):
        for p in project_level():
            rel = p.relative_to(ROOT)
            self.assertEqual(p.parent.parent.parent, PERSONAS, f"{rel} is not personas/<domain>/<project>/")
            self.assertEqual(p.name, f"context_configuration_{p.parent.name}.json",
                             f"{rel}: the file suffix must equal its project directory name")

    def test_every_project_has_a_domain_level_parent(self):
        for p in project_level():
            parent = p.parent.parent / "context_configuration.json"
            self.assertTrue(parent.exists(), f"{p.relative_to(ROOT)} has no domain-level {parent.relative_to(ROOT)}")

    def test_every_config_is_json_with_a_name(self):
        for p in config_files():
            data = json.loads(p.read_text())
            self.assertIn("context_name", data, f"{p.relative_to(ROOT)} has no context_name")

    def test_project_config_does_not_redeclare_a_name_used_by_its_domain(self):
        for p in project_level():
            domain = json.loads((p.parent.parent / "context_configuration.json").read_text())
            self.assertNotEqual(json.loads(p.read_text())["context_name"], domain["context_name"],
                                f"{p.relative_to(ROOT)} repeats its domain's context_name")


class ClaimTests(unittest.TestCase):
    def test_path_claims_in_configs_name_the_domain_directory(self):
        # "personas/<x>/context_configuration_<project>.json" must be personas/<domain>/<project>/...
        for p in config_files():
            text = p.read_text()
            for m in re.finditer(r"personas/(<[a-z_]+>)/(?:<[a-z_]+>/)?context_configuration_<project>\.json", text):
                self.assertIn("personas/<domain>/<project>/context_configuration_<project>.json", m.group(0),
                              f"{p.relative_to(ROOT)}: write the full path personas/<domain>/<project>/...")

    def test_overview_names_every_key_the_merge_rule_depends_on(self):
        text = OVERVIEW.read_text()
        for key in IDENTITY + KEYED + LISTS:
            self.assertIn(f"`{key}`", text, f"overview merge rule does not mention `{key}`")

    def test_overview_states_the_project_path_pattern(self):
        self.assertIn("personas/[domain]/[project]/context_configuration_[project].json", OVERVIEW.read_text())

    def test_keyed_entries_in_project_configs_are_objects(self):
        for p in project_level():
            data = json.loads(p.read_text())
            for key in KEYED:
                if key in data:
                    self.assertIsInstance(data[key], dict, f"{p.relative_to(ROOT)}: {key} must be a keyed object")


if __name__ == "__main__":
    unittest.main()
