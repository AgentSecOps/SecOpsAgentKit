#!/usr/bin/env bash
# install_hooks.sh — Install git hooks from .githooks/ into .git/hooks/.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOKS_SRC="${REPO_ROOT}/.githooks"
HOOKS_DST="${REPO_ROOT}/.git/hooks"

if [[ ! -d "$HOOKS_SRC" ]]; then
  echo "Error: .githooks/ directory not found at ${HOOKS_SRC}" >&2
  exit 1
fi

if [[ ! -d "$HOOKS_DST" ]]; then
  echo "Error: .git/hooks/ not found. Are you inside a git repository?" >&2
  exit 1
fi

echo "Installing git hooks from .githooks/ ..."
for hook in "$HOOKS_SRC"/*; do
  name="$(basename "$hook")"
  dest="${HOOKS_DST}/${name}"
  cp "$hook" "$dest"
  chmod +x "$dest"
  echo "  Installed: .git/hooks/${name}"
done

echo "Done. Hooks will run automatically on git operations."
echo ""
echo "Installed hooks:"
echo "  pre-commit  — validates staged SKILL.md files before each commit"
