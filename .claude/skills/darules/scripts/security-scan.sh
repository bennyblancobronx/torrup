#!/usr/bin/env bash
#
# darules security scan
# Pre-commit security scanner to detect secrets and sensitive files.
# Output: PASS, WARN, or BLOCK with details
#
# Usage:
#   security-scan.sh                -- scan staged files
#   security-scan.sh <file>         -- scan specific file
#   security-scan.sh --all          -- scan all tracked files
#
# Version: 0.1.0

set -euo pipefail

MODE="${1:-staged}"
TARGET="${2:-}"

# ── Collect file list ─────────────────────────────────────────────

get_files() {
  case "$MODE" in
    --all)
      git ls-files 2>/dev/null || find . -type f -not -path '*/.git/*'
      ;;
    staged)
      git diff --cached --name-only --diff-filter=ACMR 2>/dev/null || true
      ;;
    *)
      if [ -f "$MODE" ]; then
        echo "$MODE"
      elif [ -d "$MODE" ]; then
        find "$MODE" -type f -not -path '*/.git/*'
      else
        echo "ERROR: $MODE not found" >&2
        exit 1
      fi
      ;;
  esac | sort -u
}

FILES=$(get_files)

if [ -z "$FILES" ]; then
  echo "PASS No files to scan"
  exit 0
fi

BLOCKED=false
WARNINGS=""
BLOCKS=""

# ── Check for forbidden file types ────────────────────────────────

while IFS= read -r f; do
  [ -f "$f" ] || continue
  basename_f=$(basename "$f")

  # Environment files (block)
  if echo "$basename_f" | grep -qE '^\.env($|\.)' && [ "$basename_f" != ".env.example" ]; then
    BLOCKED=true
    BLOCKS="${BLOCKS}\n  [BLOCK] $f -- environment file"
    continue
  fi

  # Private key files (block)
  if echo "$basename_f" | grep -qE '\.(pem|key)$|^id_rsa'; then
    BLOCKED=true
    BLOCKS="${BLOCKS}\n  [BLOCK] $f -- private key file"
    continue
  fi

  # Credential files (block)
  if echo "$basename_f" | grep -qiE '^(credentials|serviceAccount)\.json$'; then
    BLOCKED=true
    BLOCKS="${BLOCKS}\n  [BLOCK] $f -- credential file"
    continue
  fi

done <<< "$FILES"

# ── Check file contents for secrets ───────────────────────────────

while IFS= read -r f; do
  [ -f "$f" ] || continue

  # Skip binary files
  file --brief --mime "$f" 2>/dev/null | grep -q "^text/" || continue

  # Skip files over 1MB
  size=$(wc -c < "$f" 2>/dev/null || echo 0)
  [ "$size" -lt 1048576 ] || continue

  # Check for hardcoded secrets
  # API_KEY, SECRET_KEY, PASSWORD, TOKEN, PRIVATE_KEY with values
  secret_match=$(grep -nEi '(api[_-]?key|secret[_-]?key|password|private[_-]?key)\s*[:=]\s*["\x27][^"\x27]{8,}' "$f" 2>/dev/null | head -3 || true)
  if [ -n "$secret_match" ]; then
    while IFS= read -r line; do
      line_num=$(echo "$line" | cut -d: -f1)
      BLOCKED=true
      BLOCKS="${BLOCKS}\n  [BLOCK] $f:$line_num -- possible hardcoded secret"
    done <<< "$secret_match"
  fi

  # Check for bearer tokens
  bearer_match=$(grep -nEi 'bearer\s+[a-zA-Z0-9_-]{20,}' "$f" 2>/dev/null | head -1 || true)
  if [ -n "$bearer_match" ]; then
    line_num=$(echo "$bearer_match" | cut -d: -f1)
    BLOCKED=true
    BLOCKS="${BLOCKS}\n  [BLOCK] $f:$line_num -- bearer token detected"
  fi

  # Check for connection strings with passwords
  conn_match=$(grep -nE '://[^:]+:[^@]+@' "$f" 2>/dev/null | head -1 || true)
  if [ -n "$conn_match" ]; then
    line_num=$(echo "$conn_match" | cut -d: -f1)
    BLOCKED=true
    BLOCKS="${BLOCKS}\n  [BLOCK] $f:$line_num -- connection string with credentials"
  fi

done <<< "$FILES"

# ── Check for code quality issues (warnings) ──────────────────────

while IFS= read -r f; do
  [ -f "$f" ] || continue

  # Skip binary files
  file --brief --mime "$f" 2>/dev/null | grep -q "^text/" || continue

  # Skip test files for debug statement check
  is_test=false
  if echo "$f" | grep -qE '(test|spec)\.(js|ts|py|rb)$|tests?/|__tests__/|spec/'; then
    is_test=true
  fi

  if ! $is_test; then
    # console.log, print statements, debugger
    debug_match=$(grep -nE '^\s*(console\.(log|debug|info)|print\(|debugger)' "$f" 2>/dev/null | head -1 || true)
    if [ -n "$debug_match" ]; then
      line_num=$(echo "$debug_match" | cut -d: -f1)
      WARNINGS="${WARNINGS}\n  [WARN] $f:$line_num -- debug statement"
    fi
  fi

  # .only() or .skip() in test files
  if $is_test; then
    only_match=$(grep -nE '\.(only|skip)\(' "$f" 2>/dev/null | head -1 || true)
    if [ -n "$only_match" ]; then
      line_num=$(echo "$only_match" | cut -d: -f1)
      WARNINGS="${WARNINGS}\n  [WARN] $f:$line_num -- .only() or .skip() in test"
    fi
  fi

  # TODO/FIXME comments
  todo_match=$(grep -nEi '\b(TODO|FIXME)\b' "$f" 2>/dev/null | head -1 || true)
  if [ -n "$todo_match" ]; then
    line_num=$(echo "$todo_match" | cut -d: -f1)
    WARNINGS="${WARNINGS}\n  [WARN] $f:$line_num -- TODO/FIXME comment"
  fi

done <<< "$FILES"

# ── Output results ────────────────────────────────────────────────

echo "SECURITY SCAN"

if [ -n "$BLOCKS" ]; then
  echo -e "$BLOCKS"
fi

if [ -n "$WARNINGS" ]; then
  echo -e "$WARNINGS"
fi

if $BLOCKED; then
  echo ""
  echo "RESULT: BLOCKED -- remove secrets before committing"
  exit 1
elif [ -n "$WARNINGS" ]; then
  echo ""
  echo "RESULT: WARNINGS -- review before proceeding"
  exit 0
else
  echo "  [PASS] No security issues found"
  echo ""
  echo "RESULT: PASS"
  exit 0
fi
