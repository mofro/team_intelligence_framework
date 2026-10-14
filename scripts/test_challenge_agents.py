"""The challenger agent embeds config/challenge_phase_prompt.md; keep them in sync."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPT = ROOT / "config" / "challenge_phase_prompt.md"
AGENT = ROOT / ".claude" / "agents" / "challenger.md"


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


if __name__ == "__main__":
    unittest.main()
