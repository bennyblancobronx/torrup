---
name: sme
version: 0.1.4
description: "Subject Matter Expert - Deep-research any topic and produce a structured reference document with cited sources. Fetches docs from URLs and GitHub repos. Documents CLI commands, best practices, and key concepts. Use when the user says /sme, asks to research a topic, wants a reference guide built, or needs to pull and summarize external documentation."
---

# SME - Subject Matter Expert

Research a topic, fetch existing docs, and produce a clean reference .md with cited sources.

## Usage

```
/sme <topic or URL>
/sme <topic> <url>
```

**Examples:**
```
/sme kubernetes networking
/sme https://docs.docker.com/compose/
/sme terraform state management
/sme react server components https://react.dev/reference/rsc/server-components
```

---

## Workflow

### 0. Check Project Context

Before researching, read `about.md` and `contracts.md` (if they exist in the project root) to understand the project context. This may inform how the research is framed or what details matter most.

### 1. Parse Input

- **No arguments** -- show the usage examples and ask the user what they want to research. Do not proceed without a topic or URL.
- **Topic only** -- research via web search + fetch top results
- **URL only** -- fetch that document, identify the topic, supplement with search
- **Topic + URL** -- fetch URL as primary source, search for additional context
- **GitHub repo URL** -- detect and fetch repo metadata (stars, description, language) via `gh api`

### 2. Research

**For topics:**
1. Run 3-4 web searches with different angles:
   - `[topic] official documentation [current year]`
   - `[topic] best practices CLI commands`
   - `[topic] getting started tutorial`
   - `[topic] vs alternatives comparison [current year]`
2. Fetch the top 3-5 most relevant results
3. Extract: key concepts, CLI commands, config examples, best practices, pitfalls
4. Note any competing tools or alternatives that appear across multiple sources

**For URLs:**
1. Fetch with WebFetch
2. If GitHub URL and WebFetch fails, convert to raw or use `gh api`:
   ```bash
   gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | base64 -d
   ```
3. Run 1-2 supplemental searches for context

**For GitHub repos:**
1. Fetch repo metadata first:
   ```bash
   gh api repos/{owner}/{repo} --jq '{name,description,stargazers_count,language,license: .license.spdx_id,updated_at}'
   ```
2. Fetch README via `gh api repos/{owner}/{repo}/readme --jq '.content' | base64 -d`
3. Search for the project name + "tutorial" or "getting started" for supplemental context

### 3. Cross-Reference

Before writing, check key claims against sources:
- If a best practice or recommendation appears in only 1 source, note it as single-source
- If it appears in 2+ sources, state it with confidence
- If sources conflict, present both sides and note the disagreement

This is lightweight -- spend 30 seconds scanning, not re-researching.

### 4. Write Document

If `docs/sme/<topic-slug>.md` already exists, note the previous research date in the Overview section (e.g., "Previously researched: YYYY-MM-DD") and overwrite with fresh research.

Save to `docs/sme/<topic-slug>.md` using this structure:

```markdown
# <Topic Title>

> Researched: <today's actual date> | Sources: N fetched, M cited

## Overview
2-3 paragraphs. What this is, why it matters, where it fits.

## Key Concepts
- **Concept**: explanation
(as many as needed)

## CLI Commands / Usage
(only if applicable)
common commands with flags and examples in code blocks

## Alternatives / Comparison
(only if research surfaced competitors or alternatives)
brief table or bullet list comparing the topic to its main alternatives
include: what it does better, what it does worse, when to pick each

## Best Practices
numbered, concrete, actionable items

## Common Pitfalls
(only if research surfaced these)

## Configuration / Setup
(only if applicable)

## Sources
- [Title](url) - what was used from here
```

### 5. Update Changelog

Add a one-line entry to `changelog.md`: "SME: researched [topic]" with today's date.

### 6. Commit

Commit the new/updated doc and changelog entry with a plain-language message (e.g., "add sme research on [topic]").

### 7. Report Back

- File path
- 2-3 sentence summary
- Note any sources that were unavailable or conflicting

---

## Rules

1. **Always cite sources.** Every recommendation traces to a source at the bottom.
2. **Source hierarchy.** Official docs > GitHub repos/READMEs > reputable blogs (major tech publications) > community forums > random posts. When in doubt, prefer the source closer to the maintainers.
3. **Cross-reference before asserting.** Claims in 2+ sources get stated as fact. Single-source claims get qualified ("according to [source]"). Conflicting claims get both sides shown.
4. **Include CLI commands when they exist.** Most useful commands with examples.
5. **Keep it practical.** Things someone would actually use, not theory.
6. **No fluff.** No filler intros. Get to the point.
7. **Slug the filename.** "Kubernetes Networking" -> `kubernetes-networking.md`
8. **Create dirs.** `mkdir -p docs/sme/` before writing.
9. **Do not fabricate sources.** Only cite URLs that were actually fetched and read.
10. **Under 400 lines.** Focus on the most important 80%. Note exclusions.
11. **Never save to root.** All output goes to `docs/sme/`.
12. **No emojis.** Plain text only.
13. **Use today's date.** Replace any date placeholder with the actual current date, never leave YYYY-MM-DD literal.
14. **Overwrite stale files.** If the output file already exists, overwrite it with fresh research. Note the previous date in Overview.

---

## Fetching External Docs

### Regular URLs
```
WebFetch(url, "Extract key information, CLI commands, config examples, best practices")
```

### GitHub URLs
```bash
# Repo metadata (stars, description, language)
gh api repos/{owner}/{repo} --jq '{name,description,stargazers_count,language,license: .license.spdx_id,updated_at}'

# Repo file contents
gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | base64 -d

# README
gh api repos/{owner}/{repo}/readme --jq '.content' | base64 -d
```

### Multiple URLs
Fetch all in parallel (max 5 concurrent), synthesize into one document.

---

## Edge Cases

- **WebFetch fails on a non-GitHub URL** (paywall, rate limit, 403/404): Skip that source, note it as unavailable in the Sources section, and continue with remaining sources.
- **`gh` CLI not installed or not authenticated**: Fall back to WebFetch on the raw GitHub URL (`https://raw.githubusercontent.com/...`). If that also fails, note it and rely on web search results only.
- **All searches return irrelevant results**: Produce a shorter document with whatever was found. Add a note at the top: "Limited sources available -- findings below may be incomplete." Tell the user in the report.
- **Fewer than 2 credible sources found**: Still produce the document but qualify all claims as single-source. Flag this clearly in the report back to the user.
- **Topic is ambiguous** (e.g., "spring" could be Spring Framework or spring season): Ask the user to clarify before researching.
