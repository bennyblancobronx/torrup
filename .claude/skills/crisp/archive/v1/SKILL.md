---
name: crisp
version: 1.0.0
description: Crisp Design Language - Functional Minimalism based on Dieter Rams' principles. Complete design system with exact specifications for typography, color, spacing, components, and layout. Ensures 100% visual consistency across all implementations.
---

# Crisp Design Language v1.0.0

**"Weniger, aber besser"** — Less, but better.

## Quick Reference Card

```
FONT: CrispByYosi ONLY
  700 Bold    -> Titles
  500 Medium  -> Buttons, Labels, Headings
  400 Regular -> Body
  300 Light   -> Captions, Meta, Code

COLORS
  Light Canvas: #FAFAF8    Dark Canvas: #0a0a0b
  Light Text:   #1C1C1A    Dark Text:   rgba(250,250,248,.87)
  Border:       #E2E1DE    Dark Border: #1f1f23
  Accent:       #f59e0b    (amber - use sparingly)
  Success: #22c55e  Warning: #eab308  Error: #ef4444

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

1. **Content speaks** — Photography, data, and text are heroes; UI recedes
2. **Function over form** — Every element must serve a purpose
3. **Honest materials** — Show real data, no fake placeholders
4. **Systematic consistency** — Grid-based, token-driven
5. **Timeless over trendy** — Design for 5+ year relevance

---

## Dieter Rams' 10 Principles of Good Design

Every design decision should be measured against these principles:

1. **Good design is innovative** — Technology enables new solutions, but innovation must serve the product.

2. **Good design makes a product useful** — Primary focus is function. Design clarifies utility.

3. **Good design is aesthetic** — Well-executed products are pleasant to use. Aesthetic quality is integral to usefulness.

4. **Good design makes a product understandable** — The product explains itself. No manual needed.

5. **Good design is unobtrusive** — Products are tools, not decorative objects. Neutral and restrained.

6. **Good design is honest** — Does not manipulate or promise more than it delivers.

7. **Good design is long-lasting** — Avoids trends. Neither fashionable nor old-fashioned.

8. **Good design is thorough down to the last detail** — Nothing arbitrary. Accuracy shows respect for users.

9. **Good design is environmentally friendly** — Conserves resources. Minimal visual and physical pollution.

10. **Good design is as little design as possible** — "Weniger, aber besser" — Less, but better. Pure essence.

---

## Historical Context

### The Ulm School (HfG Ulm)

The Hochschule fur Gestaltung Ulm (1953-1968) established systematic design methodology:

- Mathematical approach to design problems
- Grid systems and modular construction
- Rejection of decoration and ornament
- Integration of science and design
- Emphasis on research and analysis

Crisp's design language emerged from this tradition, with Dieter Rams joining in 1955 and leading design from 1961-1995.

### Key Characteristics

- **Geometric precision** — All forms derived from mathematical relationships
- **Material honesty** — Materials appear as they are
- **Functional clarity** — Purpose is immediately apparent
- **Visual quietness** — The product recedes, content emerges

---

## CrispByYosi Typeface

### Overview

CrispByYosi is the exclusive typeface for all Crisp Design Language implementations. Created by Iconwerk for Crisp Global.

### Distinctive Characteristics

1. **Racetrack terminals** — Character endings feature the signature "racetrack" shape (stadium curve), visible in letters like C, G, S, e, c, s

2. **Narrow capitals** — Uppercase letters are proportionally narrower than typical sans-serifs

3. **Circular dots** — Periods, dots on i/j, and diacritics are perfect circles

4. **Technical precision** — Geometric construction with optical corrections

5. **Lowercase emphasis** — The typeface is optimized for lowercase text, reflecting Crisp's preference for lowercase in product labeling

### Weight Usage

| Weight | Value | Character | Use |
|--------|-------|-----------|-----|
| Thin | 100 | Elegant, delicate | Display numerics, decorative (rare) |
| Light | 300 | Refined, subtle | Captions, metadata, code, hashes |
| Regular | 400 | Balanced, neutral | Body text, input values |
| Medium | 500 | Confident, clear | Buttons, navigation, labels, headings |
| Bold | 700 | Strong, authoritative | Titles, hero text |

**Critical:** Weight 600 (semibold) does not exist. Always use 500 or 700.

### Brand Text Styling

For brand names and feature labels, consider lowercase emphasis:

```
crisp (not CRISP)
good design is as little design as possible
```

This reflects the original Crisp product labeling philosophy.

---

## Accent Color Options

### Primary: Amber (#f59e0b)

The default accent color. Use sparingly for:
- Focus states
- Single emphasized CTA
- New/highlighted badges

### Alternative: Crisp Green (#4ade80)

Historic reference to Crisp's iconic green power switches. May be used as an alternative accent when:
- The context specifically references "on/active" states
- Amber conflicts with warning states
- Brand alignment with historic Crisp products is desired

```css
--color-accent-green: #4ade80;
--color-accent-green-hover: #22c55e;
```

**Note:** Only ONE accent color per interface. Never mix amber and green accents.

---

## Decision Trees

### Which Button?

```
Is it the primary action on the page?
  YES -> btn-primary (black/white)
  NO  -> Is it a secondary/cancel action?
         YES -> btn-secondary (outline)
         NO  -> Is it destructive?
                YES -> btn-secondary + error text color
                NO  -> Is it the ONLY CTA needing emphasis?
                       YES -> btn-accent (amber)
                       NO  -> btn-ghost (text only)
