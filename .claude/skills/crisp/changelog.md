# Changelog

## 0.1.4

Archived completed update planning docs.

### What changed

- Marked crispupdate.md and crispupdate-impl.md as complete (implemented in 0.1.2, verified in 0.1.3)
- Moved both files to archive/ -- planning work is done, no longer active

## 0.1.3

Verified contrast ratios with exact WCAG 2.1 calculations. Updated accessibility reference with measured values.

### What changed

- Replaced approximate contrast ratios (~) with exact calculated values in accessibility.md
- Documented #B9975C accent at 2.61:1 on canvas -- confirmed safe only as button fill, not as text on background
- #49696E (info) confirmed at 5.66:1 -- passes AA cleanly (was listed as borderline)
- #A8862B (warning) confirmed at 3.27:1 -- large text/UI only
- Dark mode muted text (38% opacity) confirmed at 3.48:1 -- large text/UI only
- Added note on accent contrast enforcement via generate-accent.js
- Version bump across all asset files

## 0.1.2

Replaced color system with warm-neutral palette. Added configurable accent.

### What changed

- Background: #fff8f2 replacing #FAFAF8. Surface: #FFFBF7 replacing #F4F4F2
- Text: #1F1F1F / #454545 / #7A7A7A replacing #1C1C1A / #5C5C58 / #8A8A86
- Functional colors: muted earth tones replacing saturated Tailwind defaults
- Accent configurable per app (default Gold #B9975C, was amber #f59e0b)
- Removed "Crisp Green" alternative accent
- Dark mode canvas #1F1F1F (was #0a0a0b), elevation ramp adjusted
- Added brand identity reference, accent tooling, bootstrap and migration scripts
- Stricter stylelint enforcement (token-only colors, font-weight 600 blocked, font-family enforced)
- Added badge-accent and toast-neutral variants
- Added status dot component classes to design-system.css
- Added destructive button to design-system.css

### Migration

Token key names, CSS property names, and Tailwind class names unchanged.
Only hardcoded hex values need updating. See scripts/migrate.sh.

### New files

- `references/brand.md` -- Brand identity spec
- `crisp.config.json` -- Per-app accent config
- `scripts/generate-accent.js` -- Accent variant generator
- `scripts/init.sh` -- Project bootstrap
- `scripts/migrate.sh` -- Old hex find-and-replace helper
- `research/design/DEPRECATED.md` -- Historical reference notice

## 0.1.1

Consolidated naming across the design system and font family.

### What changed

- Standardized skill directory name to `crisp`
- Renamed font to CrispByYosi across all 5 weight variants (full binary rename -- internal OpenType name table IDs 1, 4, 6, 16 rewritten via fonttools)
- Updated font-family in CSS, design tokens, and Tailwind preset
- Consolidated research file naming (`CRISP.md`, `crisp-design-language.md`)
- Updated references across 35 files
- No visual or behavioral changes -- same design system, cleaned up naming

## 0.1.0

Complete rebuild from v1.0.0. All design values preserved, no visual changes.

### What changed

- Rewrote all files from scratch (19 new reference files)
- Split `component-specs.md` (1,648 lines) into 6 component files by family
- Reduced `SKILL.md` from 610 lines to 236 lines (quick reference only)
- Brought all files under the 400-line limit
- Fixed frontmatter: moved `version` under `metadata.version`
- Archived original files to `archive/v1/`

### File structure

| Before | After |
|--------|-------|
| SKILL.md (610 lines) | SKILL.md (236 lines) |
| references/component-specs.md (1,648 lines) | references/buttons.md (243) |
| | references/forms.md (272) |
| | references/cards.md (115) |
| | references/navigation.md (240) |
| | references/overlays.md (251) |
| | references/data-display.md (251) |
| references/anti-patterns.md (543 lines) | references/anti-patterns.md (311) |
| references/layouts.md (581 lines) | references/layouts.md (308) |
| references/decision-trees.md (448 lines) | references/decisions.md (245) |
| references/dark-mode.md (339 lines) | references/dark-mode.md (207) |
| references/states.md (344 lines) | references/states.md (233) |
| (none) | references/philosophy.md (80) |
| (none) | references/typography.md (111) |
| (none) | references/colors.md (121) |
| (none) | references/spacing-and-tokens.md (126) |
| (none) | references/responsive.md (196) |
| (none) | references/accessibility.md (118) |
| (none) | references/naming.md (75) |

### Assets (unchanged)

- `assets/css/design-system.css`
- `assets/css/fonts.css`
- `assets/config/design-tokens.json`
- `assets/config/tailwind.preset.js`
- `assets/config/stylelint.config.js`
- `assets/fonts/CrispByYosi-*.woff2` (5 files)
