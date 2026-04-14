#!/usr/bin/env python3
"""Auto-generate marketplace.json from the skills/ directory structure.

Usage:
  python3 scripts/generate_marketplace.py           # Update marketplace.json in-place
  python3 scripts/generate_marketplace.py --check   # Exit 1 if marketplace.json is out of sync
  python3 scripts/generate_marketplace.py --dry-run # Print what would be written, no changes
"""

import json
import sys
from pathlib import Path

# Maps category directory name -> plugin name in marketplace.json
CATEGORY_TO_PLUGIN = {
    "appsec": "appsec-skills",
    "devsecops": "devsecops-skills",
    "secsdlc": "secsdlc-skills",
    "threatmodel": "threatmodel-skills",
    "compliance": "compliance-skills",
    "incident-response": "incident-response-skills",
    "offsec": "offsec-skills",
}

MARKETPLACE_PATH_REL = "skills/.claude-plugin/marketplace.json"


def discover_skills(skills_root: Path) -> dict[str, list[str]]:
    """Return a mapping of plugin-name -> sorted list of skill paths."""
    plugins: dict[str, list[str]] = {v: [] for v in CATEGORY_TO_PLUGIN.values()}
    for category, plugin_name in CATEGORY_TO_PLUGIN.items():
        cat_dir = skills_root / category
        if not cat_dir.exists():
            continue
        for skill_dir in sorted(cat_dir.iterdir()):
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                plugins[plugin_name].append(f"./{category}/{skill_dir.name}")
    return plugins


def main() -> None:
    repo_root = Path(__file__).parent.parent
    marketplace_path = repo_root / MARKETPLACE_PATH_REL

    if not marketplace_path.exists():
        print(f"Error: {MARKETPLACE_PATH_REL} not found. Create it first.", file=sys.stderr)
        sys.exit(1)

    existing = json.loads(marketplace_path.read_text())
    discovered = discover_skills(repo_root / "skills")

    # Update the skills list for each known plugin; leave unknown plugins untouched
    for plugin in existing["plugins"]:
        name = plugin["name"]
        if name in discovered:
            plugin["skills"] = discovered[name]

    output = json.dumps(existing, indent=2) + "\n"

    check_mode = "--check" in sys.argv
    dry_run = "--dry-run" in sys.argv

    if check_mode:
        current = marketplace_path.read_text()
        if current != output:
            print(
                "marketplace.json is out of sync with the skills/ directory.\n"
                f"Run:  python3 scripts/generate_marketplace.py\n"
                f"File: {MARKETPLACE_PATH_REL}",
                file=sys.stderr,
            )
            sys.exit(1)
        print("marketplace.json is up to date.")
    elif dry_run:
        print(output, end="")
    else:
        marketplace_path.write_text(output)
        total = sum(len(v) for v in discovered.values())
        print(f"marketplace.json updated ({total} skills registered).")


if __name__ == "__main__":
    main()
