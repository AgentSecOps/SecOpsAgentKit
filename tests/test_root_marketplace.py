"""Regression tests for the repository-root Claude marketplace manifest."""

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"


class RootMarketplaceTests(unittest.TestCase):
    def test_declared_skill_sources_resolve_from_repository_root(self) -> None:
        data = json.loads(MARKETPLACE_PATH.read_text(encoding="utf-8"))

        self.assertIsInstance(data.get("plugins"), list)
        declared = [
            skill_path
            for plugin in data["plugins"]
            for skill_path in plugin.get("skills", [])
        ]

        self.assertGreater(len(declared), 0)
        for skill_path in declared:
            self.assertTrue(skill_path.startswith("./skills/"), skill_path)
            resolved = (REPO_ROOT / skill_path[2:]).resolve()
            self.assertTrue((resolved / "SKILL.md").is_file(), skill_path)


if __name__ == "__main__":
    unittest.main()
