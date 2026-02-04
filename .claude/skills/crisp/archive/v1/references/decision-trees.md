# Decision Trees

Complete flowcharts for every design decision. Follow these exactly - no interpretation needed.

---

## Button Selection

```
START: What action is this button for?
  |
  +-- Is it the PRIMARY action on the page?
  |     YES --> btn-primary (black in light, white in dark)
  |     NO  --> continue
  |
  +-- Is it a SECONDARY or CANCEL action?
  |     YES --> btn-secondary (outlined)
  |     NO  --> continue
  |
  +-- Is it a DESTRUCTIVE action (delete, remove)?
  |     YES --> btn-secondary with error text color (#ef4444)
  |     NO  --> continue
  |
  +-- Is it the ONLY call-to-action needing emphasis?
  |     YES --> btn-accent (amber #f59e0b)
  |     NO  --> continue
  |
  +-- Is it an inline/subtle action (e.g., "Learn more")?
        YES --> btn-ghost (text only, no background)
```

### Button Size Selection

```
Where is the button used?
  |
  +-- In a toolbar or tight space?
  |     --> Small (height: 32px)
  |
  +-- Standard form or dialog?
  |     --> Medium (height: 44px) [DEFAULT]
  |
  +-- Hero section or standalone CTA?
        --> Large (height: 52px)
```

---

## Typography Selection

### Font Weight

```
What is this text element?
  |
  +-- Page title or hero text?
  |     --> 700 (Bold)
  |
  +-- Section heading, button label, navigation item?
  |     --> 500 (Medium)
  |
  +-- Body text, paragraph, input value?
  |     --> 400 (Regular)
  |
  +-- Caption, metadata, timestamp, code, hash/ID?
  |     --> 300 (Light)
  |
  +-- Decorative display (rare, e.g., massive numbers)?
        --> 100 (Thin)

NEVER USE 600 - it does not exist in CrispByYosi
```

### Font Size

```
What is this text's role?
  |
  +-- Uppercase label (STATUS, TYPE, CATEGORY)?
  |     --> 11px, weight 500, letter-spacing 0.1em
  |
  +-- Caption, metadata, timestamp, code?
  |     --> 13px, weight 300
  |
  +-- Body text, input text?
  |     --> 15px, weight 400 [DEFAULT]
  |
  +-- Subsection heading?
  |     --> 17px, weight 500
  |
  +-- Section heading?
  |     --> 20px, weight 500
  |
  +-- Page title?
  |     --> 24px, weight 700
  |
  +-- Hero title?
  |     --> 30px, weight 700
  |
  +-- Display (very rare)?
        --> 36px, weight 700
```

---

## Spacing Selection

### Component Internal Spacing

```
What are you spacing?
  |
  +-- Icon to adjacent label?
  |     --> 8px
  |
  +-- Button internal padding (vertical)?
  |     --> sm: 6px, md: 10px, lg: 14px
  |
  +-- Button internal padding (horizontal)?
  |     --> sm: 12px, md: 20px, lg: 28px
  |
  +-- Input padding?
  |     --> 10px 12px
  |
  +-- Card padding?
  |     --> 16px (standard) or 24px (spacious)
  |
  +-- Modal padding?
        --> 24px
```

### Layout Spacing

```
What are you spacing?
  |
  +-- Between form fields?
  |     --> 16px
  |
  +-- Between cards in a grid?
  |     --> 24px
  |
  +-- Between content sections within a card?
  |     --> 16px
  |
  +-- Between page sections?
  |     --> 48px (standard) or 64px (major)
  |
  +-- Page edge padding?
        --> 24px (mobile) or 32px (desktop)
```

---

## Color Selection

### When to Use Accent (Amber)

```
Should I use the amber accent color?
  |
  +-- Is it a focused input border?
  |     YES --> Use accent
  |
  +-- Is it a focus ring (outline)?
  |     YES --> Use accent, 2px solid
  |
  +-- Is it the ONLY CTA button needing emphasis?
  |     YES --> Use btn-accent
  |     NO  --> Do NOT use accent for buttons
  |
  +-- Is it showing a "new" or "highlighted" state?
  |     YES --> Consider accent badge sparingly
  |
  +-- Is it decorative?
        YES --> DO NOT USE. Color = function only.
```

### When to Use Functional Colors

```
What state or meaning does this communicate?
  |
  +-- Success, verified, complete, positive?
  |     --> #22c55e (success)
  |
  +-- Warning, attention needed, caution?
  |     --> #eab308 (warning)
  |
  +-- Error, failed, destructive?
  |     --> #ef4444 (error)
  |
  +-- Informational, neutral highlight?
  |     --> #3b82f6 (info)
  |
  +-- None of the above?
        --> Use text colors only (primary/secondary/muted)
```

### Functional Color Application

```
Where to apply functional colors?
  |
  +-- Status badges?
  |     --> Colored background (subtle) + colored text
  |     Light: success-surface #dcfce7, text #166534
  |     Dark:  success-surface rgba(34,197,94,0.15), text #4ade80
  |
  +-- Status indicators (dots)?
  |     --> Solid fill with functional color
  |
  +-- Error messages?
  |     --> Text color only (#ef4444)
  |
  +-- Form validation?
  |     --> Border color only (1px solid #ef4444)
  |
  +-- Numbers, values, metrics?
        --> DO NOT color. Use text colors only.
        --> Exception: Colored label/badge NEXT to value
```

