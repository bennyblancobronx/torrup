---
name: crisp
description: >
  Crisp Design Language - Functional minimalism based on Dieter Rams' principles.
  Complete design system for typography, color, spacing, components, and layout.
metadata:
  version: 0.1.4
---

# Crisp Design Language

**"Weniger, aber besser"** -- Less, but better.

## Quick Reference Card

```
FONT: CrispByYosi ONLY
  700 Bold    -> Titles
  500 Medium  -> Buttons, Labels, Headings
  400 Regular -> Body
  300 Light   -> Captions, Meta, Code

COLORS (locked across all apps)
  Light Canvas: #fff8f2    Dark Canvas: #1F1F1F
  Light Text:   #1F1F1F    Dark Text:   rgba(255,251,247,.87)
  Border:       #EDE3D4    Dark Border: #353535
  Success: #286736  Warning: #A8862B  Error: #AE1C09  Info: #49696E

ACCENT (configurable per app, default Gold)
  Light: #B9975C   Dark: #D4BF9B   Hover: #725A31

SPACING (8pt grid)
  8   -> tight       24  -> sections
  16  -> default     48  -> major sections

RADIUS
  4px -> badges      6px -> buttons/inputs    8px -> cards

NEVER
  x Pure black/white    x Radius > 8px       x Colored buttons
  x Gradients           x Shadows (dark)     x Animated loaders
  x Multiple fonts      x Decorative icons
```

---

## Core Philosophy

1. **Content speaks** -- Photography, data, and text are heroes; UI recedes
2. **Function over form** -- Every element must serve a purpose
3. **Honest materials** -- Show real data, no fake placeholders
4. **Systematic consistency** -- Grid-based, token-driven
5. **Timeless over trendy** -- Design for 5+ year relevance

---

## Dieter Rams' 10 Principles

1. **Innovative** -- Technology enables new solutions, but innovation must serve the product
2. **Useful** -- Primary focus is function. Design clarifies utility
3. **Aesthetic** -- Well-executed products are pleasant to use
4. **Understandable** -- The product explains itself. No manual needed
5. **Unobtrusive** -- Products are tools, not decorative objects
6. **Honest** -- Does not manipulate or promise more than it delivers
7. **Long-lasting** -- Avoids trends. Neither fashionable nor old-fashioned
8. **Thorough** -- Nothing arbitrary. Accuracy shows respect for users
9. **Environmentally friendly** -- Conserves resources. Minimal pollution
10. **As little design as possible** -- Pure essence

---

## Type Scale

| Token | Size | Weight | Line Height | Letter Spacing | Use |
|-------|------|--------|-------------|----------------|-----|
| text-xs | 11px | 500 | 1.3 | 0.1em | Labels (UPPERCASE) |
| text-sm | 13px | 300 | 1.5 | 0 | Captions, metadata, code |
| text-base | 15px | 400 | 1.6 | 0 | Body text |
| text-lg | 17px | 500 | 1.5 | 0 | Subsection heads |
| text-xl | 20px | 500 | 1.4 | -0.01em | Section heads |
| text-2xl | 24px | 700 | 1.3 | -0.01em | Page titles |
| text-3xl | 30px | 700 | 1.2 | -0.02em | Hero titles |

Weight 600 does not exist. Use 500 or 700.

---

## Color Tokens (Light)

| Token | Hex | Use |
|-------|-----|-----|
| canvas | #fff8f2 | App background |
| surface | #FFFBF7 | Cards, panels |
| surface-elevated | #FFFBF7 | Modals, dropdowns |
| text | #1F1F1F | Primary text |
| text-secondary | #454545 | Descriptions |
| text-muted | #7A7A7A | Captions, meta |
| border | #EDE3D4 | Default borders |
| border-emphasis | #C2BAB1 | Input borders |

## Color Tokens (Dark)

| Token | Value | Use |
|-------|-------|-----|
| canvas | #1F1F1F | App background |
| surface | #2A2A2A | Cards, panels |
| surface-elevated | #353535 | Modals, dropdowns |
| text | rgba(255,251,247,0.87) | Primary text |
| text-secondary | rgba(255,251,247,0.60) | Descriptions |
| text-muted | rgba(255,251,247,0.38) | Captions, meta |
| border | #353535 | Default borders |
| border-emphasis | #4A4A4A | Input borders |

## Functional Colors

| Function | Hex |
|----------|-----|
| success | #286736 |
| warning | #A8862B |
| error | #AE1C09 |
| info | #49696E |

## Accent (configurable, default Gold)

