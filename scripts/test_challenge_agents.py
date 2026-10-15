"""The challenger agents embed config/challenge_phase_prompt.md; the plugin's challenge files must match the repo-local ones."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPT = ROOT / "config" / "challenge_phase_prompt.md"
AGENT = ROOT / ".claude" / "agents" / "challenger.md"
SYNTH = ROOT / ".claude" / "agents" / "synthesizer.md"
PLUGIN = ROOT / "plugin"


def prompt_body():
    """The system prompt and output format, without the runtime-implementer notes."""
    text = PROMPT.read_text()
    start = text.index("You are operating in **Challenge Phase**")
    end = text.index("---\n\n## Notes for Runtime Implementers")
    return text[start:end].strip()


def agent_body():
    text = AGENT.read_text()
    match = re.match(r"---\n.*?\n---\n\n(.*)", text, re.DOTALL)
    if not match:
        raise AssertionError("challenger.md has no frontmatter")
    return match.group(1).strip()


class ChallengerAgentTest(unittest.TestCase):
    def test_agent_body_matches_phase_prompt(self):
        self.assertEqual(
            agent_body(),
            prompt_body(),
            "challenger.md is out of sync with config/challenge_phase_prompt.md; "
            "copy the prompt section into the agent body",
        )

    def test_agent_frontmatter_names_the_agent(self):
        head = AGENT.read_text().split("---")[1]
        self.assertIn("name: challenger", head)


def body_after_front_matter(path):
    match = re.match(r"---\n.*?\n---\n\n(.*)", path.read_text(), re.DOTALL)
    if not match:
        raise AssertionError(f"{path} has no front matter")
    return match.group(1).strip()


def requirements(path):
    text = path.read_text()
    return text[text.index("**Requirements:**"):].strip()


class PluginChallengeFilesTest(unittest.TestCase):
    def test_plugin_challenger_body_matches_phase_prompt(self):
        self.assertEqual(body_after_front_matter(PLUGIN / "agents" / "challenger.md"), prompt_body())

    def test_plugin_challenger_body_matches_repo_local_agent(self):
        self.assertEqual(body_after_front_matter(PLUGIN / "agents" / "challenger.md"), agent_body())

    def test_plugin_synthesizer_requirements_match_repo_local(self):
        self.assertEqual(requirements(PLUGIN / "agents" / "synthesizer.md"), requirements(SYNTH))

    def test_plugin_agents_are_read_only(self):
        for name in ("challenger", "synthesizer"):
            head = (PLUGIN / "agents" / f"{name}.md").read_text().split("---")[1]
            self.assertIn(f"name: {name}", head)
            self.assertRegex(head, r"(?m)^tools: Read$")

    def test_plugin_commands_name_the_same_subagents_and_pass_only_their_inputs(self):
        pairs = (("challenge", "challenger"), ("synthesize", "synthesizer"))
        for command, agent in pairs:
            local = (ROOT / ".claude" / "commands" / f"{command}.md").read_text()
            plugin = (PLUGIN / "commands" / f"{command}.md").read_text()
            self.assertIn(f"`{agent}` subagent", local)
            self.assertIn(f"`tif:{agent}` subagent", plugin)
            for text in (local, plugin):
                self.assertIn("nothing else", text.lower())
                self.assertIn("no summary of this conversation", text.lower())
                self.assertIn("Challenge Artifact", text)
                self.assertIn("verbatim", text)

    def test_plugin_synthesize_command_passes_framework_dir(self):
        text = (PLUGIN / "commands" / "synthesize.md").read_text()
        self.assertIn("framework_dir: ${CLAUDE_PLUGIN_ROOT}/framework", text)
        self.assertNotIn("config/", text)

    def test_plugin_challenge_command_passes_no_framework_dir(self):
        self.assertNotIn("framework_dir", (PLUGIN / "commands" / "challenge.md").read_text())

    def test_exposed_surface(self):
        self.assertEqual(sorted(p.name for p in (PLUGIN / "skills").iterdir()), ["catalog"])
        self.assertEqual(sorted(p.stem for p in (PLUGIN / "commands").glob("*.md")), ["challenge", "context", "synthesize"])
        self.assertEqual(sorted(p.stem for p in (PLUGIN / "agents").glob("*.md")), ["challenger", "synthesizer"])


if __name__ == "__main__":
    unittest.main()
