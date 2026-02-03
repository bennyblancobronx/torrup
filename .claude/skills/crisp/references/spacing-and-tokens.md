# Spacing and Tokens

## Spacing System (8pt Grid)

```css
--space-1: 4px;    /* Fine adjustment only */
--space-2: 8px;    /* Tight grouping */
--space-3: 12px;   /* Related elements */
--space-4: 16px;   /* Component padding - DEFAULT */
--space-5: 20px;
--space-6: 24px;   /* Section spacing */
--space-8: 32px;   /* Group separation */
--space-10: 40px;
--space-12: 48px;  /* Major sections */
--space-16: 64px;  /* Page sections */
--space-20: 80px;
--space-24: 96px;  /* Hero spacing */
```

Allowed values: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96.

---

## When to Use

| Context | Value |
|---------|-------|
| Icon margin | 4px |
| Button icon gap | 8px |
| Input padding | 10-12px |
| Card padding | 16px |
| Section gap | 24px |
| Card grid gap | 24px |
| Between form fields | 16px |
| Between page sections | 48-64px |
| Page edge (mobile) | 16px |
| Page edge (desktop) | 32px |

---

## Border Radius

| Token | Value | Use |
|-------|-------|-----|
| radius-sm | 4px | Badges, chips, tags |
| radius-md | 6px | Buttons, inputs |
| radius-lg | 8px | Cards, panels, modals |
| radius-full | 50% | Avatars, circular icons |

**Rule:** Never exceed 8px except for full circles (50%) and toggle pill shapes (9999px).

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

## Icon Sizes

| Size | Dimensions | Stroke Width | Use |
|------|------------|--------------|-----|
| sm | 16x16 | 1.5px | Inline with captions |
| md | 20x20 | 2px | Buttons, nav, inputs |
| lg | 24x24 | 2px | Standalone, section heads |
| xl | 32x32 | 2.5px | Hero, feature highlights |

### Icon Rules

- Stroke only, no fills
- Use `currentColor` for stroke
- No decorative icons -- icons must communicate function
- Exception: Status indicator dots may use functional colors

---

## Shadows (Light Mode Only)

```css
--shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
--shadow-md: 0 2px 4px rgba(0, 0, 0, 0.06);
--shadow-lg: 0 4px 8px rgba(0, 0, 0, 0.08);
```

Use sparingly. Prefer borders over shadows. **No shadows in dark mode** -- use elevation surfaces instead. See `references/dark-mode.md`.

---

## Transition Timing

| Interaction | Duration | Easing |
|-------------|----------|--------|
| hover | 100ms | ease-out |
| focus | 100ms | ease-out |
| active | 50ms | ease-out |
| color change | 150ms | ease |
| transform | 150ms | ease-out |
| modal open | 250ms | ease-out |
| modal close | 200ms | ease-in |

Max duration: 350ms. No decorative animations.
