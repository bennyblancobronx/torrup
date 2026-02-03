# Decision Trees

Flowcharts for every design decision. Follow exactly.

---

## Button Selection

```
Is it the PRIMARY action on the page?
  YES -> btn-primary (gunmetal in light, porcelain in dark)
  NO  -> Is it a SECONDARY or CANCEL action?
         YES -> btn-secondary (outlined)
         NO  -> Is it a DESTRUCTIVE action (delete, remove)?
                YES -> btn-destructive (error outline)
                NO  -> Is it the ONLY CTA needing emphasis?
                       YES -> btn-accent (configurable, default Gold #B9975C)
                       NO  -> btn-ghost (text only)
```

### Button Size

```
In a toolbar or tight space?     -> Small (32px)
Standard form or dialog?         -> Medium (44px) [DEFAULT]
Hero section or standalone CTA?  -> Large (52px)
```

---

## Typography

### Font Weight

```
Page title or hero text?                          -> 700 (Bold)
Section heading, button label, navigation item?   -> 500 (Medium)
Body text, paragraph, input value?                -> 400 (Regular)
Caption, metadata, timestamp, code, hash/ID?      -> 300 (Light)
Decorative display (rare, e.g., massive numbers)? -> 100 (Thin)

NEVER USE 600 - it does not exist in CrispByYosi
```

### Font Size

```
Uppercase label (STATUS, TYPE)?    -> 11px, 500, 0.1em spacing
Caption, metadata, code?           -> 13px, 300
Body text, input text?             -> 15px, 400 [DEFAULT]
Subsection heading?                -> 17px, 500
Section heading?                   -> 20px, 500
Page title?                        -> 24px, 700
Hero title?                        -> 30px, 700
Display (very rare)?               -> 36px, 700
```

---

## Spacing

### Component Internal

```
Icon to adjacent label?            -> 8px
Button padding (vertical)?         -> sm: 6px, md: 10px, lg: 14px
Button padding (horizontal)?       -> sm: 12px, md: 20px, lg: 28px
Input padding?                     -> 10px 12px
Card padding?                      -> 16px (standard) or 24px (spacious)
Modal padding?                     -> 24px
```

### Layout

```
Between form fields?               -> 16px
Between cards in a grid?           -> 24px
Between content sections in card?  -> 16px
Between page sections?             -> 48px (standard) or 64px (major)
Page edge padding?                 -> 24px (mobile) or 32px (desktop)
```

---

## Color

### When to Use Accent (configurable, default Gold)

```
Focused input border?              -> YES, use accent
Focus ring (outline)?              -> YES, 2px solid accent
Only CTA button needing emphasis?  -> YES, btn-accent
"New" or "highlighted" badge?      -> Consider, use sparingly
Decorative?                        -> NO. Color = function only.
```

### When to Use Functional Colors

```
Success, verified, complete?       -> #286736
Warning, attention needed?         -> #A8862B
Error, failed, destructive?        -> #AE1C09
Informational, neutral highlight?  -> #49696E
None of the above?                 -> Use text colors only
```

### Functional Color Application

```
Status badges?         -> Colored BG (subtle) + colored text
Status indicator dots? -> Solid fill with functional color
Error messages?        -> Text color only (#AE1C09)
Form validation?       -> Border color only (1px solid #AE1C09)
Numbers and values?    -> DO NOT color. Text colors only.
                          Put colored badge/dot NEXT to value.
```

---

## Border Radius

```
Badge, chip, tag?                  -> 4px
Button, input, select, textarea?   -> 6px
Card, panel, modal, dropdown?      -> 8px [MAXIMUM]
Avatar, circular icon, dot?        -> 50% (full circle)
Toggle switch track?               -> 9999px (only exception)
```

---

## Shadow

### Light Mode

```
Elevated surface (modal, dropdown)?   -> shadow-md: 0 2px 4px rgba(0,0,0,0.06)
Card needing subtle depth?            -> shadow-sm: 0 1px 2px rgba(0,0,0,0.04)
                                         Prefer borders over shadows.
Decorative effect?                    -> NO SHADOW. Use border instead.
```

### Dark Mode

```
Does this element need a shadow?      -> NO. Never.
Use surface elevation colors instead:
  Base layer       -> #1F1F1F  (elevation-0)
  Cards, sidebars  -> #2A2A2A  (elevation-1)
  Dropdowns        -> #353535  (elevation-2)
  Modals           -> #404040  (elevation-3)
  Tooltips         -> #4A4A4A  (elevation-4)
```

---

## Border

```
Card outline (default)?            -> 1px solid var(--color-border)
Card outline (hover)?              -> 1px solid var(--color-border-emphasis)
Card outline (selected/active)?    -> 1px solid var(--color-text)
Input (default)?                   -> 1px solid var(--color-border-emphasis)
Input (focused)?                   -> 1px solid var(--color-accent)
Input (error)?                     -> 1px solid var(--color-error)
Table row separator?               -> 1px solid var(--color-border)
Section divider?                   -> 1px solid var(--color-border)
```

---

## Icon

### Size

```
Inline with small text (badges)?   -> 16x16, stroke-width 1.5
Buttons, navigation, inputs?       -> 20x20, stroke-width 2 [DEFAULT]
Standalone or section headers?     -> 24x24, stroke-width 2
Hero or feature highlight?         -> 32x32, stroke-width 2.5
```

### Style

```
ALWAYS: stroke: currentColor, fill: none
NEVER:  filled icons, colored icons, decorative icons, multi-color
```

---

## Loading State

```
< 300ms?      -> No indicator
300ms - 2s?   -> Text "Loading..." in muted color
> 2s?         -> Static progress bar (determinate if possible)

NEVER: animated skeletons, shimmer, spinning icons, bouncing dots
```

---

## Modal Size

```
Simple confirmation or alert?      -> modal-sm (480px)
Form or moderate content?          -> modal-md (640px) [DEFAULT]
Complex content or wide form?      -> modal-lg (800px)

All: padding 24px, radius 8px, backdrop rgba(0,0,0,0.5/0.7)
Mobile: full-screen with safe areas
```

---

## Z-Index

```
Regular content?                   -> 0 (auto)
Dropdown menu?                     -> 100
Sticky header?                     -> 200
Modal backdrop?                    -> 300
Modal content?                     -> 400
Popover?                           -> 500
Tooltip?                           -> 600
Toast notification?                -> 700
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
| What color for primary button? | Gunmetal (light) / Porcelain (dark) |
| What color for focus ring? | Accent (default Gold #B9975C), 2px solid |
| Shadows in dark mode? | No. Elevation colors. |
| Animated loading? | No. Static only. |
| Decorative icons? | No. Function only. |