```

### Which Spacing?

```
Between icon and label?         -> 8px
Between form fields?            -> 16px
Between card content sections?  -> 16px
Between cards in a grid?        -> 24px
Between page sections?          -> 48px
Between major areas?            -> 64px
```

### Which Font Weight?

```
Page title?           -> 700 Bold
Section heading?      -> 500 Medium
Body text?            -> 400 Regular
Caption/meta?         -> 300 Light
Uppercase label?      -> 500 Medium
Code/hash/ID?         -> 300 Light
```

### Which Border?

```
Card outline?           -> 1px solid var(--color-border)
Input default?          -> 1px solid var(--color-border-emphasis)
Divider line?           -> 1px solid var(--color-border)
Active/selected state?  -> 1px solid var(--color-text)
```

---

## Typography

**Font: CrispByYosi (EXCLUSIVE)**

Single font family for ALL text. No exceptions.

```css
font-family: 'CrispByYosi', system-ui, sans-serif;
```

### Type Scale

| Token | Size | Weight | Line Height | Letter Spacing | Use |
|-------|------|--------|-------------|----------------|-----|
| text-xs | 11px | 500 | 1.3 | 0.1em | Labels (UPPERCASE) |
| text-sm | 13px | 300 | 1.5 | 0 | Captions, metadata, code |
| text-base | 15px | 400 | 1.6 | 0 | Body text |
| text-lg | 17px | 500 | 1.5 | 0 | Subsection heads |
| text-xl | 20px | 500 | 1.4 | -0.01em | Section heads |
| text-2xl | 24px | 700 | 1.3 | -0.01em | Page titles |
| text-3xl | 30px | 700 | 1.2 | -0.02em | Hero titles |
| text-4xl | 36px | 700 | 1.2 | -0.02em | Display (rare) |

### Font Weights

| Weight | Value | Use |
|--------|-------|-----|
| Thin | 100 | Display, decorative (rare) |
| Light | 300 | Captions, meta, code, hashes |
| Regular | 400 | Body text, inputs |
| Medium | 500 | Buttons, nav, labels, headings |
| Bold | 700 | Page titles, hero text |

**Note:** CrispByYosi has no 600 weight. Use 500 or 700.

---

## Color System

### Light Mode

| Token | Hex | Use |
|-------|-----|-----|
| canvas | #FAFAF8 | App background |
| surface | #F4F4F2 | Cards, panels |
| surface-elevated | #FFFFFF | Modals, dropdowns |
| text | #1C1C1A | Primary text |
| text-secondary | #5C5C58 | Descriptions |
| text-muted | #8A8A86 | Captions, meta |
| border | #E2E1DE | Default borders |
| border-emphasis | #C0BFBC | Input borders, emphasis |

### Dark Mode

| Token | Value | Use |
|-------|-------|-----|
| canvas | #0a0a0b | App background |
| surface | #111113 | Cards, panels |
| surface-elevated | #1A1A1C | Modals, dropdowns |
| text | rgba(250,250,248,0.87) | Primary text |
| text-secondary | rgba(250,250,248,0.60) | Descriptions |
| text-muted | rgba(250,250,248,0.38) | Captions, meta |
| border | #1f1f23 | Default borders |
| border-emphasis | #3A3A3E | Input borders |

### Functional Colors (Both Modes)

| Function | Hex | Use |
|----------|-----|-----|
| success | #22c55e | Verified, complete, positive |
| warning | #eab308 | Caution, attention needed |
| error | #ef4444 | Error, destructive, failed |
| info | #3b82f6 | Informational |

### Accent (Amber - Use Sparingly)

| Token | Light | Dark |
|-------|-------|------|
| accent | #f59e0b | #fbbf24 |
| accent-hover | #d97706 | #f59e0b |
| accent-surface | #fef3c7 | rgba(251,191,36,0.15) |

---

## Spacing System (8pt Grid)

```css
--space-1: 4px;    /* Fine adjustment only */
--space-2: 8px;    /* Tight grouping */
--space-3: 12px;   /* Related elements */
--space-4: 16px;   /* Component padding - DEFAULT */
--space-5: 20px;   /* -- */
--space-6: 24px;   /* Section spacing */
--space-8: 32px;   /* Group separation */
--space-10: 40px;  /* -- */
--space-12: 48px;  /* Major sections */
--space-16: 64px;  /* Page sections */
--space-20: 80px;  /* -- */
--space-24: 96px;  /* Hero spacing */
```

### When to Use

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
| radius-sm | 4px | Badges, chips, tags |
| radius-md | 6px | Buttons, inputs |
| radius-lg | 8px | Cards, panels, modals |
| radius-full | 50% | Avatars, circular icons |

**Rule:** Never exceed 8px except for full circles.

---

## Component Specifications

### Buttons

| Size | Height | Padding | Font Size |
|------|--------|---------|-----------|
| Small | 32px | 6px 12px | 13px |
| Medium | 44px | 10px 20px | 15px |
| Large | 52px | 14px 28px | 17px |

### Button States

| State | Primary BG | Primary Text |
|-------|------------|--------------|
| default | #1C1C1A | #FFFFFF |
| hover | #333330 | #FFFFFF |
| active | #1C1C1A | #FFFFFF |
| focus | #1C1C1A + 2px amber outline | #FFFFFF |
| disabled | #E2E1DE | #8A8A86 |

### Input States

| State | Background | Border | Text |
|-------|------------|--------|------|
| default | #FFFFFF | 1px #C0BFBC | #1C1C1A |
| hover | #FFFFFF | 1px #8A8A86 | #1C1C1A |
| focus | #FFFFFF | 1px #f59e0b | #1C1C1A |
| error | #FFFFFF | 1px #ef4444 | #1C1C1A |
| disabled | #F4F4F2 | 1px #E2E1DE | #8A8A86 |

### Cards

| State | Background | Border |
|-------|------------|--------|
| default | #FFFFFF | 1px #E2E1DE |
| hover | #FFFFFF | 1px #C0BFBC |
| selected | #FFFFFF | 1px #1C1C1A |

---

## Layout Templates

### Dashboard

```
Header: height 64px, padding 0 24px, border-bottom
Sidebar: width 240px, padding 24px 16px, border-right
Main: padding 32px
Card Grid: gap 24px, columns auto-fill minmax(280px, 1fr)
```

### Settings/Forms

```
Nav: width 200px
Form: max-width 640px, padding 32px
Section gap: 48px
Field gap: 16px
```

### Modal

```
Small: width 480px
Medium: width 640px
Large: width 800px
Padding: 24px
Border-radius: 8px
Backdrop: rgba(0,0,0,0.5) light / rgba(0,0,0,0.7) dark
```

### Data Table

```
Header height: 48px
Row height: 52px
Cell padding: 12px 16px
Header font: 11px / 500 / uppercase / 0.1em letter-spacing
Cell font: 15px / 400
```

---

## Z-Index Scale

| Token | Value | Use |
|-------|-------|-----|
| z-base | 0 | Default |
| z-dropdown | 100 | Dropdowns |
| z-sticky | 200 | Sticky headers |
| z-modal-backdrop | 300 | Modal overlay |
| z-modal | 400 | Modal content |
| z-popover | 500 | Popovers |
| z-tooltip | 600 | Tooltips |
| z-toast | 700 | Toast notifications |

---

## Opacity Scale

| Value | Use |
|-------|-----|
| 0.03 | Hover background (light) |
| 0.05 | Hover background (dark), selected (light) |
| 0.08 | Selected background (dark) |
| 0.38 | Muted text, disabled elements |
| 0.50 | Modal backdrop (light) |
| 0.60 | Secondary text (dark) |
| 0.70 | Modal backdrop (dark) |
| 0.87 | Primary text (dark) |

---

## Icons

### Sizes

| Size | Dimensions | Stroke Width |
|------|------------|--------------|
| sm | 16x16 | 1.5px |
| md | 20x20 | 2px |
| lg | 24x24 | 2px |
| xl | 32x32 | 2.5px |

### Rules

- Stroke only, no fills
- Use `currentColor` for stroke
- No decorative icons
- Icons must communicate function

---

## Loading States

| Duration | Treatment |
|----------|-----------|
| < 300ms | No indicator |
| 300ms - 2s | Text "Loading..." |
| > 2s | Static progress bar |

**Never:** Animated skeletons, shimmer effects, pulse animations.

---

## Accessibility

### Contrast Requirements

| Element | Minimum Ratio |
|---------|---------------|
| Normal text | 4.5:1 |
| Large text (24px+) | 3:1 |
| UI components | 3:1 |
| Focus indicators | 3:1 |

### Touch Targets

- Minimum: 44x44px
- Recommended: 48x48px

### Focus States

```css
:focus-visible {
  outline: 2px solid #f59e0b;
  outline-offset: 2px;
}
```

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
- [ ] Focus states visible (2px amber outline)
- [ ] Dark mode tested

---

## Anti-Patterns (REJECT)

- Colored accent buttons (except amber)
- Gradient overlays on imagery
- Decorative shadows or glows
- Border-radius > 8px
- Animated loading skeletons
- Text shadows
- Color for decoration (not function)
- Ornamental icons
- Multiple font families
- Non-grid spacing
- Pure black (#000) or white (#FFF)

---

## Naming Conventions

### Components

```
btn-{variant}     -> btn-primary, btn-secondary, btn-ghost, btn-accent
input-{variant}   -> input-default, input-error
card-{size}       -> card-sm, card-md, card-lg
badge-{status}    -> badge-success, badge-warning, badge-error
```

### Layout

```
layout-{type}     -> layout-dashboard, layout-settings
sidebar-{element} -> sidebar-nav, sidebar-brand
```

### Utilities

```
text-{role}       -> text-primary, text-secondary, text-muted
bg-{surface}      -> bg-canvas, bg-surface, bg-elevated
```

### States

```
is-{state}        -> is-active, is-disabled, is-loading
has-{feature}     -> has-error, has-icon
```

---

## Additional References

- `references/component-specs.md` — Complete CSS for all components
- `references/dark-mode.md` — Dark mode implementation guide
- `references/anti-patterns.md` — Detailed violations with examples
- `references/decision-trees.md` — Complete decision flowcharts
- `references/layouts.md` — Page layout templates with breakpoints
- `references/states.md` — All interactive states specification
- `assets/css/design-system.css` — Production-ready CSS
- `assets/css/fonts.css` — @font-face declarations
- `assets/config/tailwind.preset.js` — Tailwind configuration
- `assets/config/design-tokens.json` — Design tokens export
- `assets/config/stylelint.config.js` — Automated lint rules
- `assets/fonts/` — CrispByYosi font files (woff2)

---

## Sources

- Dieter Rams' 10 Principles of Good Design
- Ulm School of Design methodology
- CrispByYosi typeface by Iconwerk
- Material Design dark theme guidelines
- WCAG 2.1 accessibility standards
