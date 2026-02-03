# Crisp Update Plan -- Phase 2: Implementation

Version: 0.2.0
Status: Complete -- implemented in 0.1.2, verified in 0.1.3
Companion: `crispupdate.md` (Phase 1: palette spec)

---

## 1. Files to Update

### Assets (full rewrite with new palette)

| File | Changes |
|------|---------|
| `assets/config/design-tokens.json` | All hex values. Schema unchanged (see section 5). Add top-level `"version": "0.2.0"` |
| `assets/config/tailwind.preset.js` | All color values. Structure unchanged (see section 6). Add version comment |
| `assets/css/design-system.css` | All CSS custom properties, both themes, badge/toast/status classes. Add version comment |
| `assets/config/stylelint.config.js` | Updated enforcement rules (see section 9) |

### Reference docs (update hardcoded hex values)

| File | Scope |
|------|-------|
| `references/colors.md` | Full rewrite. Remove Crisp Green. Add accent configurability note. |
| `references/buttons.md` | All 5 variants, every state, every hex, accent -> configurable |
| `references/forms.md` | All inputs/selects/checkboxes/radios/toggles, inline SVG data URIs |
| `references/navigation.md` | Sidebar, header, tabs, dropdowns, all dark mode |
| `references/overlays.md` | Modals, tooltips, toasts (new functional colors), empty/loading states |
| `references/data-display.md` | Tables, badges (add warning), status dots, avatars, dividers |
| `references/cards.md` | Base card, sizes, image cards, states, grid, all dark mode |
| `references/states.md` | Every interactive state for every component (highest hex density) |
| `references/dark-mode.md` | Elevation values, theme CSS, component adaptations, contrast table |
| `references/anti-patterns.md` | WRONG/CORRECT examples. #000 correct value now #1F1F1F |
| `references/decisions.md` | Hex values, "amber" -> "accent (configurable, default Gold #B9975C)" |
| `references/accessibility.md` | Focus color, contrast re-verification with new palette |
| `references/naming.md` | Add `badge-warning` pattern |
| `SKILL.md` | Quick reference hex, version bump in frontmatter |
| `about.md` | "amber accent" -> "configurable accent (Gold by default)", version bump |

No update needed: `references/responsive.md`, `references/spacing-and-tokens.md`, `references/typography.md`, `references/layouts.md` (verify no hardcoded hex), `references/philosophy.md` (no color references), `assets/css/fonts.css` (no colors).

### New files

| File | Purpose |
|------|---------|
| `references/brand.md` | Brand identity spec (see Phase 1, section 7) |
| `crisp.config.json` | Per-app accent config schema |
| `scripts/generate-accent.js` | Accent variant generator (see section 4) |
| `scripts/init.sh` | Project bootstrap (see section 7) |
| `scripts/migrate.sh` | Old hex find-and-replace helper (see section 8) |
| `research/design/DEPRECATED.md` | Historical reference notice |

---

## 2. Inline SVG Updates

These hardcoded colors inside SVG data URIs are easy to miss in find-and-replace:

### forms.md -- Checkbox checkmark

```
stroke='white' -> stroke='%23FFFBF7'
stroke='%230a0a0b' -> stroke='%231F1F1F'
```

### forms.md -- Select dropdown arrow

```
stroke='%235C5C58' -> stroke='%23454545'
```

These are URL-encoded hex inside `background-image: url("data:image/svg+xml,...")` strings.

---

## 3. Component Color Tables (Derived)

These tables derive from the main palette mapping. Use when updating component reference files.

### Badge Surfaces

| Status | Light BG | Light Text | Dark BG | Dark Text |
|--------|----------|------------|---------|-----------|
| success | rgba(40,103,54,0.10) | #173B1F | rgba(57,147,77,0.15) | #39934D |
| warning | rgba(168,134,43,0.10) | #6B5518 | rgba(212,173,74,0.15) | #D4AD4A |
| error | rgba(174,28,9,0.10) | #741306 | rgba(245,83,61,0.15) | #F5533D |
| info | rgba(73,105,110,0.10) | #314649 | rgba(145,177,182,0.15) | #91B1B6 |
| accent | rgba(185,151,92,0.10) | #725A31 | rgba(212,191,155,0.15) | #D4BF9B |

### Toast Colors

