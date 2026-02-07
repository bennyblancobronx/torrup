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

echo "Releasing $VERSION..."

# 1. Update VERSION in Dockerfile (optional as we use build-args now, but good for local)
# sed -i '' "s/ARG VERSION=.*/ARG VERSION=${VERSION#v}/" Dockerfile

# 2. Update APP_VERSION in src/config.py
sed -i '' "s/APP_VERSION = ".*"/APP_VERSION = "${VERSION#v}"/" src/config.py

# 3. Update version in README.md
sed -i '' "s/^## Version.*/## Version

${VERSION#v}/" README.md

# 4. Commit changes
git add src/config.py README.md
git commit -m "Bump version to $VERSION"

# 5. Tag and push
git tag -a "$VERSION" -m "Release $VERSION"
git push origin main
git push origin "$VERSION"

echo "Done. GitHub Action will now build and push the Docker image to GHCR."
