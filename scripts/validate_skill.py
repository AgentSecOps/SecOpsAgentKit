#!/usr/bin/env python3
"""Validate skill directory structure and SKILL.md frontmatter compliance.

Usage:
  ./scripts/validate_skill.py skills/appsec/sast-semgrep    # validate one skill
  ./scripts/validate_skill.py --all                          # validate every skill
  ./scripts/validate_skill.py --json skills/appsec/sast-semgrep  # machine-readable output

Exit codes:
  0  All checked skills pass
  1  One or more validation errors found
  2  Usage / invocation error
"""

import json
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install it with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

VALID_CATEGORIES = {
    "appsec",
    "devsecops",
    "secsdlc",
    "threatmodel",
    "compliance",
    "incident-response",
    "offsec",
}

FORBIDDEN_FILES = {"README.md", "CHANGELOG.md", "INSTALLATION.md"}
PLACEHOLDERS = ["TODO", "FIXME", "your-github-username"]
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
MAX_SKILL_LINES = 750
MIN_DESCRIPTION_LEN = 100

REPO_ROOT = Path(__file__).parent.parent
MARKETPLACE_PATH = REPO_ROOT / "skills" / ".claude-plugin" / "marketplace.json"


# ---------------------------------------------------------------------------
# Result helpers
# ---------------------------------------------------------------------------

class CheckResult:
    def __init__(self, name: str, passed: bool, message: str = ""):
        self.name = name
        self.passed = passed
        self.message = message

    def to_dict(self) -> dict:
        return {"check": self.name, "passed": self.passed, "message": self.message}


def _pass(name: str, detail: str = "") -> CheckResult:
    return CheckResult(name, True, detail)


def _fail(name: str, detail: str) -> CheckResult:
    return CheckResult(name, False, detail)


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_frontmatter(skill_md: Path) -> tuple[dict | None, list[CheckResult]]:
    """Parse and return frontmatter dict; emit check results."""
    results: list[CheckResult] = []
    text = skill_md.read_text(encoding="utf-8")

    if not text.startswith("---"):
        results.append(_fail("frontmatter_present", "SKILL.md does not start with '---'"))
        return None, results
    results.append(_pass("frontmatter_present"))

    parts = text.split("---", 2)
    if len(parts) < 3:
        results.append(_fail("frontmatter_parseable", "Could not find closing '---'"))
        return None, results

    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        results.append(_fail("frontmatter_parseable", f"YAML parse error: {exc}"))
        return None, results

    if not isinstance(fm, dict):
        results.append(_fail("frontmatter_parseable", "Frontmatter did not parse to a mapping"))
        return None, results

    results.append(_pass("frontmatter_parseable"))
    return fm, results


def check_required_fields(fm: dict) -> list[CheckResult]:
    required = ["name", "description", "version", "maintainer", "category", "tags"]
    missing = [f for f in required if f not in fm or fm[f] is None]
    if missing:
        return [_fail("required_fields", f"Missing required fields: {', '.join(missing)}")]
    return [_pass("required_fields", f"All required fields present: {', '.join(required)}")]


def check_description(fm: dict) -> list[CheckResult]:
    desc = str(fm.get("description", ""))
    results = []
    if "Use when:" not in desc:
        results.append(_fail("description_use_when", "description must contain 'Use when:' clause"))
    else:
        results.append(_pass("description_use_when", "'Use when:' clause present"))

    if len(desc) < MIN_DESCRIPTION_LEN:
        results.append(
            _fail("description_length", f"description is {len(desc)} chars (minimum {MIN_DESCRIPTION_LEN})")
        )
    else:
        results.append(_pass("description_length", f"description is {len(desc)} chars"))
    return results


def check_name(fm: dict) -> list[CheckResult]:
    name = str(fm.get("name", ""))
    if not KEBAB_RE.match(name):
        return [_fail("name_kebab_case", f"name '{name}' is not kebab-case")]
    return [_pass("name_kebab_case", f"name '{name}' is kebab-case")]


def check_category(fm: dict) -> list[CheckResult]:
    cat = str(fm.get("category", ""))
    if cat not in VALID_CATEGORIES:
        return [_fail("category_valid", f"category '{cat}' must be one of: {', '.join(sorted(VALID_CATEGORIES))}")]
    return [_pass("category_valid", f"category '{cat}' is valid")]


def check_version(fm: dict) -> list[CheckResult]:
    ver = str(fm.get("version", ""))
    if not SEMVER_RE.match(ver):
        return [_fail("version_semver", f"version '{ver}' is not semantic versioning (X.Y.Z)")]
    return [_pass("version_semver", f"version '{ver}'")]


def check_line_count(skill_md: Path) -> list[CheckResult]:
    lines = skill_md.read_text(encoding="utf-8").count("\n")
    if lines >= MAX_SKILL_LINES:
        return [_fail("line_count", f"SKILL.md is {lines} lines (must be < {MAX_SKILL_LINES})")]
    return [_pass("line_count", f"SKILL.md is {lines} lines (< {MAX_SKILL_LINES})")]


def check_placeholders(skill_md: Path) -> list[CheckResult]:
    text = skill_md.read_text(encoding="utf-8")
    found = [p for p in PLACEHOLDERS if p in text]
    if found:
        return [_fail("no_placeholders", f"Found placeholder text: {', '.join(found)}")]
    return [_pass("no_placeholders", "No placeholder text found")]


