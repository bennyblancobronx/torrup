#!/usr/bin/env bash
#
# darules mechanical audit
# Checks rules that have deterministic, scriptable answers.
# Output: one line per check -- PASS|FAIL|SKIP rule_number description [details]
#
# Usage:
#   audit.sh                    -- check uncommitted changes (staged + unstaged)
#   audit.sh staged             -- check staged changes only
#   audit.sh file <path>        -- check a specific file or directory
#   audit.sh full               -- check all tracked files
#
# Version: 0.1.0

set -euo pipefail

MODE="${1:-diff}"
TARGET="${2:-}"

# ── Collect file list ─────────────────────────────────────────────

get_files() {
  case "$MODE" in
    staged)
      git diff --cached --name-only --diff-filter=ACMR 2>/dev/null || true
      ;;
    file)
      if [ -z "$TARGET" ]; then
        echo "ERROR: file mode requires a path argument" >&2
        exit 1
      fi
      if [ -d "$TARGET" ]; then
        find "$TARGET" -type f -not -path '*/.git/*' -not -name '.DS_Store'
      elif [ -f "$TARGET" ]; then
        echo "$TARGET"
      else
        echo "ERROR: $TARGET not found" >&2
        exit 1
      fi
      ;;
    full)
      git ls-files 2>/dev/null || find . -type f -not -path '*/.git/*' -not -name '.DS_Store'
      ;;
    *)
      # default: staged + unstaged changes
      git diff --name-only --diff-filter=ACMR 2>/dev/null || true
      git diff --cached --name-only --diff-filter=ACMR 2>/dev/null || true
      ;;
  esac | sort -u
}

FILES=$(get_files)

if [ -z "$FILES" ]; then
  echo "NO_CHANGES No files in scope"
  exit 0
fi

# ── Rule 8: Files under 400 lines ────────────────────────────────

rule8_pass=true
rule8_details=""

while IFS= read -r f; do
  [ -f "$f" ] || continue
  # skip binary files
  file --brief --mime "$f" 2>/dev/null | grep -q "^text/" || continue
  lines=$(wc -l < "$f" | tr -d ' ')
  if [ "$lines" -gt 400 ]; then
    rule8_pass=false
    rule8_details="${rule8_details} ${f}:${lines}lines"
  fi
done <<< "$FILES"

if $rule8_pass; then
  echo "PASS 8 Files under 400 lines"
else
  echo "FAIL 8 Files under 400 lines --${rule8_details}"
fi

# ── Rule 23: No emojis ───────────────────────────────────────────

rule23_pass=true
rule23_details=""

while IFS= read -r f; do
  [ -f "$f" ] || continue
  file --brief --mime "$f" 2>/dev/null | grep -q "^text/" || continue
  # Match common emoji ranges in unicode
  emoji_lines=$(grep -nP '[\x{1F300}-\x{1F9FF}\x{2600}-\x{26FF}\x{2700}-\x{27BF}\x{FE00}-\x{FE0F}\x{1F000}-\x{1F02F}\x{1F0A0}-\x{1F0FF}\x{1F100}-\x{1F64F}\x{1F680}-\x{1F6FF}\x{1F900}-\x{1F9FF}\x{1FA00}-\x{1FA6F}\x{1FA70}-\x{1FAFF}\x{200D}\x{20E3}]' "$f" 2>/dev/null || true)
  if [ -n "$emoji_lines" ]; then
    rule23_pass=false
    first_line=$(echo "$emoji_lines" | head -1 | cut -d: -f1)
    rule23_details="${rule23_details} ${f}:${first_line}"
  fi
done <<< "$FILES"

if $rule23_pass; then
  echo "PASS 23 No emojis"
else
  echo "FAIL 23 No emojis --${rule23_details}"
fi

# ── Rule 13: No root-level working files ──────────────────────────

rule13_pass=true
rule13_details=""

# Files that belong in root (whitelist)
ROOT_ALLOWED="^(\.gitignore|README\.md|LICENSE|changelog\.md|about\.md|contracts\.md|techguide\.md|CLAUDE\.md|\.env\.example|Makefile|package\.json|package-lock\.json|tsconfig\.json|Cargo\.toml|Cargo\.lock|go\.mod|go\.sum|Gemfile|Gemfile\.lock|requirements\.txt|pyproject\.toml|setup\.py|setup\.cfg|\.eslintrc.*|\.prettierrc.*|\.editorconfig|\.tool-versions|flake\.nix|flake\.lock|updateprojects\.sh)$"

while IFS= read -r f; do
  # Only check files directly in root (no slash in path)
  if [[ "$f" != */* ]] && ! echo "$f" | grep -qE "$ROOT_ALLOWED"; then
    rule13_pass=false
    rule13_details="${rule13_details} ${f}"
  fi
done <<< "$FILES"

if $rule13_pass; then
  echo "PASS 13 No root-level working files"
else
  echo "FAIL 13 No root-level working files --${rule13_details}"
fi

# ── Rule 10: No hardcoded secrets ─────────────────────────────────

rule10_pass=true
rule10_details=""

while IFS= read -r f; do
  [ -f "$f" ] || continue
  file --brief --mime "$f" 2>/dev/null | grep -q "^text/" || continue

  # Check for common secret patterns
  secret_lines=$(grep -nEi '(api[_-]?key|secret[_-]?key|password|token|credential)\s*[:=]\s*["\x27][^"\x27]{8,}' "$f" 2>/dev/null || true)

  # Check for .env files being tracked
  basename_f=$(basename "$f")
  if echo "$basename_f" | grep -qE '^\.env($|\.)' && [ "$basename_f" != ".env.example" ]; then
    rule10_pass=false
    rule10_details="${rule10_details} ${f}(env-file)"
  fi

  if [ -n "$secret_lines" ]; then
    rule10_pass=false
    first_line=$(echo "$secret_lines" | head -1 | cut -d: -f1)
    rule10_details="${rule10_details} ${f}:${first_line}(possible-secret)"
  fi
done <<< "$FILES"

if $rule10_pass; then
  echo "PASS 10 No hardcoded secrets"
else
  echo "FAIL 10 No hardcoded secrets --${rule10_details}"
fi

# ── Rule 24: No AI mentions in commits ────────────────────────────

if git rev-parse --is-inside-work-tree &>/dev/null; then
  recent_commits=$(git log --oneline -5 --format="%s" 2>/dev/null || true)
  if [ -n "$recent_commits" ]; then
    # Filter out path references like .claude/ or claude-flow before checking
    ai_mentions=$(echo "$recent_commits" | sed 's|[./]claude[-_/][^ ]*||g' | grep -iE '\b(claude|artificial intelligence|chatgpt|copilot|llm|gpt)\b' || true)
    # Also check for standalone "AI" (uppercase only, not as part of another word)
    ai_standalone=$(echo "$recent_commits" | grep -E '\bAI\b' || true)
    ai_mentions="${ai_mentions}${ai_standalone}"
    if [ -n "$ai_mentions" ]; then
      echo "FAIL 24 No AI mentions in commits -- $(echo "$ai_mentions" | head -1)"
    else
      echo "PASS 24 No AI mentions in commits"
    fi
  else
    echo "SKIP 24 No AI mentions in commits -- no recent commits"
  fi
else
  echo "SKIP 24 No AI mentions in commits -- not a git repo"
fi