| Type | Light BG | Light Text | Dark BG | Dark Text |
|------|----------|------------|---------|-----------|
| success | rgba(40,103,54,0.10) | #173B1F | rgba(57,147,77,0.15) | #39934D |
| warning | rgba(168,134,43,0.10) | #6B5518 | rgba(212,173,74,0.15) | #D4AD4A |
| error | rgba(174,28,9,0.10) | #741306 | rgba(245,83,61,0.15) | #F5533D |
| info | rgba(73,105,110,0.10) | #314649 | rgba(145,177,182,0.15) | #91B1B6 |
| neutral | #454545 | #FFFBF7 | #4A4A4A | rgba(255,251,247,0.87) |

### Status Indicator Dots

| Status | Hex |
|--------|-----|
| neutral | #7A7A7A |
| success | #286736 |
| warning | #A8862B |
| error | #AE1C09 |
| info | #49696E |

### Hover/Active Overlays

| State | Light | Dark |
|-------|-------|------|
| hover | rgba(0,0,0,0.03) | rgba(255,255,255,0.05) |
| selected | rgba(0,0,0,0.05) | rgba(255,255,255,0.08) |
| active | rgba(0,0,0,0.05) | rgba(255,255,255,0.08) |
| backdrop | rgba(0,0,0,0.50) | rgba(0,0,0,0.70) |

Dark mode overlays unchanged but verify visually on #1F1F1F canvas.

---

## 4. generate-accent.js Specification

All color math uses OKLCH (CSS Color Level 4). OKLCH preserves perceptual uniformity -- equal lightness steps look consistent across hues. HSL is not acceptable.

### Input

One required arg: 6-digit hex. Validated with `/^#?[0-9a-fA-F]{6}$/`. Optional `--name "Camel"`.

### Derivation rules

| Output | Rule |
|--------|------|
| accent | Input hex unchanged |
| accent-hover | OKLCH lightness -15% |
| accent-surface | rgba(input, 0.10) on #fff8f2 |
| accent-surface-dark | rgba(input, 0.15) on #1F1F1F |
| accent-foreground | #1F1F1F if OKLCH L > 0.55, else rgba(255,251,247,0.87) |
| accent-dark | OKLCH lightness +15% |
| accent-hover-dark | Input hex |

### Contrast validation

1. `accent` vs #fff8f2 -- must pass 3:1 (UI components)
2. `accent-dark` vs #1F1F1F -- must pass 3:1
3. `accent-foreground` vs `accent` -- must pass 4.5:1 (text on button fill)

Uses WCAG 2.1 relative luminance (sRGB). If any check fails, exit code 1. `--force` overrides.

### Edge cases

- Very light accent: if hover still fails 3:1, darken further in 5% steps
- Very dark accent: if dark variant fails 3:1 on #1F1F1F, lighten in 5% steps
- Pure gray: warn that it is visually indistinct from locked neutrals

### Output

Writes three files: `accent-tokens.json`, `accent-vars.css`, `accent-tailwind.js`. Dependencies: Node 18+, `culori` (MIT, <50KB devDependency).

---

## 5. design-tokens.json Schema

No keys added or removed. Schema structure identical between 0.1.x and 0.2.0. Pure value replacement. One addition: top-level `"version": "0.2.0"` field outside `crisp` object.

See Phase 1 section 2 for the complete old-to-new value mapping.

---

## 6. Tailwind Preset Changes

Structure unchanged. All functional color groups already exist with `DEFAULT`, `surface`, `foreground`. Values replaced per Phase 1 section 2. Surface values use rgba (Tailwind handles it, matches token file).

---

## 7. Project Bootstrap Script

`scripts/init.sh`:

```
Usage: ./init.sh /path/to/project [--accent "#B9975C"]

1. Creates /path/to/project/crisp/
2. Copies fonts (woff2) and fonts.css
3. Runs generate-accent.js with provided accent (or default Gold)
4. Outputs design-system.css, tailwind.preset.js, design-tokens.json with accent baked in
5. Prints setup instructions (@import paths, Tailwind config)
```

`--accent` is the only flag. Omit for Gold default.

---

## 8. Migration Path for Existing Apps

No schema changes. Token key names, CSS property names, and Tailwind class names are all identical. Apps using `var()` tokens or Tailwind classes need zero code changes.

Breaking only for hardcoded hex values. Add `scripts/migrate.sh`:

```
Usage: ./migrate.sh /path/to/project [--dry-run]

Scans .css/.html/.svelte/.tsx/.jsx/.vue files.
Reports each old hex with file, line, suggested replacement.
--dry-run: report only. Without: performs sed replacements.
```

