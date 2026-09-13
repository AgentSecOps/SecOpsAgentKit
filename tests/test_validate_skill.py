"""Fixture-based tests for the skill validator's local reference checks."""

import importlib.util
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_skill.py"
SPEC = importlib.util.spec_from_file_location("validate_skill", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import guard
    raise RuntimeError(f"Could not load validator from {VALIDATOR_PATH}")
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ReferenceTargetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.skill_dir = Path(self.temp_dir.name) / "skills" / "appsec" / "fixture"
        self.references_dir = self.skill_dir / "references"
        self.references_dir.mkdir(parents=True)
        self.skill_md = self.skill_dir / "SKILL.md"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_skill(self, text: str) -> None:
        self.skill_md.write_text(text, encoding="utf-8")

    def check(self):
        return validator.check_reference_targets(self.skill_dir, self.skill_md)[0]

    def test_missing_reference_target_fails(self) -> None:
        self.write_skill("See `references/missing.md` for details.\n")

        result = self.check()

        self.assertFalse(result.passed)
        self.assertEqual(result.name, "reference_targets")
        self.assertIn("references/missing.md", result.message)

    def test_existing_reference_target_with_fragment_passes(self) -> None:
        (self.references_dir / "guide.md").write_text("# Guide\n", encoding="utf-8")
        self.write_skill('See [the guide](references/guide.md#setup "Guide").\n')

        result = self.check()

        self.assertTrue(result.passed)

    def test_external_and_in_page_links_are_ignored(self) -> None:
        self.write_skill(
            "See [external](https://example.com/references/missing.md) "
            "or [section](#references/missing.md).\n"
        )

        result = self.check()

        self.assertTrue(result.passed)

    def test_reference_target_cannot_escape_skill_directory(self) -> None:
        self.write_skill("See [outside](references/../../secret.md).\n")

        result = self.check()

        self.assertFalse(result.passed)
        self.assertIn("outside skill directory", result.message)


if __name__ == "__main__":
    unittest.main()