def check_forbidden_files(skill_dir: Path) -> list[CheckResult]:
    found = [f for f in FORBIDDEN_FILES if (skill_dir / f).exists()]
    if found:
        return [_fail("no_forbidden_files", f"Forbidden files present: {', '.join(found)}")]
    return [_pass("no_forbidden_files", "No forbidden files")]


def check_scripts_executable(skill_dir: Path) -> list[CheckResult]:
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return [_pass("scripts_executable", "No scripts/ directory")]
    non_exec = [
        f.name for f in scripts_dir.iterdir()
        if f.is_file() and not os.access(f, os.X_OK)
    ]
    if non_exec:
        return [_fail("scripts_executable", f"Not executable: {', '.join(sorted(non_exec))}")]
    return [_pass("scripts_executable", "All scripts are executable")]


def check_reference_linkage(skill_dir: Path, skill_md: Path) -> list[CheckResult]:
    refs_dir = skill_dir / "references"
    if not refs_dir.exists():
        return [_pass("reference_linkage", "No references/ directory")]
    skill_text = skill_md.read_text(encoding="utf-8")
    unlinked = [
        f.name for f in refs_dir.iterdir()
        if f.is_file() and f.name not in skill_text
    ]
    if unlinked:
        return [_fail("reference_linkage", f"Reference files not linked in SKILL.md: {', '.join(sorted(unlinked))}")]
    return [_pass("reference_linkage", "All reference files linked in SKILL.md")]


def check_marketplace(skill_dir: Path) -> list[CheckResult]:
    if not MARKETPLACE_PATH.exists():
        return [_fail("marketplace_registered", f"marketplace.json not found at {MARKETPLACE_PATH}")]

    try:
        data = json.loads(MARKETPLACE_PATH.read_text())
    except json.JSONDecodeError as exc:
        return [_fail("marketplace_registered", f"marketplace.json parse error: {exc}")]

    # Build relative path as it appears in marketplace.json: ./category/skill-name
    try:
        rel = skill_dir.relative_to(REPO_ROOT / "skills")
        skill_path = "./" + str(rel).replace("\\", "/")
    except ValueError:
        return [_fail("marketplace_registered", "Could not compute relative skill path")]

    all_skills: list[str] = []
    for plugin in data.get("plugins", []):
        all_skills.extend(plugin.get("skills", []))

    if skill_path not in all_skills:
        return [_fail("marketplace_registered", f"'{skill_path}' not found in marketplace.json")]
    return [_pass("marketplace_registered", f"Registered as '{skill_path}'")]


# ---------------------------------------------------------------------------
# Full skill validation
# ---------------------------------------------------------------------------

def validate_skill(skill_dir: Path) -> tuple[list[CheckResult], bool]:
    """Run all checks for one skill. Returns (results, passed)."""
    skill_md = skill_dir / "SKILL.md"
    results: list[CheckResult] = []

    if not skill_md.exists():
        results.append(_fail("skill_md_exists", f"SKILL.md not found in {skill_dir}"))
        return results, False

    results.append(_pass("skill_md_exists"))

    fm, fm_results = check_frontmatter(skill_md)
    results.extend(fm_results)

    if fm is not None:
        results.extend(check_required_fields(fm))
        results.extend(check_description(fm))
        results.extend(check_name(fm))
        results.extend(check_category(fm))
        results.extend(check_version(fm))

    results.extend(check_line_count(skill_md))
    results.extend(check_placeholders(skill_md))
    results.extend(check_forbidden_files(skill_dir))
    results.extend(check_scripts_executable(skill_dir))
    results.extend(check_reference_linkage(skill_dir, skill_md))
    results.extend(check_marketplace(skill_dir))

    passed = all(r.passed for r in results)
    return results, passed


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def print_results(skill_dir: Path, results: list[CheckResult], passed: bool) -> None:
    total = len(results)
    ok = sum(1 for r in results if r.passed)
    print(f"\nValidating {skill_dir} ...")
    for r in results:
        icon = "✓" if r.passed else "✗"
        detail = f" ({r.message})" if r.message else ""
        print(f"  {icon} {r.name}{detail}")
    status = "PASS" if passed else "FAIL"
    print(f"  {status} ({ok}/{total} checks)")


def print_results_json(skill_dir: Path, results: list[CheckResult], passed: bool) -> None:
    out = {
        "skill": str(skill_dir),
        "passed": passed,
        "checks": [r.to_dict() for r in results],
    }
    print(json.dumps(out, indent=2))


# ---------------------------------------------------------------------------
# Skill discovery
# ---------------------------------------------------------------------------

def discover_all_skills() -> list[Path]:
    skills_root = REPO_ROOT / "skills"
    found = []
    for category in VALID_CATEGORIES:
        cat_dir = skills_root / category
        if not cat_dir.exists():
            continue
        for skill_dir in sorted(cat_dir.iterdir()):
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                found.append(skill_dir)
    return found


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = sys.argv[1:]
    as_json = "--json" in args
    all_mode = "--all" in args
    positional = [a for a in args if not a.startswith("--")]

    if not all_mode and not positional:
        print(__doc__)
        sys.exit(2)

    if all_mode:
        skill_dirs = discover_all_skills()
        if not skill_dirs:
            print("No skills found.", file=sys.stderr)
            sys.exit(2)
    else:
        skill_dirs = [Path(p).resolve() for p in positional]

    overall_pass = True
    for skill_dir in skill_dirs:
        results, passed = validate_skill(skill_dir)
        if not passed:
            overall_pass = False
        if as_json:
            print_results_json(skill_dir, results, passed)
        else:
            print_results(skill_dir, results, passed)

    sys.exit(0 if overall_pass else 1)


if __name__ == "__main__":
    main()
