#!/bin/bash
# Crisp Design Language - Project Bootstrap
# Version: 0.1.3
#
# Usage: ./init.sh /path/to/project [--accent "#B9975C"]
#
# Creates a crisp/ directory in the target project with:
# - Font files (woff2)
# - fonts.css
# - design-system.css (with accent baked in)
# - tailwind.preset.js
# - design-tokens.json
#
# --accent is the only flag. Omit for Gold default.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CRISP_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ACCENT="#B9975C"
TARGET=""

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --accent)
      ACCENT="$2"
      shift 2
      ;;
    *)
      TARGET="$1"
      shift
      ;;
  esac
done

if [ -z "$TARGET" ]; then
  echo "Usage: ./init.sh /path/to/project [--accent \"#B9975C\"]"
  exit 1
fi

# Validate hex
if ! echo "$ACCENT" | grep -qE '^#[0-9a-fA-F]{6}$'; then
  echo "Error: accent must be a 6-digit hex color (e.g., #B9975C)"
  exit 1
fi

DEST="$TARGET/crisp"
mkdir -p "$DEST/fonts"

echo "Initializing Crisp Design Language in $DEST"

# Copy fonts
cp "$CRISP_DIR/assets/fonts/"*.woff2 "$DEST/fonts/"
cp "$CRISP_DIR/assets/css/fonts.css" "$DEST/"

# Copy design system
cp "$CRISP_DIR/assets/css/design-system.css" "$DEST/"

# Copy config files
cp "$CRISP_DIR/assets/config/tailwind.preset.js" "$DEST/"
cp "$CRISP_DIR/assets/config/design-tokens.json" "$DEST/"

# Generate accent if not default
if [ "$ACCENT" != "#B9975C" ]; then
  echo "Generating custom accent: $ACCENT"
  if command -v node &> /dev/null; then
    cd "$DEST"
    node "$CRISP_DIR/scripts/generate-accent.js" "$ACCENT"
    echo "Custom accent files generated."
  else
    echo "Warning: Node.js not found. Install Node 18+ and run generate-accent.js manually."
  fi
fi

echo ""
echo "Setup complete. Add to your HTML:"
echo ""
echo "  <link rel=\"stylesheet\" href=\"crisp/fonts.css\">"
echo "  <link rel=\"stylesheet\" href=\"crisp/design-system.css\">"
echo ""
echo "For Tailwind, add to tailwind.config.js:"
echo ""
echo "  import crispPreset from './crisp/tailwind.preset.js';"
echo "  export default { presets: [crispPreset], ... };"
echo ""
