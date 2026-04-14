#!/usr/bin/env bash
# init_skill.sh — Initialize a new skill from the _template directory.
set -euo pipefail

SKILL_NAME="${1:-}"
CATEGORY="${2:-}"

VALID_CATEGORIES="appsec devsecops secsdlc threatmodel compliance incident-response offsec"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE_DIR="${REPO_ROOT}/skills/_template"

usage() {
  echo "Usage: $(basename "$0") <skill-name> <category>"
  echo ""
  echo "  skill-name   Kebab-case name (e.g. sast-semgrep, vuln-trivy)"
  echo "  category     One of: ${VALID_CATEGORIES}"
  echo ""
  echo "Examples:"
  echo "  $(basename "$0") sast-semgrep appsec"
  echo "  $(basename "$0") zeek-monitor incident-response"
  exit 1
}

# Require both arguments
if [[ -z "$SKILL_NAME" || -z "$CATEGORY" ]]; then
  usage
fi

# Validate kebab-case
if [[ ! "$SKILL_NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Error: skill-name must be kebab-case (lowercase letters, digits, hyphens)" >&2
  echo "  Got: $SKILL_NAME" >&2
  exit 1
fi

# Validate category
VALID=0
for CAT in $VALID_CATEGORIES; do
  if [[ "$CATEGORY" == "$CAT" ]]; then
    VALID=1
    break
  fi
done
if [[ "$VALID" -eq 0 ]]; then
  echo "Error: category must be one of: ${VALID_CATEGORIES}" >&2
  echo "  Got: $CATEGORY" >&2
  exit 1
fi

TARGET_DIR="${REPO_ROOT}/skills/${CATEGORY}/${SKILL_NAME}"

# Refuse to overwrite an existing skill
if [[ -e "$TARGET_DIR" ]]; then
  echo "Error: ${TARGET_DIR} already exists" >&2
  exit 1
fi

# Copy template
cp -r "$TEMPLATE_DIR" "$TARGET_DIR"

# Patch frontmatter: name and category fields
sed -i "s/^name: .*/name: ${SKILL_NAME}/" "${TARGET_DIR}/SKILL.md"
sed -i "s/^category: .*/category: ${CATEGORY}/" "${TARGET_DIR}/SKILL.md"

# Make any bundled scripts executable
if [[ -d "${TARGET_DIR}/scripts" ]]; then
  find "${TARGET_DIR}/scripts" -type f -exec chmod +x {} \;
fi

echo "Skill initialized at ${TARGET_DIR}"
echo ""
echo "Next steps:"
echo "  1. Edit ${TARGET_DIR}/SKILL.md — update description, maintainer, tags, frameworks"
echo "  2. Add scripts to ${TARGET_DIR}/scripts/ and references to ${TARGET_DIR}/references/"
echo "  3. Run: ./scripts/validate_skill.py skills/${CATEGORY}/${SKILL_NAME}"
echo "  4. Update: skills/.claude-plugin/marketplace.json  (or run ./scripts/generate_marketplace.py)"
