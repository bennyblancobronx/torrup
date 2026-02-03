#!/usr/bin/env bash
#
# scan-contributors.sh v0.1.1
# Two-part protection:
#   1. Scans for contributor intruders in files and git history
#   2. Verifies .gitignore blocks dangerous .claude files
#
# Usage:
#   ./scan-contributors.sh [directory]           # Run both checks
#   ./scan-contributors.sh [directory] --scan    # Only scan for intruders
#   ./scan-contributors.sh [directory] --verify  # Only verify gitignore
#   ./scan-contributors.sh [directory] --fix     # Auto-fix gitignore issues

set -euo pipefail

TARGET_DIR="${1:-.}"
MODE="${2:-both}"

ALLOWED_NAME="bennyblancobronx"
ALLOWED_EMAIL="casket.iphone392@nizomail.com"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

FOUND_ISSUES=0
SCAN_COUNT=0
GITIGNORE_ISSUES=0

# ============================================
# PART 1: GITIGNORE VERIFICATION
# ============================================

# .claude paths that MUST be in .gitignore (contain attribution/config)
REQUIRED_IGNORES=(
    ".claude/settings.json"
    ".claude/settings.local.json"
    ".claude/helpers/"
    ".claude/agents/"
    ".claude/commands/"
    ".claude-flow/"
    ".mcp.json"
    "CLAUDE.md"
)

# Patterns that indicate dangerous attribution content in .claude files
# These are SPECIFIC attribution patterns, not just tool references
DANGEROUS_CLAUDE_PATTERNS=(
    "co-authored-by[[:space:]]*:"
    "generated with \[claude"
    "noreply@anthropic\.com"
    "ruv@ruv\.net"
    "@author[[:space:]]*:[[:space:]]*claude"
)

