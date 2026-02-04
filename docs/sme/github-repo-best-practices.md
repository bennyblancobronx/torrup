# GitHub Repository Best Practices - Core Files

> Researched: 2026-02-03 | Sources: 5 fetched, 5 cited

## Overview

A well-structured GitHub repository includes specific files that communicate project purpose, legal terms, contribution guidelines, and community standards. GitHub automatically recognizes and surfaces these files to visitors, linking them in relevant UI locations (issue creation, PR creation, repository insights).

These files can be placed in the repository root, `.github/` directory, or `docs/` directory. Files in `.github/` take precedence over root-level equivalents.

## Key Concepts

- **Community Health Files**: GitHub's term for standard files (README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY) that define project expectations
- **File Location Precedence**: `.github/` > root (`./`) > `docs/`
- **Default Files**: Organizations can create default community health files in a `.github` repository that apply to all repos lacking their own
- **Templates**: Issue and PR templates standardize contributor submissions

## Core Files and Contents

### Required (Tier 1)

| File | Purpose | Contents |
|------|---------|----------|
| **README.md** | Project introduction | What it does, why it matters, installation, usage, dependencies |
| **LICENSE** | Legal terms | Full license text (MIT, Apache, GPL, etc.). Must be at root for GitHub API |
| **.gitignore** | Exclude files | Patterns for build artifacts, secrets, IDE files, OS files |

### Strongly Recommended (Tier 2)

| File | Purpose | Contents |
|------|---------|----------|
| **CONTRIBUTING.md** | Contributor guide | How to report bugs, submit PRs, code style, testing requirements |
| **CODE_OF_CONDUCT.md** | Community standards | Behavioral expectations, enforcement, reporting process |
| **SECURITY.md** | Vulnerability reporting | Supported versions, how to report, response timeline |
| **CHANGELOG.md** | Change history | Version history, features, fixes, breaking changes |

### Recommended (Tier 3)

| File | Purpose | Contents |
|------|---------|----------|
| **CODEOWNERS** | Review automation | Path patterns mapped to reviewers (auto-requested on PRs) |
| **SUPPORT.md** | Help resources | Where to get help, linked on "New Issue" page |
| **FUNDING.yml** | Sponsorship | Sponsor button configuration |
| **.github/ISSUE_TEMPLATE/** | Issue templates | Bug report, feature request templates with required fields |
| **.github/PULL_REQUEST_TEMPLATE.md** | PR template | Checklist, description format, testing requirements |
| **.github/workflows/** | CI/CD | Automated testing, linting, deployment workflows |
| **.github/dependabot.yml** | Dependency updates | Automated security and version update PRs |

## Best Practices

1. **Always include a README** - Answer what, why, and how. Include installation, usage, and prerequisites.

2. **Choose a license explicitly** - No license means all rights reserved. Use MIT for permissive, Apache 2.0 for patent protection, GPL for copyleft.

3. **Enable GitHub security features** - Dependabot alerts, secret scanning, push protection, and code scanning are free for public repos.

4. **Use issue and PR templates** - Standardize submissions to get necessary information upfront.

5. **Keep CHANGELOG updated** - Use Keep a Changelog format. Document every release.

6. **Add CODEOWNERS for teams** - Automate review requests and clarify code ownership.

7. **Protect important branches** - Require PR reviews and status checks on main/master.

8. **Document security reporting** - Never let vulnerabilities be reported via public issues.

9. **Cross-reference related files** - Link SECURITY.md from CONTRIBUTING.md, link CONTRIBUTING.md from README.

10. **Use semantic versioning** - Follow SemVer for releases with git tags.

## Common Pitfalls

- **Missing LICENSE** - Code without a license cannot be legally used, modified, or distributed by others
- **Stale README** - Outdated installation or usage instructions frustrate users
- **No .gitignore** - Committed IDE files, secrets, or build artifacts pollute history
- **SECURITY.md without contact** - No way to privately report vulnerabilities
- **Monolithic CONTRIBUTING** - Too long; nobody reads it. Keep it focused.

## README Structure

A good README follows this pattern:

```markdown
# Project Name

One-line description.

## Features
- Feature 1
- Feature 2

## Prerequisites
- Dependency 1
- Dependency 2

## Installation
step-by-step commands

## Usage
basic examples

## Configuration
environment variables or config files

## Contributing
link to CONTRIBUTING.md

## License
license name with link to LICENSE file
```

## Sources

- [Best practices for repositories - GitHub Docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories) - Security features, collaboration approach, README importance
- [GitHub special files and paths](https://github.com/joelparkerhenderson/github-special-files-and-paths) - Comprehensive list of all special files and their locations
- [Creating default community health files - GitHub Docs](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file) - Organization-wide default files
- [Open Source Checklist - libresource](https://github.com/libresource/open-source-checklist) - Pre-launch checklist for open source projects
- [GitHub Repository Structure Best Practices - Medium](https://medium.com/code-factory-berlin/github-repository-structure-best-practices-248e6effc405) - File organization and structure