| Token | Light | Dark |
|-------|-------|------|
| accent | #B9975C | #D4BF9B |
| accent-hover | #725A31 | #B9975C |
| accent-surface | #FFEBD6 | rgba(185,151,92,0.15) |

---

## Spacing (8pt Grid)

| Context | Value |
|---------|-------|
| Icon margin | 4px |
| Button icon gap | 8px |
| Input padding | 10-12px |
| Card padding | 16px |
| Section gap | 24px |
| Card grid gap | 24px |
| Page sections | 48-64px |

---

## Border Radius

| Token | Value | Use |
|-------|-------|-----|
| radius-sm | 4px | Badges, chips |
| radius-md | 6px | Buttons, inputs |
| radius-lg | 8px | Cards, panels, modals |
| radius-full | 50% | Avatars, circles |

Never exceed 8px except for full circles and toggle pill shapes.

---

## Quick Decisions

**Button:** Primary action -> btn-primary (gunmetal/porcelain). Secondary -> btn-secondary (outline). Destructive -> btn-destructive (error outline). Only CTA -> btn-accent (configurable, default Gold). Subtle -> btn-ghost.

**Spacing:** Icon-to-label 8px. Form fields 16px. Cards in grid 24px. Page sections 48px.

**Weight:** Title 700. Heading/button/nav 500. Body 400. Caption/meta/code 300.

**Border:** Card 1px border. Input 1px border-emphasis. Active 1px text. Divider 1px border.

---

## Verification Checklist

Before committing any UI:

- [ ] Font is CrispByYosi (check ALL text)
- [ ] All spacing values on 8pt grid
- [ ] No border-radius > 8px (except 50% circles)
- [ ] No pure black (#000) or pure white (#FFF)
- [ ] No decorative colors (color = function only)
- [ ] No decorative shadows
- [ ] No animated skeletons or loaders
- [ ] All interactive states defined
- [ ] Touch targets >= 44px
- [ ] Contrast ratio >= 4.5:1
- [ ] Focus states visible (2px accent outline)
- [ ] Dark mode tested

---

## Anti-Patterns (REJECT)

- Colored accent buttons (except configurable accent)
- Gradient overlays on imagery
- Decorative shadows or glows
- Border-radius > 8px
- Animated loading skeletons
- Text shadows or gradient text
- Color for decoration (not function)
- Ornamental icons or filled icons
- Multiple font families
- Non-grid spacing
- Pure black (#000) or white (#FFF)
- Transitions longer than 350ms

---

## Reference Files

| File | Content |
|------|---------|
| `references/philosophy.md` | Rams' principles expanded, Ulm School, brand text |
| `references/typography.md` | CrispByYosi characteristics, weight/size tables |
| `references/colors.md` | Full color tokens, light/dark, functional, accent |
| `references/spacing-and-tokens.md` | 8pt grid, z-index, opacity, icon sizes |
| `references/buttons.md` | All button variants, sizes, states, CSS |
| `references/forms.md` | Inputs, selects, checkboxes, radios, toggles |
| `references/cards.md` | Card variants, sizes, image cards, CSS |
| `references/navigation.md` | Sidebar, header, tabs, dropdown menus |
| `references/overlays.md` | Modals, tooltips, toasts, empty states, loading |
| `references/data-display.md` | Tables, badges, status indicators, avatars, dividers |
| `references/layouts.md` | Dashboard, settings, modal, detail, empty layouts |
| `references/responsive.md` | Breakpoints, density, sidebar/card/table reflow |
| `references/dark-mode.md` | Theme detection, toggle, elevation, shadows |
| `references/states.md` | All interactive states for all components |
| `references/accessibility.md` | Contrast, touch targets, focus, ARIA |
| `references/anti-patterns.md` | Violations with WRONG/CORRECT examples |
| `references/decisions.md` | Decision tree flowcharts for every choice |
| `references/naming.md` | Component, layout, utility, state naming |
| `references/brand.md` | Brand identity, naming, voice, favicon, OG image |

## Assets

- `assets/css/design-system.css` -- Production-ready CSS
- `assets/css/fonts.css` -- @font-face declarations
- `assets/config/tailwind.preset.js` -- Tailwind configuration
- `assets/config/design-tokens.json` -- Design tokens export
- `assets/config/stylelint.config.js` -- Automated lint rules
- `assets/fonts/` -- CrispByYosi font files (woff2)
- `crisp.config.json` -- Per-app accent configuration
- `scripts/generate-accent.js` -- Accent variant generator
- `scripts/init.sh` -- Project bootstrap
- `scripts/migrate.sh` -- Old hex migration helper