---

## Border Radius Selection

```
What element is this?
  |
  +-- Badge, chip, tag?
  |     --> 4px
  |
  +-- Button, input, select, textarea?
  |     --> 6px
  |
  +-- Card, panel, modal, dropdown?
  |     --> 8px [MAXIMUM]
  |
  +-- Avatar, circular icon, indicator dot?
  |     --> 50% (full circle)
  |
  +-- Toggle switch track?
        --> 9999px (pill shape - ONLY exception to 8px max)
```

---

## Shadow Selection

### Light Mode

```
Does this element need a shadow?
  |
  +-- Is it an elevated surface (modal, dropdown, popover)?
  |     YES --> shadow-md: 0 2px 4px rgba(0,0,0,0.06)
  |
  +-- Is it a card that needs subtle depth?
  |     YES --> shadow-sm: 0 1px 2px rgba(0,0,0,0.04)
  |     Prefer borders over shadows
  |
  +-- Is it for decorative effect?
        YES --> NO SHADOW. Use border instead.
```

### Dark Mode

```
Does this element need a shadow?
  |
  NO. Never. Use surface elevation colors instead.
  |
  +-- Base layer --> #0a0a0b (elevation-0)
  +-- Cards, sidebars --> #111113 (elevation-1)
  +-- Elevated cards, dropdowns --> #1A1A1C (elevation-2)
  +-- Modals, popovers --> #252527 (elevation-3)
  +-- Tooltips --> #2D2D30 (elevation-4)
```

---

## Border Selection

```
What element needs a border?
  |
  +-- Card outline (default)?
  |     --> 1px solid var(--color-border)
  |
  +-- Card outline (hover)?
  |     --> 1px solid var(--color-border-emphasis)
  |
  +-- Card outline (selected/active)?
  |     --> 1px solid var(--color-text)
  |
  +-- Input (default)?
  |     --> 1px solid var(--color-border-emphasis)
  |
  +-- Input (focused)?
  |     --> 1px solid var(--color-accent)
  |
  +-- Input (error)?
  |     --> 1px solid var(--color-error)
  |
  +-- Table row separator?
  |     --> 1px solid var(--color-border)
  |
  +-- Section divider?
        --> 1px solid var(--color-border)
```

---

## Icon Selection

### Size

```
Where is the icon used?
  |
  +-- Inline with small text (badges, captions)?
  |     --> 16x16, stroke-width 1.5
  |
  +-- Buttons, navigation, inputs?
  |     --> 20x20, stroke-width 2 [DEFAULT]
  |
  +-- Standalone or section headers?
  |     --> 24x24, stroke-width 2
  |
  +-- Hero or feature highlight?
        --> 32x32, stroke-width 2.5
```

### Style

```
How should the icon be styled?
  |
  ALWAYS:
  +-- stroke: currentColor
  +-- fill: none
  +-- Use the sizes/weights above
  |
  NEVER:
  +-- Filled icons
  +-- Colored icons (except functional indicators)
  +-- Decorative/ornamental icons
  +-- Multi-color icons
```

---

## Loading State Selection

```
How long is the operation expected to take?
  |
  +-- < 300ms?
  |     --> No indicator. Just complete the action.
  |
  +-- 300ms - 2 seconds?
  |     --> Show text "Loading..." in muted color
  |     --> Or button text changes to "Loading..."
  |
  +-- > 2 seconds?
        --> Static progress bar (determinate if possible)
        --> Or static text with percentage

NEVER:
  - Animated skeleton loaders
  - Shimmer/pulse effects
  - Spinning icons
  - Bouncing dots
```

---

## Modal/Dialog Selection

```
What type of content?
  |
  +-- Simple confirmation or alert?
  |     --> Modal small (480px)
  |
  +-- Form or moderate content?
  |     --> Modal medium (640px) [DEFAULT]
  |
  +-- Complex content or wide form?
        --> Modal large (800px)

All modals:
  - Padding: 24px
  - Border-radius: 8px
  - Background: surface-elevated
  - Backdrop: rgba(0,0,0,0.5) light / rgba(0,0,0,0.7) dark
```

---

## Z-Index Selection

```
What layer does this element occupy?
  |
  +-- Regular content?
  |     --> 0 (auto)
  |
  +-- Dropdown menu?
  |     --> 100
  |
  +-- Sticky header?
  |     --> 200
  |
  +-- Modal backdrop?
  |     --> 300
  |
  +-- Modal content?
  |     --> 400
  |
  +-- Popover (date picker, color picker)?
  |     --> 500
  |
  +-- Tooltip?
  |     --> 600
  |
  +-- Toast notification?
        --> 700
```

---

## Quick Answers

| Question | Answer |
|----------|--------|
| What font? | CrispByYosi. Always. |
| What radius for buttons? | 6px |
| What radius for cards? | 8px |
| What spacing between form fields? | 16px |
| What spacing between cards? | 24px |
| What color for primary button? | Black (light mode) / White (dark mode) |
| What color for focus ring? | Amber #f59e0b, 2px solid |
| Shadows in dark mode? | No. Use elevation colors. |
| Animated loading? | No. Static only. |
| Decorative icons? | No. Function only. |