verify_gitignore() {
    local gitignore="$TARGET_DIR/.gitignore"

    echo -e "${BLUE}[GITIGNORE VERIFICATION]${NC}"
    echo "Checking required .gitignore entries..."
    echo ""

    if [ ! -f "$gitignore" ]; then
        echo -e "${RED}[MISSING]${NC} No .gitignore file found!"
        GITIGNORE_ISSUES=$((GITIGNORE_ISSUES + 1))
        return
    fi

    local missing=()

    for pattern in "${REQUIRED_IGNORES[@]}"; do
        # Check if pattern or a parent pattern exists in gitignore
        if ! grep -qE "^${pattern}$|^\*\*/${pattern}$|^${pattern%/}/?\$" "$gitignore" 2>/dev/null; then
            # Also check for wildcard coverage
            local parent_dir=$(dirname "$pattern")
            if [ "$parent_dir" != "." ] && ! grep -qE "^${parent_dir}/?\$|^\*\*/${parent_dir}/?\$" "$gitignore" 2>/dev/null; then
                missing+=("$pattern")
            fi
        fi
    done

    if [ ${#missing[@]} -eq 0 ]; then
        echo -e "${GREEN}[OK]${NC} All required patterns in .gitignore"
    else
        for pattern in "${missing[@]}"; do
            echo -e "${RED}[MISSING]${NC} $pattern not in .gitignore"
            GITIGNORE_ISSUES=$((GITIGNORE_ISSUES + 1))
        done
    fi

    # Check for unignored .claude files that contain dangerous content
    echo ""
    echo "Scanning for dangerous unignored .claude files..."

    if [ -d "$TARGET_DIR/.claude" ]; then
        # Check if this is a valid git repo (not just a hooks folder)
        local is_valid_git=false
        if git -C "$TARGET_DIR" rev-parse --git-dir >/dev/null 2>&1; then
            is_valid_git=true
        fi

        while IFS= read -r file; do
            [ -z "$file" ] && continue
            [ -f "$file" ] || continue

            local is_ignored=false

            # Check if file is ignored
            if [ "$is_valid_git" = true ]; then
                # Valid git repo - use git check-ignore
                if git -C "$TARGET_DIR" check-ignore -q "$file" 2>/dev/null; then
                    is_ignored=true
                fi
            else
                # Not a valid git repo - check gitignore patterns manually
                local gitignore="$TARGET_DIR/.gitignore"
                if [ -f "$gitignore" ]; then
                    local relpath=${file#$TARGET_DIR/}
                    local dirpath=$(dirname "$relpath")
                    # Check various gitignore pattern formats
                    if grep -qE "^${relpath}$|^\*\*/${relpath}$|^${dirpath}/$|^\*\*/${dirpath}/$" "$gitignore" 2>/dev/null; then
                        is_ignored=true
                    fi
                fi
            fi

            # If not ignored, check for dangerous content
            if [ "$is_ignored" = false ]; then
                for pattern in "${DANGEROUS_CLAUDE_PATTERNS[@]}"; do
                    if grep -qiE "$pattern" "$file" 2>/dev/null; then
                        echo -e "${RED}[DANGER]${NC} $file contains '$pattern' but is NOT gitignored"
                        GITIGNORE_ISSUES=$((GITIGNORE_ISSUES + 1))
                        break
                    fi
                done
            fi
        done < <(find "$TARGET_DIR/.claude" -type f \( -name "*.json" -o -name "*.sh" -o -name "*.md" \) 2>/dev/null)
    fi

    echo ""
}

fix_gitignore() {
    local gitignore="$TARGET_DIR/.gitignore"

    echo -e "${BLUE}[AUTO-FIX GITIGNORE]${NC}"

    # Create gitignore if missing
    if [ ! -f "$gitignore" ]; then
        touch "$gitignore"
        echo "Created .gitignore"
    fi

    # Check if Claude section exists
    if ! grep -q "# Claude Code / AI tooling" "$gitignore" 2>/dev/null; then
        echo "" >> "$gitignore"
        echo "# Claude Code / AI tooling - DO NOT COMMIT" >> "$gitignore"
    fi

    local added=0

    for pattern in "${REQUIRED_IGNORES[@]}"; do
        if ! grep -qE "^${pattern}$|^\*\*/${pattern}$" "$gitignore" 2>/dev/null; then
            echo "$pattern" >> "$gitignore"
            echo -e "${GREEN}[ADDED]${NC} $pattern"
            added=$((added + 1))
        fi
    done

    # Add wildcard versions for nested projects
    for pattern in "${REQUIRED_IGNORES[@]}"; do
        local wildcard="**/$pattern"
        if ! grep -qE "^\*\*/${pattern}$" "$gitignore" 2>/dev/null; then
            echo "$wildcard" >> "$gitignore"
            added=$((added + 1))
        fi
    done

    if [ $added -eq 0 ]; then
        echo "No changes needed - .gitignore already complete"
    else
        echo ""
        echo -e "${GREEN}Added $added entries to .gitignore${NC}"
    fi

    echo ""
}

# ============================================
# PART 2: INTRUDER SCANNING
# ============================================

# Critical patterns - high confidence contributor indicators
CRITICAL_PATTERNS=(
    'co-authored-by[[:space:]]*:'
    'co-author[[:space:]]*:'
)

# AI attribution patterns - ONLY match actual authorship claims
# NOT descriptions of AI features or documentation about AI
AI_CRITICAL_PATTERNS=(
    'generated[[:space:]]by[[:space:]]claude[[:space:]]code'
    'generated[[:space:]]by[[:space:]]gpt-[0-9]'
    'generated[[:space:]]by[[:space:]]copilot'
    'written[[:space:]]by[[:space:]]claude'
    'written[[:space:]]by[[:space:]]chatgpt'
    'written[[:space:]]by[[:space:]]gpt'
)

EMAIL_PATTERN='[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

log_issue() {
    local severity="$1"
    local file="$2"
    local line_num="$3"
    local pattern="$4"
    local content="$5"

    if [ "$severity" = "CRITICAL" ]; then
        echo -e "${RED}[CRITICAL]${NC} $file:$line_num"
    else
        echo -e "${YELLOW}[WARNING]${NC} $file:$line_num"
    fi
    echo -e "  Pattern: $pattern"
    echo -e "  Content: ${content:0:100}"
    echo ""
    FOUND_ISSUES=$((FOUND_ISSUES + 1))
}

should_skip_file() {
    local file="$1"

    # Skip this scanner script itself
    [[ "$file" == *"scan-contributors.sh" ]] && return 0

    # Skip minified/map/lock files
    [[ "$file" == *.min.js ]] && return 0
    [[ "$file" == *.min.css ]] && return 0
    [[ "$file" == *.bundle.js ]] && return 0
    [[ "$file" == *.map ]] && return 0
    [[ "$file" == *package-lock.json ]] && return 0
    [[ "$file" == *yarn.lock ]] && return 0
    [[ "$file" == *Cargo.lock ]] && return 0

    # Skip audit/security scripts
    [[ "$file" == *audit*.sh ]] && return 0
    [[ "$file" == *security-scan*.sh ]] && return 0
    [[ "$file" == *pre-push ]] && return 0
    [[ "$file" == *post-commit ]] && return 0

    return 1
}

scan_file() {
    local file="$1"

    should_skip_file "$file" && return
    [ -r "$file" ] || return

    SCAN_COUNT=$((SCAN_COUNT + 1))

    # Skip binary files
    file "$file" 2>/dev/null | grep -q "binary" && return

    # Critical patterns
    for pattern in "${CRITICAL_PATTERNS[@]}"; do
        while IFS=: read -r line_num content; do
            [ -z "$line_num" ] && continue
            # Skip if only contains allowed name/email
            if echo "$content" | grep -qi "$ALLOWED_NAME\|$ALLOWED_EMAIL"; then
                other_emails=$(echo "$content" | grep -oiE "$EMAIL_PATTERN" | grep -vi "$ALLOWED_EMAIL" || true)
                [ -z "$other_emails" ] && continue
            fi
            log_issue "CRITICAL" "$file" "$line_num" "$pattern" "$content"
        done < <(grep -niE "$pattern" "$file" 2>/dev/null || true)
    done

    # AI patterns
    for pattern in "${AI_CRITICAL_PATTERNS[@]}"; do
        while IFS=: read -r line_num content; do
            [ -z "$line_num" ] && continue
            # Skip detection/rule code
            echo "$content" | grep -qiE "(detect|check|scan|rule|pattern|grep|match|block|strip)" && continue
            # Skip AI feature descriptions
            echo "$content" | grep -qiE "ai-generated[[:space:]]+(topolog|model|content|image|text|data|response|output)" && continue
            # Skip Maestro auto-generated headers
            echo "$content" | grep -qiE "auto-generated by claude maestro" && continue
            # Skip AI-assisted in descriptions (not attribution)
            echo "$content" | grep -qiE '"description".*ai-assisted' && continue
            log_issue "CRITICAL" "$file" "$line_num" "AI: $pattern" "$content"
        done < <(grep -niE "$pattern" "$file" 2>/dev/null || true)
    done

    # Unauthorized emails in author contexts
    while IFS=: read -r line_num content; do
        [ -z "$line_num" ] && continue
        email=$(echo "$content" | grep -oE "$EMAIL_PATTERN" | head -1)
        if [ -n "$email" ] && [ "$email" != "$ALLOWED_EMAIL" ]; then
            echo "$email" | grep -qiE "(example\.com|test\.com|localhost|noreply|users\.noreply\.github|company\.com)" && continue
            log_issue "WARNING" "$file" "$line_num" "Unauthorized email in author context" "$content"
        fi
    done < <(grep -niE "(^[[:space:]]*(author|by|contributor)[[:space:]]*[=:]|co-authored).*$EMAIL_PATTERN" "$file" 2>/dev/null || true)
}

scan_for_intruders() {
    echo -e "${BLUE}[INTRUDER SCAN]${NC}"
    echo "Scanning for unauthorized contributors..."
    echo ""

    cd "$TARGET_DIR"

    # Git-aware scanning
    if [ -d ".git" ]; then
        echo "Mode: Git-aware (tracked + untracked non-ignored files)"
        echo ""

        while IFS= read -r file; do
            [ -z "$file" ] && continue
            [ -f "$file" ] || continue
            scan_file "$file"
        done < <(git ls-files --cached --others --exclude-standard 2>/dev/null)

        # Git history
        echo "Scanning git history..."

        CO_AUTH_COMMITS=$(git log --all --format="%h %s" --grep="Co-Authored-By" -i 2>/dev/null | head -10 || true)
        if [ -n "$CO_AUTH_COMMITS" ]; then
            echo -e "${RED}[GIT CRITICAL]${NC} Commits with Co-Authored-By:"
            echo "$CO_AUTH_COMMITS"
            echo ""
            FOUND_ISSUES=$((FOUND_ISSUES + 1))
        fi

        UNAUTH_AUTHORS=$(git log --all --format="%an <%ae>" 2>/dev/null | sort -u | grep -v "$ALLOWED_NAME" | grep -v "^$" || true)
        if [ -n "$UNAUTH_AUTHORS" ]; then
            echo -e "${RED}[GIT CRITICAL]${NC} Unauthorized authors in history:"
            echo "$UNAUTH_AUTHORS"
            echo ""
            FOUND_ISSUES=$((FOUND_ISSUES + 1))
        fi
    else
        echo "Mode: Full scan (no git repo)"
        echo ""
        while IFS= read -r -d '' file; do
            scan_file "$file"
        done < <(find . -type f \( -name "*.md" -o -name "*.txt" -o -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.json" -o -name "*.yaml" -o -name "*.sh" \) -not -path "*/.git/*" -not -path "*/node_modules/*" -print0 2>/dev/null)
    fi

    echo ""
}

# ============================================
# MAIN
# ============================================

echo "=========================================="
echo " Contributor Scanner v0.1.1"
echo "=========================================="
echo "Target: $TARGET_DIR"
echo "Allowed: $ALLOWED_NAME <$ALLOWED_EMAIL>"
echo ""

case "$MODE" in
    --verify)
        verify_gitignore
        ;;
    --scan)
        scan_for_intruders
        ;;
    --fix)
        fix_gitignore
        verify_gitignore
        ;;
    both|*)
        verify_gitignore
        scan_for_intruders
        ;;
esac

# Summary
echo "=========================================="
TOTAL_ISSUES=$((FOUND_ISSUES + GITIGNORE_ISSUES))

if [ "$MODE" != "--verify" ]; then
    echo "Files scanned: $SCAN_COUNT"
fi
echo "Intruder issues: $FOUND_ISSUES"
echo "Gitignore issues: $GITIGNORE_ISSUES"
echo ""

if [ $TOTAL_ISSUES -eq 0 ]; then
    echo -e "${GREEN}Status: CLEAN - No issues found${NC}"
    exit 0
else
    echo -e "${RED}Status: $TOTAL_ISSUES issue(s) found${NC}"
    if [ $GITIGNORE_ISSUES -gt 0 ]; then
        echo ""
        echo "Run with --fix to auto-add missing gitignore entries"
    fi
    exit 1
fi
