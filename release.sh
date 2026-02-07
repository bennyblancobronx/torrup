#!/bin/bash
# Simple release script for torrup

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: ./release.sh v0.1.9"
    exit 1
fi

# Ensure version starts with v
if [[ ! $VERSION =~ ^v ]]; then
    VERSION="v$VERSION"
fi

# Version without v
PLAIN_VERSION="${VERSION#v}"

echo "Releasing $VERSION ($PLAIN_VERSION)..."

# Detect OS for sed differences
case "$(uname)" in
    Darwin*)  SED_I=(sed -i '') ;;
    *)        SED_I=(sed -i)    ;;
esac

# 1. Update APP_VERSION in src/config.py
"${SED_I[@]}" "s/APP_VERSION = \".*\"/APP_VERSION = \"$PLAIN_VERSION\"/" src/config.py

# 2. Update version in README.md (using a simpler pattern)
# We match the line after '## Version'
"${SED_I[@]}" "/## Version/!b;n;c\\
\\
$PLAIN_VERSION" README.md

# 3. Commit changes
git add src/config.py README.md
git commit -m "Bump version to $VERSION"

# 4. Tag and push
git tag -a "$VERSION" -m "Release $VERSION"
git push origin main
git push origin "$VERSION"

echo "Done. GitHub Action will now build and push the Docker image to GHCR."