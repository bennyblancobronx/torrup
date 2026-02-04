---
name: darules
version: 0.1.5
description: >
  Audit changes against The Rules. Runs mechanical checks via script, then
  walks each applicable rule with evidence-based pass/fail reporting.
  Auto-fixes documentation gaps (changelog, techguide, contracts) when detected.
  One contributor only: bennyblancobronx. No exceptions. No skipping.
  Commits to GitHub by default. Use when the user says /darules.
---

# darules -- Rules Compliance Audit + Cleanup

Check that changes follow every applicable rule in darules.md. Default mode includes full cleanup workflow.

## Usage

```
/darules              -- FULL WORKFLOW: audit, cleanup contributors, run hooks, commit to git
/darules nogit        -- RULES ONLY: audit and score without any git operations
/darules <file>       -- audit a specific file or path (with git ops)
/darules staged       -- audit only staged changes (with git ops)
/darules full         -- audit entire project (with git ops)
/darules --push       -- full workflow + push to remote
/darules --pr         -- full workflow + push + create PR
```

**Flags can be combined with scope:**
```
/darules staged --push    -- audit staged, cleanup, commit and push
/darules nogit full       -- audit entire project, scoring only (no git)
```

---

## Workflow

### 0. Load Context + Mode Detection

1. Read `darules.md` (in this skill's directory) to load the current ruleset
2. Read `about.md` and `contracts.md` if they exist in the target project
3. **Detect mode:**
   - `nogit` argument present = **Rules Only Mode** (steps 1-5 only, skip all git operations)
   - No `nogit` = **Full Workflow Mode** (all steps including cleanup and commit)

### 1. Determine Scope

| Argument | Scope |
|----------|-------|
| (none) | `git diff` -- staged + unstaged changes |
| `nogit` | Same as (none) but skip git operations |
| `staged` | `git diff --cached` only |
| `<file>` | That specific file/path |
| `full` | All tracked files in the project |

Collect:
- List of changed/target files
- The actual diff content (for line-level evidence)
- Recent commit messages (last 5) if commits are in scope

### 2. Classify Change Type

Tag the change set with all that apply:

| Tag | Triggered by |
|-----|-------------|
| `code` | .js, .ts, .py, .sh, .go, .rs, .swift, .rb, .php, .java, .c, .cpp, .cs, .ex, .kt, or similar |
| `docs` | .md files, comments-only changes |
| `config` | .json, .yaml, .yml, .toml, .env*, .ini, config files |
| `ui` | .html, .css, .scss, .jsx, .tsx, .vue, .svelte, templates |
| `test` | files in test/, tests/, __tests__/, spec/, or *test*/*spec* naming |
| `commit` | commit messages are in scope |
| `db` | migrations, schema files, .sql |
| `script` | files in scripts/, .sh files, Makefile |

### 3. Run Mechanical Checks

Run the audit script first to get deterministic results:

```bash
bash <skill-dir>/scripts/audit.sh [scope-args]
```

The script checks:
- File line counts (rule 8: under 400 lines)
- Emoji detection (rule 23)
- Root-level working files (rule 13)
- Secrets/env files (rule 10)
- AI mentions in commit messages (rule 24)

Parse the script output -- each line is `PASS|FAIL|SKIP rule_number description [details]`.

### 4. Check Judgment Rules

For each rule in darules.md, check applicability then evaluate:

**Rule applicability by change type:**

| Rule | code | docs | config | ui | test | commit | db | script |
|------|------|------|--------|-----|------|--------|-----|--------|
| 1. Read about.md/contracts.md first | all | all | all | all | all | - | all | all |
| 2. Read code before modifying | x | - | - | x | x | - | x | x |
| 3. Prioritize existing tools | x | - | - | x | - | - | - | x |
| 4. Keep it simple | x | - | x | x | x | - | x | x |
| 5. Plan before non-trivial changes | x | - | - | x | - | - | x | x |
| 6. Implement only what was asked | x | - | - | x | x | - | x | x |
| 7. Ask for UI mockups if unclear | - | - | - | x | - | - | - | - |
| 8. Files under 400 lines | SCRIPT | SCRIPT | SCRIPT | SCRIPT | SCRIPT | - | SCRIPT | SCRIPT |
| 9. No unnecessary dependencies | x | - | x | x | - | - | - | x |
| 10. No hardcoded secrets | SCRIPT | - | SCRIPT | SCRIPT | SCRIPT | - | SCRIPT | SCRIPT |
| 11. No silent error swallowing | x | - | - | x | x | - | - | x |
| 12. No credential modification | - | - | - | - | - | - | x | - |
| 13. No root-level working files | SCRIPT | SCRIPT | SCRIPT | SCRIPT | SCRIPT | - | SCRIPT | SCRIPT |
| 14. Small testable steps | x | - | - | x | x | - | x | x |
| 15. Test after every change | x | - | - | x | - | - | x | x |
| 16. Revert when stuck | x | - | - | x | - | - | - | x |
| 17. Re-read contracts before scope changes | x | x | x | x | - | - | x | x |
| 18. Update changelog/techguide/contracts | x | x | x | x | - | - | x | x |
| 19. Separate version per script/app | - | - | - | - | - | - | - | x |
| 20. Patch-level version bumps only | x | x | x | x | - | - | - | x |
| 21. Commit after each working change | - | - | - | - | - | x | - | - |
| 22. No destructive ops without confirm | - | - | - | - | - | - | x | x |
| 23. No emojis | SCRIPT | SCRIPT | SCRIPT | SCRIPT | SCRIPT | SCRIPT | SCRIPT | SCRIPT |
| 24. No AI mentions | SCRIPT | SCRIPT | SCRIPT | SCRIPT | SCRIPT | SCRIPT | SCRIPT | SCRIPT |
| 25. Explain changes in plain language | x | x | - | x | - | x | - | x |

Rules marked `SCRIPT` are handled by step 3. Rules marked `-` are skipped for that change type. Rules marked `x` require judgment evaluation.

For each applicable judgment rule:
1. Read the relevant changed files/diffs
2. Evaluate against the rule
3. Record PASS, FAIL, or WARN with specific evidence (file:line or description)

### 5. Generate Report

Output format:

```
DARULES AUDIT -- [scope description]
Files checked: N | Change types: [tags]

MECHANICAL CHECKS
  [PASS] Rule 8:  Files under 400 lines
  [FAIL] Rule 23: No emojis -- README.md:47 contains emoji
  [SKIP] Rule 24: No AI mentions -- no commits in scope

JUDGMENT CHECKS
  [PASS] Rule 2:  Read code before modifying
  [WARN] Rule 5:  Plan before non-trivial changes -- 4 files modified, no plan visible in conversation
  [FAIL] Rule 6:  Implement only what was asked -- utils/helpers.ts added but not in requirements
  [SKIP] Rule 7:  Ask for UI mockups -- no UI changes

SUMMARY
  Passed: 18 | Failed: 2 | Warnings: 1 | Skipped: 4

  Failures:
    Rule 23: README.md:47 -- remove emoji from heading
    Rule 6:  utils/helpers.ts -- confirm this file was requested or remove it
```

Rules:
- PASS = fully compliant, cite evidence where helpful
- FAIL = clear violation, always cite file:line or specific evidence
- WARN = possible violation, needs human judgment
- SKIP = rule does not apply to this change type

### 6. No Auto-Fix (Except Documentation)

Report only for most violations. The user decides what to act on.

**Exception: Rule 18 (Documentation Updates)** -- If the audit detects that changelog.md, techguide.md, or contracts.md should have been updated but were not, proceed to step 7.

---

### 7. Auto-Fix Documentation (Rule 18)

When rule 18 violations are detected, automatically generate and apply missing documentation updates.

#### 7.1 Detection Criteria

| Doc File | Update Required When |
|----------|---------------------|
| `changelog.md` | Any code, config, script, or db change that affects functionality |
| `techguide.md` | Changes to core logic, CLI commands, APIs, or how things work |
| `contracts.md` | Changes to integrations, external dependencies, scope, or obligations |

#### 7.2 Auto-Update Workflow

1. **Analyze the changes** -- Read the diff to understand what was modified
2. **Check existing docs** -- Read current changelog.md, techguide.md, contracts.md
3. **Determine what needs updating:**
   - changelog.md: Always for functional changes (TL;DR style, one line per change)
   - techguide.md: Only if how-it-works changed (commands, logic, behavior)
   - contracts.md: Only if external interfaces/scope changed

4. **Generate updates:**
   - changelog.md: Add entry under current version with brief description of what changed
   - techguide.md: Update relevant sections describing new/changed behavior
   - contracts.md: Update affected integration points or scope definitions

5. **Apply updates** -- Use Edit tool to add the generated content

6. **Report what was updated:**
   ```
   AUTO-FIXED DOCUMENTATION
     [UPDATED] changelog.md -- added entry for [change summary]
     [UPDATED] techguide.md -- updated [section] with [description]
     [SKIPPED] contracts.md -- no integration changes detected
   ```

#### 7.3 Update Format Rules

- **changelog.md**: Follow existing format. Add under current version header. One line per logical change. No emojis. Example: `- Added validation for user input in auth module`
- **techguide.md**: Match existing section structure. Update in place, do not duplicate sections. Keep descriptions concise.
- **contracts.md**: Only add/modify entries for genuinely changed integrations or scope. Do not pad with unchanged items.

#### 7.4 When NOT to Auto-Update

- If the doc files do not exist in the project (report SKIP, do not create them)
- If the change is docs-only (no functional change to document)
- If the change is test-only with no behavior change
- If unable to determine what changed (report WARN, let user handle it)

---

### 8. Conversation Gap Detection

Scan the current conversation for decisions and changes that should be documented but are not yet captured in changelog.md, techguide.md, or contracts.md.

#### 8.1 What to Scan For

| Pattern | Indicates | Document In |
|---------|-----------|-------------|
| "we decided to...", "let's use...", "going with..." | Architecture decision | techguide.md |
| "added", "implemented", "created", "built" | New feature/capability | changelog.md |
| "fixed", "resolved", "patched", "corrected" | Bug fix | changelog.md |
| "changed the approach", "now uses X instead of Y" | Implementation change | techguide.md, changelog.md |
| "new command", "renamed", "deprecated", "removed" | API/CLI change | techguide.md, changelog.md |
| "integrates with", "calls", "depends on" | External dependency | contracts.md |
| "scope now includes", "out of scope" | Scope change | contracts.md |

#### 8.2 Gap Detection Workflow

1. **Review conversation context** -- Look for keywords and patterns above
2. **Extract undocumented items** -- List decisions/changes not in current docs
3. **Present findings to user:**
   ```
   CONVERSATION GAP DETECTION
     Found 3 potentially undocumented items:

     [GAP] "Added rate limiting to API endpoints" -- not in changelog.md
     [GAP] "Switched from REST to GraphQL for user service" -- not in techguide.md
     [GAP] "Now depends on Redis for caching" -- not in contracts.md

     Add these to documentation? [y/n]
   ```
4. **If user confirms** -- Add entries to appropriate doc files
5. **If user declines** -- Note as skipped and proceed

#### 8.3 Gap Detection Limitations

- Cannot access conversation history directly; relies on visible context
- May miss items discussed much earlier in long conversations
- When uncertain, ask user: "Were there other decisions made this session?"

---

### 9. Ghost Contributor Purge (Full Workflow Mode Only)

**SKIP this step if `nogit` mode is active.**

**BULLETPROOF RULE: One contributor only - bennyblancobronx. Everyone else is a ghost. No exceptions. No skipping.**

This step runs automatically and purges ALL ghost contributors from ALL files.

#### 9.1 Run Contributor Purge

Execute the contributor scanner in fix-all mode:

```bash
./scripts/scan-contributors.sh [project-dir] --fix-all
```

**What gets PURGED (no exceptions):**
- ALL external author/contributor lines with emails that aren't ours
- ALL AI attribution patterns

**Report format:**
```
GHOST PURGE
  [PURGED] README.md
  [PURGED] src/config.ts
  [PURGED] docs/setup.md
  Purged 3 file(s)
```

#### 9.2 No Skipping Policy

**DO NOT SKIP:**
- Third-party files - PURGE them
- Vendor code - PURGE it
- ChangeLog files - PURGE them
- External package files - PURGE them

If we never talked, you didn't contribute. Strip it.

#### 9.3 Run Project Update Scripts

Execute the cleanup and sync scripts:

```bash
# Run the master update script
./scripts/update-all.sh
```

**What update-all.sh does:**
1. `update-hooks.sh` - Syncs git hooks to all projects
2. `update-scripts.sh` - Distributes utility scripts (scan-contributors.sh)
3. `update-skills.sh` - Syncs Claude skills
4. `update-rules.sh` - Syncs project rules
5. `init-claude-flow.sh` - Initializes claude-flow in projects

**Report format:**
```
PROJECT UPDATE
  [RUN] update-all.sh
  [OK] Hooks updated
  [OK] Scripts synced
  [OK] Skills synced
  [OK] Rules synced
  [OK] Claude-flow initialized
```

#### 9.4 Verify Hooks Are Installed

Confirm the post-commit and pre-push hooks are in place:

```bash
# Check post-commit hook exists and has the right content

# Check pre-push hook exists
grep -q "scan-contributors" .git/hooks/pre-push
```

**If hooks missing:**
```
HOOKS CHECK
  [WARN] post-commit hook missing or outdated
  [FIX] Installing post-commit hook...
  [OK] Hooks verified
```

---

### 10. Safe Commit and Push (Default in Full Workflow Mode)

**SKIP this step if `nogit` mode is active.**

In Full Workflow Mode, commit changes to git by default. Add `--push` to also push to remote, or `--pr` to create a pull request.

| Mode | Behavior |
|------|----------|
| `/darules` | Commit locally only |
| `/darules --push` | Commit and push to remote |
| `/darules --pr` | Commit, push, and create PR |
| `/darules nogit` | No git operations at all |

#### 10.1 Pre-flight Checks

Run these checks before any commit/push operation:

| Check | Command | Action |
|-------|---------|--------|
| Changes exist | `git status` | ABORT if nothing to commit |
| Review staged | `git diff --cached` | Show what will be committed |
| Current branch | `git branch --show-current` | Note branch name in output |
| Remote tracking | `git rev-parse --abbrev-ref @{u}` | ABORT if no upstream configured |
| Remote ahead | `git fetch && git status -uno` | Prompt to pull/rebase if behind |

#### 10.2 Security Scan (BLOCK if found)

**NEVER commit if any of these are detected:**

| Pattern | Description |
|---------|-------------|
| `.env`, `*.env*` | Environment files (except .env.example) |
| `API_KEY`, `SECRET`, `PASSWORD`, `TOKEN`, `PRIVATE_KEY` | Secrets in file contents |
| `id_rsa`, `*.pem`, `*.key` | Private key files |
| `credentials.json`, `serviceAccount.json` | Credential files |
| Connection strings with passwords | `://user:pass@` patterns |

```
SECURITY SCAN
  [BLOCK] .env file detected -- cannot commit
  [BLOCK] src/config.ts:47 contains hardcoded API_KEY

  Commit ABORTED. Remove secrets before proceeding.
```

#### 10.3 Code Quality Warnings

**Ask before proceeding if found:**

| Pattern | Location | Concern |
|---------|----------|---------|
| `console.log`, `print()`, `debugger` | Non-test files | Debug code left in |
| `.only()`, `.skip()` | Test files | Tests will not run properly |
| Commented code blocks (>10 lines) | Any file | Dead code |
| `TODO`, `FIXME` | In the diff | Incomplete work |

```
CODE QUALITY WARNINGS
  [WARN] src/api.ts:23 -- console.log statement
  [WARN] tests/user.test.ts:45 -- .only() will skip other tests
  [WARN] src/utils.ts:78-92 -- 15 lines of commented code

  Proceed with commit? [y/n]
```

#### 10.4 Files to Never Stage

Automatically exclude from staging:

```
# Dependencies
node_modules/
__pycache__/
.venv/
vendor/

# Build outputs
dist/
build/
*.o
*.pyc

# IDE files (unless intentional)
.idea/
.vscode/settings.json

# OS files
.DS_Store
Thumbs.db
```

#### 10.5 Commit Message Generation

1. **Analyze actual changes** -- Read the diff to understand what changed
2. **Check for conventional commits** -- If repo uses them, follow the pattern
3. **Format:**
   - First line under 72 characters
   - Descriptive but concise
   - Reference issue numbers if apparent from branch name
4. **No AI attribution** -- Never mention Claude, AI, or generated

Example messages:
```
Update documentation per rules audit

Add rate limiting to API endpoints
Fix null check in user validation
Refactor auth module for clarity
```

#### 10.6 Execution Sequence

```
COMMIT AND PUSH
  [CHECK] Changes detected: 3 files modified
  [CHECK] Branch: feature/add-rate-limiting (not main)
  [CHECK] Upstream: origin/feature/add-rate-limiting
  [CHECK] Remote in sync

  [SCAN] Security scan passed
  [WARN] 1 code quality warning (user confirmed proceed)

  [STAGE] changelog.md
  [STAGE] techguide.md
  [STAGE] src/api.ts

  [COMMIT] a1b2c3d "Add rate limiting to API endpoints"
  [PUSH] Pushed to origin/feature/add-rate-limiting

  Summary: 3 files, +47/-12 lines
```

#### 10.7 PR Creation (--pr flag)

When `--pr` flag is used, create a pull request after pushing:

1. **Check for existing PR** -- `gh pr list --head <branch>`
2. **If no PR exists:**
   ```bash
   gh pr create --title "<commit message>" --body "<changelog entries>"
   ```
3. **Report PR URL:**
   ```
   [PR] Created: https://github.com/owner/repo/pull/123
   ```

#### 10.8 NEVER DO -- HARD RULES (NO EXCEPTIONS)

**CRITICAL: These are BLOCKING rules. NEVER bypass them. NEVER use workarounds.**

- **NEVER use `--no-verify`** -- If a hook fails, FIX THE HOOK. Do not bypass it.
- **NEVER use `--force` or `-f`** -- No force pushing, ever.
- **NEVER proceed if security scan finds issues** -- ABORT, do not offer override.
- **NEVER bypass pre-push hooks** -- They exist for a reason. Fix problems, don't skip them.
- **NEVER commit files matching .gitignore patterns**
- **NEVER include AI/Claude mentions in commit messages**

**If a hook has a syntax error:**
1. READ the hook file
2. FIX the syntax error
3. RE-RUN the push WITHOUT `--no-verify`

**If a hook blocks the push:**
1. READ the hook output to understand why
2. FIX the underlying issue (purge the files, fix the patterns, etc.)
3. RE-RUN the push WITHOUT `--no-verify`

**"The hook is broken" is NOT an excuse to use `--no-verify`. Fix the hook.**

---

## Rules

1. Always load the current darules.md at runtime -- never hardcode rules
2. Run the mechanical script before judgment checks
3. Every FAIL and WARN must include specific evidence (file:line, commit hash, or description)
4. Do not check rules that are not applicable to the change type
5. SKIP is not a failure -- it means the rule does not apply
6. When in doubt between PASS and WARN, use WARN
7. When in doubt between WARN and FAIL, use WARN
8. No emojis in output (rule 23 applies to the audit itself)
9. Do not suggest improvements beyond what the rules require
10. Keep the report concise -- one line per rule, details only on FAIL/WARN
11. Auto-fix rule 18 violations (missing doc updates) after reporting all other findings
12. When auto-fixing docs, match the existing format and style of each file
13. Report all auto-fix actions taken at the end of the audit output
14. Never proceed with commit/push if security scan finds secrets
15. Run conversation gap detection after auto-fix, before commit/push
16. Use explicit file paths when staging, never `git add -A` or `git add .`
17. Generate commit messages from actual diff content, not assumptions
18. **NEVER use --no-verify or --force** -- If hooks fail, FIX THEM. No exceptions. No bypassing.
19. **`nogit` mode skips steps 9-10** -- no contributor purge, no hooks, no commit
20. **PURGE ALL GHOST CONTRIBUTORS** -- no exceptions, no skipping, strip everything
21. **One contributor only: bennyblancobronx** -- if we never talked, you didn't contribute
22. **Never skip files** -- third-party, vendor, ChangeLog, external packages all get purged
23. **Always run update-all.sh** in full workflow mode to sync hooks and scripts

---

## Edge Cases

- **No changes detected**: Report "No changes in scope" and exit. Do not audit nothing.
- **darules.md not found**: Error and exit. Cannot audit without rules.
- **Not a git repo** (and no file specified): Error -- need either git or an explicit file target.
- **Binary files in diff**: Skip binary files, note them as skipped.
- **Very large diff** (50+ files): Run mechanical checks on all, but for judgment checks focus on the 10 most-changed files and note the rest were not individually reviewed.
- **Doc file missing**: If changelog.md/techguide.md/contracts.md does not exist, skip auto-fix for that file (do not create it).
- **Doc file already updated**: If the doc file was modified in the same changeset, do not auto-update it (it was already handled).
- **Cannot determine changes**: If the diff is unclear or too complex to summarize, report WARN and let user handle the doc update manually.
- **--push with no remote**: Error and exit. Cannot push without configured remote.
- **Security scan finds secrets**: ABORT immediately. Do not offer override.
- **gh CLI not installed** (for --pr): Error with instructions to install GitHub CLI.
- **PR already exists**: Report existing PR URL instead of creating duplicate.
- **Merge conflicts after pull**: Abort push, report conflict status, let user resolve.
- **No conversation context visible**: Skip gap detection, note in output.
- **User declines quality warnings**: Proceed with commit but log that warnings were acknowledged.
- **nogit mode**: Skip all git operations (steps 9-10), only output rules audit report.
- **scan-contributors.sh not found**: Warn and skip contributor scan, but continue with commit.
- **update-all.sh not found**: Warn and skip project update, but continue with commit.
- **Hooks not installed**: Install them as part of step 9, then proceed.

---

## Reference Files

| File | Content |
|------|---------|
| `darules.md` | The rules themselves (source of truth) |
| `references/scoping.md` | What counts as "non-trivial", "over-engineering", etc. |
| `references/examples.md` | Example violations and passes for ambiguous rules |
| `references/security-patterns.md` | Patterns for security scan (secrets, keys, credentials) |
| `scripts/audit.sh` | Mechanical checks script |
| `scripts/security-scan.sh` | Pre-commit security scanner |