Key replacements: `#FAFAF8->#fff8f2`, `#1C1C1A->#1F1F1F`, `#f59e0b->#B9975C`, `#22c55e->#286736`, `#ef4444->#AE1C09`, `#3b82f6->#49696E`, `#0a0a0b->#1F1F1F`, plus all dark mode elevation values. Warns on ambiguous matches (e.g., `#FFFFFF`). Skips fonts, images, node_modules.

---

## 9. Stylelint Changes

### Add plugin for token enforcement

```js
plugins: ['stylelint-declaration-strict-value'],
```

Force all color properties to use `var()` instead of raw hex. Exclude `design-system.css` from linting (it defines the raw values).

### Add font-weight 600 block

```js
'font-weight': ['600', 'semibold'],  // in disallowed list
```

### Add font-family enforcement

```js
'font-family-no-missing-generic-family-keyword': null,
'declaration-property-value-allowed-list': {
  'font-family': ["/CrispByYosi/", "inherit", "unset"],
},
```

---

## 10. research/design/ Disposition

All files superseded by `skills/crisp/`. Add `research/design/DEPRECATED.md` noting canonical source. Do not update old files with new colors.

---

## 11. Version Bumps

| File | Location | From | To |
|------|----------|------|----|
| `SKILL.md` | Frontmatter `metadata.version` | 0.1.1 | 0.2.0 |
| `about.md` | Line 28 | 0.1.1 | 0.2.0 |
| `design-tokens.json` | New top-level field | (none) | 0.2.0 |
| `design-system.css` | Comment header | (none) | 0.2.0 |
| `tailwind.preset.js` | Comment header | (none) | 0.2.0 |
| `changelog.md` | New entry | (none) | 0.2.0 |

---

## 12. Changelog Entry (Draft)

```
## 0.2.0

Replaced color system with warm-neutral palette. Added configurable accent.

### What changed

- Background: #fff8f2 replacing #FAFAF8. Surface: #FFFBF7 replacing #F4F4F2
- Text: #1F1F1F / #454545 / #7A7A7A replacing #1C1C1A / #5C5C58 / #8A8A86
- Functional colors: muted earth tones replacing saturated Tailwind defaults
- Accent configurable per app (default Gold #B9975C, was amber #f59e0b)
- Removed "Crisp Green" alternative accent
- Dark mode canvas #1F1F1F (was #0a0a0b), elevation ramp adjusted
- Added brand identity reference, accent tooling, bootstrap and migration scripts
- Stricter stylelint enforcement

### Migration

Token key names, CSS property names, and Tailwind class names unchanged.
Only hardcoded hex values need updating. See scripts/migrate.sh.
```

---

## 13. Implementation Order

### Phase A: Verification (before touching files)

1. Run contrast verification on borderline combos with exact checker
2. Resolve border rgba to solid hex fallbacks (verify visually)
3. Verify dark mode overlays on #1F1F1F canvas

### Phase B: Core assets

4. Update `design-tokens.json` (all values, add version field)
5. Update `design-system.css` (all custom properties, both themes, component classes)
6. Update `tailwind.preset.js` (all color values)
7. Update `stylelint.config.js` (plugin, font rules, blocklist)

### Phase C: Reference docs

8. Rewrite `references/colors.md`
9. Update `references/dark-mode.md`
10. Update `references/buttons.md`
11. Update `references/forms.md` (including inline SVG data URIs)
12. Update `references/navigation.md`
13. Update `references/overlays.md`
14. Update `references/data-display.md`
15. Update `references/cards.md`
16. Update `references/states.md`
17. Update `references/anti-patterns.md`
18. Update `references/decisions.md`
19. Update `references/accessibility.md`
20. Update `references/naming.md`
21. Update `SKILL.md` (hex values + version bump)
22. Update `about.md` (wording + version bump)

### Phase D: New files

23. Create `references/brand.md`
24. Create `crisp.config.json`
25. Create `scripts/generate-accent.js`
26. Create `scripts/init.sh`
27. Create `scripts/migrate.sh`

### Phase E: Housekeeping

28. Add `research/design/DEPRECATED.md`
29. Re-verify accessibility contrast (full pass with new values in place)
30. Update `changelog.md`
31. Grep entire `skills/crisp/` for remaining old hex values
