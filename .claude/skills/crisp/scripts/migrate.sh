#!/bin/bash
# Crisp Design Language - Migration Helper
# Version: 0.1.3
#
# Scans project files for old hex values and reports/replaces them.
#
# Usage:
#   ./migrate.sh /path/to/project [--dry-run]
#
# --dry-run: report only, no changes
# Without flag: performs sed replacements

set -e

TARGET=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    *)
      TARGET="$1"
      shift
      ;;
  esac
done

if [ -z "$TARGET" ]; then
  echo "Usage: ./migrate.sh /path/to/project [--dry-run]"
  exit 1
fi

# Old -> New hex mapping
declare -A REPLACEMENTS=(
  # Light mode backgrounds/surfaces
  ["#FAFAF8"]="#fff8f2"
  ["#F4F4F2"]="#FFFBF7"

  # Text colors
  ["#1C1C1A"]="#1F1F1F"
  ["#5C5C58"]="#454545"
  ["#8A8A86"]="#7A7A7A"
  ["#C0BFBC"]="rgba(122,122,122,0.50)"

  # Borders
  ["#E2E1DE"]="#EDE3D4"
  ["#EEEEED"]="#FFF1E2"

  # Accent
  ["#f59e0b"]="#B9975C"
  ["#d97706"]="#725A31"
  ["#fef3c7"]="#FFEBD6"
  ["#fbbf24"]="#D4BF9B"

  # Functional: success
  ["#22c55e"]="#286736"
  ["#dcfce7"]="rgba(40,103,54,0.10)"
  ["#166534"]="#173B1F"
  ["#4ade80"]="#39934D"

  # Functional: warning
  ["#eab308"]="#A8862B"
  ["#92400e"]="#6B5518"
  ["#facc15"]="#D4AD4A"

  # Functional: error
  ["#ef4444"]="#AE1C09"
  ["#fee2e2"]="rgba(174,28,9,0.10)"
  ["#991b1b"]="#741306"
  ["#f87171"]="#F5533D"

  # Functional: info
  ["#3b82f6"]="#49696E"
  ["#dbeafe"]="rgba(73,105,110,0.10)"
  ["#1e40af"]="#314649"
  ["#60a5fa"]="#91B1B6"

  # Dark mode canvas/elevation
  ["#0a0a0b"]="#1F1F1F"
  ["#111113"]="#2A2A2A"
  ["#1A1A1C"]="#353535"
  ["#252527"]="#404040"
  ["#2D2D30"]="#4A4A4A"

  # Dark mode borders
  ["#1f1f23"]="#353535"
  ["#3A3A3E"]="#4A4A4A"
)

# File extensions to scan
EXTENSIONS="css,html,svelte,tsx,jsx,vue,ts,js"

echo "Scanning $TARGET for old Crisp hex values..."
echo ""

FOUND=0

for OLD in "${!REPLACEMENTS[@]}"; do
  NEW="${REPLACEMENTS[$OLD]}"

  # Case-insensitive grep
  MATCHES=$(grep -rin --include="*.css" --include="*.html" --include="*.svelte" \
    --include="*.tsx" --include="*.jsx" --include="*.vue" --include="*.ts" --include="*.js" \
    --exclude-dir="node_modules" --exclude-dir=".git" --exclude-dir="dist" --exclude-dir="build" \
    "$OLD" "$TARGET" 2>/dev/null || true)

  if [ -n "$MATCHES" ]; then
    FOUND=$((FOUND + 1))
    echo "[$OLD -> $NEW]"
    echo "$MATCHES" | head -20
    echo ""

    if [ "$DRY_RUN" = false ]; then
      find "$TARGET" \
        -type f \( -name "*.css" -o -name "*.html" -o -name "*.svelte" \
        -o -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" -o -name "*.ts" -o -name "*.js" \) \
        ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/dist/*" ! -path "*/build/*" \
        -exec sed -i '' "s|$OLD|$NEW|g" {} +
    fi
  fi
done

echo "---"
if [ "$DRY_RUN" = true ]; then
  echo "Dry run complete. Found $FOUND old hex patterns."
  echo "Run without --dry-run to apply replacements."
else
  echo "Migration complete. Replaced $FOUND hex patterns."
  echo "Review changes with: git diff"
fi
