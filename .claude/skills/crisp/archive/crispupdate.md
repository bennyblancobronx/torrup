# Crisp Update Plan -- Phase 1: Palette Spec

Version: 0.2.0
Status: Complete -- implemented in 0.1.2, verified in 0.1.3
Companion: `crispupdate-impl.md` (Phase 2: implementation details)

---

## Summary

Replace the color system with an approved warm-neutral palette. Lock every color except the single configurable accent. Gold (Camel #B9975C) is the default. Every other color is locked and identical across all apps.

---

## 1. New Approved Color Palette

### Background

| Token | Hex | Name |
|-------|-----|------|
| background | #fff8f2 | Background White |

Replaces #FAFAF8. Warmer tone throughout.

### Gray/Black (Locked)

| Variant | Hex | Name | Use |
|---------|-----|------|-----|
| main | #454545 | Gunmetal | Primary text, primary button fill |
| light | #7A7A7A | Grey | Secondary text, muted text, captions |
| dark | #1F1F1F | Carbon Black | Dark mode canvas, headings on light |

### White (Locked)

| Variant | Hex | Name | Use |
|---------|-----|------|-----|
| main | #FFFBF7 | Porcelain | Cards, panels, surface |
| light | #FFFBF7 | Porcelain | Modals, dropdowns, surface-elevated |
| dark | #FFEBD6 | Antique White | Warm tint backgrounds, accent surfaces |

### Gold (Default Accent -- CONFIGURABLE PER APP)

| Variant | Hex | Name | Use |
|---------|-----|------|-----|
| main | #B9975C | Camel | Accent, focus rings, CTA button |
| light | #D4BF9B | Pale Oak | Accent surface (light mode badges) |
| dark | #725A31 | Olive Bark | Accent hover, accent on dark mode |

### Red (Error / Destructive -- Locked)

| Variant | Hex | Name | Use |
|---------|-----|------|-----|
| main | #AE1C09 | Oxidized Iron | Error text, error borders |
| light | #F5533D | Tomato | Error surface foreground (dark mode) |
| dark | #741306 | Molten Lava | Error surface foreground (light mode) |

### Green (Success / Verified -- Locked)

| Variant | Hex | Name | Use |
|---------|-----|------|-----|
| main | #286736 | Dark Emerald | Success text, success borders |
| light | #39934D | Sea Green | Success surface foreground (dark mode) |
| dark | #173B1F | Deep Forest | Success surface foreground (light mode) |

### Yellow (Warning / Caution -- Locked)

| Variant | Hex | Name | Use |
|---------|-----|------|-----|
| main | #A8862B | Raw Sienna | Warning text, warning borders |
| light | #D4AD4A | Harvest Gold | Warning surface foreground (dark mode) |
| dark | #6B5518 | Bronze | Warning surface foreground (light mode) |

### Blue (Info / Neutral Highlight -- Locked)

| Variant | Hex | Name | Use |
|---------|-----|------|-----|
| main | #49696E | Blue Slate | Info text, info borders |
| light | #91B1B6 | Cool Steel | Info surface foreground (dark mode) |
| dark | #314649 | Dark Slate Gray | Info surface foreground (light mode) |

### Orange (Reserved -- Not Active by Default)

Not included in default tokens. Add to a project only if a sixth functional color is needed.

| Variant | Hex | Name |
|---------|-----|------|
| main | #9E5A2A | Burnt Copper |
| light | #C4835A | Clay |
| dark | #6A3B19 | Umber |

---

## 2. Token Mapping (Old to New)

### Light Mode

| Token | Old | New | Source |
|-------|-----|-----|--------|
| canvas | #FAFAF8 | #fff8f2 | Background White |
| surface | #F4F4F2 | #FFFBF7 | Porcelain |
| surface-elevated | #FFFFFF | #FFFBF7 | Porcelain (no pure white) |
| text | #1C1C1A | #1F1F1F | Carbon Black |
| text-secondary | #5C5C58 | #454545 | Gunmetal |
| text-muted | #8A8A86 | #7A7A7A | Grey |
| text-disabled | #C0BFBC | rgba(122,122,122,0.50) | Grey at 50% |
| border | #E2E1DE | rgba(212,191,155,0.40) | Pale Oak at 40% |
| border-emphasis | #C0BFBC | rgba(122,122,122,0.40) | Grey at 40% |
| border-subtle | #EEEEED | rgba(255,235,214,0.50) | Antique White at 50% |
| accent | #f59e0b | #B9975C | Camel (configurable) |
| accent-hover | #d97706 | #725A31 | Olive Bark (configurable) |
| accent-surface | #fef3c7 | #FFEBD6 | Antique White (configurable) |
| accent-foreground | (implicit) | #1F1F1F | Carbon Black (auto-derived) |
| success | #22c55e | #286736 | Dark Emerald |
| success-foreground | #166534 | #173B1F | Deep Forest |
| success-surface | #dcfce7 | rgba(40,103,54,0.10) | Dark Emerald at 10% |
| warning | #eab308 | #A8862B | Raw Sienna |
| warning-foreground | (none) | #6B5518 | Bronze |
| warning-surface | (none) | rgba(168,134,43,0.10) | Raw Sienna at 10% |
| error | #ef4444 | #AE1C09 | Oxidized Iron |
| error-foreground | #991b1b | #741306 | Molten Lava |
| error-surface | #fee2e2 | rgba(174,28,9,0.10) | Oxidized Iron at 10% |
| info | #3b82f6 | #49696E | Blue Slate |
| info-foreground | #1e40af | #314649 | Dark Slate Gray |
| info-surface | #dbeafe | rgba(73,105,110,0.10) | Blue Slate at 10% |

Borders use opacity blending against #fff8f2. Solid hex fallbacks for non-alpha contexts:

| Token | rgba | Approx Solid Hex |
|-------|------|-------------------|
| border | rgba(212,191,155,0.40) | #EDE3D4 |
| border-emphasis | rgba(122,122,122,0.40) | #C2BAB1 |
| border-subtle | rgba(255,235,214,0.50) | #FFF1E2 |

### Dark Mode

| Token | Old | New | Source |
|-------|-----|-----|--------|
| canvas | #0a0a0b | #1F1F1F | Carbon Black |
| surface (elevation-1) | #111113 | #2A2A2A | Derived (+1 step) |
| surface-elevated (elevation-2) | #1A1A1C | #353535 | Derived (+2 steps) |
| elevation-3 | #252527 | #404040 | Derived (+3 steps) |
| elevation-4 | #2D2D30 | #4A4A4A | Derived (+4 steps) |
| text | rgba(250,250,248,0.87) | rgba(255,251,247,0.87) | Porcelain at 87% |
| text-secondary | rgba(250,250,248,0.60) | rgba(255,251,247,0.60) | Porcelain at 60% |
| text-muted | rgba(250,250,248,0.38) | rgba(255,251,247,0.38) | Porcelain at 38% |
| border | #1f1f23 | #353535 | Elevation-2 |
| border-emphasis | #3A3A3E | #4A4A4A | Elevation-4 |
| border-subtle | #1f1f23 | #2A2A2A | Elevation-1 |
| accent | #fbbf24 | #D4BF9B | Pale Oak (configurable) |
| accent-hover | #f59e0b | #B9975C | Camel (configurable) |
| accent-surface | rgba(251,191,36,0.15) | rgba(185,151,92,0.15) | Camel at 15% |
| accent-foreground | (implicit) | #1F1F1F | Carbon Black (auto-derived) |
| success | #22c55e | #286736 | Dark Emerald |
| success-foreground | #4ade80 | #39934D | Sea Green |
| success-surface | rgba(34,197,94,0.15) | rgba(57,147,77,0.15) | Sea Green at 15% |
| warning | (none) | #D4AD4A | Harvest Gold |
| warning-foreground | (none) | #D4AD4A | Harvest Gold |
| warning-surface | (none) | rgba(168,134,43,0.15) | Raw Sienna at 15% |
| error | #ef4444 | #AE1C09 | Oxidized Iron |
| error-foreground | #f87171 | #F5533D | Tomato |
| error-surface | rgba(239,68,68,0.15) | rgba(245,83,61,0.15) | Tomato at 15% |
| info | #3b82f6 | #49696E | Blue Slate |
| info-foreground | #60a5fa | #91B1B6 | Cool Steel |
| info-surface | rgba(59,130,246,0.15) | rgba(145,177,182,0.15) | Cool Steel at 15% |

Hover/active overlays stay as-is. Verify visually on #1F1F1F canvas.

---

## 3. Functional Color Summary

Six families. Five active, one reserved.

| Function | Main | Light | Dark | Status |
|----------|------|-------|------|--------|
| Error | #AE1C09 Oxidized Iron | #F5533D Tomato | #741306 Molten Lava | Locked |
| Warning | #A8862B Raw Sienna | #D4AD4A Harvest Gold | #6B5518 Bronze | Locked |
| Success | #286736 Dark Emerald | #39934D Sea Green | #173B1F Deep Forest | Locked |
| Info | #49696E Blue Slate | #91B1B6 Cool Steel | #314649 Dark Slate Gray | Locked |
| Accent | #B9975C Camel | #D4BF9B Pale Oak | #725A31 Olive Bark | Configurable |
| Orange | #9E5A2A Burnt Copper | #C4835A Clay | #6A3B19 Umber | Reserved |

Warning (Raw Sienna) is visually distinct from Gold accent -- ochre vs warm gold.

---

## 4. Accent Parameterization

The accent is the ONLY color that changes between apps. Everything else is locked.

Set accent hex in `crisp.config.json`. Run `scripts/generate-accent.js`. The script derives hover, surface, foreground, and dark mode variants automatically.

### crisp.config.json schema

```json
{
  "accent": "#B9975C",
  "accentName": "Camel"
}
```

### What the script generates from one hex

| Token | Rule |
|-------|------|
| accent | Input hex |
| accent-hover | 15% darker (OKLCH lightness) |
| accent-surface | 10% opacity on #fff8f2 |
| accent-surface-dark | 15% opacity on #1F1F1F |
| accent-foreground | #1F1F1F if light accent, Porcelain 87% if dark |
| Dark mode accent | 15% lighter (OKLCH lightness) |
| Dark mode accent-hover | Original input hex |
| Focus ring | `outline: 2px solid [accent]` |

### What stays locked (never changes per app)

All gray/black, all white, all functional colors, typography, spacing, radius, shadows, transitions, z-index, layout dimensions, and all component structure.

---

## 5. Contrast Verification

All text/background combos need WCAG AA (4.5:1 normal, 3:1 large/UI).

### Light mode (on #fff8f2)

| Combination | Ratio | Pass? |
|-------------|-------|-------|
| #1F1F1F on #fff8f2 | ~14.5:1 | Yes |
| #454545 on #fff8f2 | ~7.2:1 | Yes |
| #7A7A7A on #fff8f2 | ~4.0:1 | Borderline -- captions only |
| #725A31 on #fff8f2 | ~5.3:1 | Yes |
| #B9975C on #fff8f2 | ~3.8:1 | Large text only |
| #AE1C09 on #fff8f2 | ~5.0:1 | Yes |
| #286736 on #fff8f2 | ~5.8:1 | Yes |
| #A8862B on #fff8f2 | ~5.0:1 | Yes |
| #49696E on #fff8f2 | ~4.5:1 | Borderline -- verify exactly |

### Dark mode (on #1F1F1F)

| Combination | Ratio | Pass? |
|-------------|-------|-------|
| Porcelain 87% on #1F1F1F | ~12.0:1 | Yes |
| Porcelain 60% on #1F1F1F | ~7.5:1 | Yes |
| Porcelain 38% on #1F1F1F | ~4.2:1 | Borderline -- captions only |
| #D4BF9B on #1F1F1F | ~8.5:1 | Yes |
| #39934D on #1F1F1F | ~4.5:1 | Borderline -- verify |
| #D4AD4A on #1F1F1F | ~7.5:1 | Yes |
| #F5533D on #1F1F1F | ~4.8:1 | Yes |
| #91B1B6 on #1F1F1F | ~6.5:1 | Yes |

Borderline items need exact calculation before finalizing. Accent contrast note: the generate script must verify 3:1 against canvas for UI components.

---

## 6. Crisp Green Removal

Remove `references/colors.md` lines 72-86 ("Crisp Green" alternative accent). Green is a locked functional color (success) and cannot double as accent. Replace with:

```
The accent color is configurable per app. See crisp.config.json.
Default: Gold (#B9975C).
```

---

## 7. Brand Identity

### Name

- Running text and UI: lowercase `crisp`
- Sentence start or doc title: `Crisp`
- Never `CRISP`
- App naming: `[appname]` lowercase, no "Crisp" prefix unless first-party

### Voice

Direct. No superlatives. No marketing hedging. Technical when describing features, plain when addressing users. Sentence case headings. Lowercase labels.

```
GOOD: "Upload a CSV to import contacts."
BAD:  "Seamlessly import your contacts with our powerful CSV upload tool."

GOOD: "Search finds results across all fields."
BAD:  "Our intelligent search empowers you to find anything instantly."
```

### Logo

No logo spec this version. If a mark is needed: single lowercase letter in CrispByYosi Bold, #1F1F1F on light / #FFFBF7 on dark.

### Favicon

- Solid rounded square, #1F1F1F background, #FFFBF7 letter, CrispByYosi Bold, centered
- Corner radius: 4px at 32x32 (scales proportionally)
- Sizes: 16x16, 32x32, 48x48, 180x180 (apple-touch-icon), SVG
- Letter: first letter of app name, lowercase. Fallback: period (`.`)

### OG Image

- 1200x630px, #fff8f2 background
- App name: CrispByYosi Bold, 72px, #1F1F1F, centered, 40% from top
- Optional subtext: CrispByYosi Regular, 28px, #454545, 16px below
- No imagery, no icons, no accent color

---

## Approved Palette (Quick Reference)

```
LOCKED (identical across all apps)

  Background     #fff8f2    Background White
  Surface        #FFFBF7    Porcelain
  Warm Tint      #FFEBD6    Antique White

  Text Primary   #1F1F1F    Carbon Black
  Text Secondary #454545    Gunmetal
  Text Muted     #7A7A7A    Grey

  Error          #AE1C09 / #F5533D / #741306
  Warning        #A8862B / #D4AD4A / #6B5518
  Success        #286736 / #39934D / #173B1F
  Info           #49696E / #91B1B6 / #314649

ACCENT (only color that changes per app)

  Default Gold   #B9975C / #D4BF9B / #725A31

DARK MODE CANVAS

  Canvas         #1F1F1F    Elev 1: #2A2A2A
  Elev 2         #353535    Elev 3: #404040    Elev 4: #4A4A4A

BORDERS (resolved from rgba on #fff8f2)

  Border         #EDE3D4    Emphasis: #C2BAB1    Subtle: #FFF1E2
```
