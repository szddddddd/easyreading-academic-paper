#!/bin/sh
set -eu

SKILL_NAME="easyreading-academic-paper"
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SOURCE_DIR="$SCRIPT_DIR/$SKILL_NAME"
FORCE=0

usage() {
  cat <<'EOF'
Usage: ./install.sh <target> [--force]

Targets:
  codex    Install to ${CODEX_HOME:-$HOME/.codex}/skills
  claude   Install to ~/.claude/skills
  gemini   Install to ~/.gemini/skills
  grok     Install to ~/.grok/skills
  agents   Install to ~/.agents/skills (portable Agent Skills path)
  all      Install to codex, claude, gemini, and grok

Use --force to replace an existing installation.
EOF
}

if [ "$#" -eq 0 ]; then
  usage
  exit 2
fi

TARGET=$1
shift

while [ "$#" -gt 0 ]; do
  case "$1" in
    --force)
      FORCE=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown option: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if [ ! -f "$SOURCE_DIR/SKILL.md" ]; then
  printf 'Skill source not found: %s\n' "$SOURCE_DIR" >&2
  exit 1
fi

CODEX_ROOT=${CODEX_HOME:-"$HOME/.codex"}

root_for() {
  case "$1" in
    codex) printf '%s\n' "$CODEX_ROOT/skills" ;;
    claude) printf '%s\n' "$HOME/.claude/skills" ;;
    gemini) printf '%s\n' "$HOME/.gemini/skills" ;;
    grok) printf '%s\n' "$HOME/.grok/skills" ;;
    agents) printf '%s\n' "$HOME/.agents/skills" ;;
    *) return 1 ;;
  esac
}

case "$TARGET" in
  all) TARGETS="codex claude gemini grok" ;;
  codex|claude|gemini|grok|agents) TARGETS=$TARGET ;;
  -h|--help)
    usage
    exit 0
    ;;
  *)
    printf 'Unknown target: %s\n' "$TARGET" >&2
    usage >&2
    exit 2
    ;;
esac

for agent in $TARGETS; do
  root=$(root_for "$agent")
  destination="$root/$SKILL_NAME"
  if { [ -e "$destination" ] || [ -L "$destination" ]; } && [ "$FORCE" -ne 1 ]; then
    printf 'Installation already exists: %s\n' "$destination" >&2
    printf 'Re-run with --force to replace it.\n' >&2
    exit 2
  fi
done

for agent in $TARGETS; do
  root=$(root_for "$agent")
  destination="$root/$SKILL_NAME"
  temporary="$root/.${SKILL_NAME}.tmp.$$"

  mkdir -p "$root"
  rm -rf "$temporary"
  cp -R "$SOURCE_DIR" "$temporary"

  if [ -e "$destination" ] || [ -L "$destination" ]; then
    rm -rf "$destination"
  fi
  mv "$temporary" "$destination"
  printf 'Installed for %s: %s\n' "$agent" "$destination"
done
