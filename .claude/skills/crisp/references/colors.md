# Colors

## Light Mode

| Token | Value | Use |
|-------|-------|-----|
| canvas | #fff8f2 | App background |
| surface | #FFFBF7 | Cards, panels |
| surface-elevated | #FFFBF7 | Modals, dropdowns |
| text | #1F1F1F | Primary text |
| text-secondary | #454545 | Descriptions |
| text-muted | #7A7A7A | Captions, meta |
| text-disabled | rgba(122,122,122,0.50) | Disabled states |
| border | rgba(212,191,155,0.40) | Default borders |
| border-subtle | rgba(255,235,214,0.50) | Subtle dividers |
| border-emphasis | rgba(122,122,122,0.40) | Input borders, emphasis |

Solid hex fallbacks for non-alpha contexts:

| Token | rgba | Approx Solid Hex |
|-------|------|-------------------|
| border | rgba(212,191,155,0.40) | #EDE3D4 |
| border-emphasis | rgba(122,122,122,0.40) | #C2BAB1 |
| border-subtle | rgba(255,235,214,0.50) | #FFF1E2 |

---

## Dark Mode

| Token | Value | Use |
|-------|-------|-----|
| canvas | #1F1F1F | App background |
| surface | #2A2A2A | Cards, panels |
| surface-elevated | #353535 | Modals, dropdowns |
| text | rgba(255,251,247,0.87) | Primary text |
| text-secondary | rgba(255,251,247,0.60) | Descriptions |
| text-muted | rgba(255,251,247,0.38) | Captions, meta |
| text-disabled | rgba(255,251,247,0.38) | Disabled states |
| border | #353535 | Default borders |
| border-subtle | #2A2A2A | Subtle dividers |
| border-emphasis | #4A4A4A | Input borders |

---

## Functional Colors (Both Modes)

| Function | Main | Light Variant | Dark Variant | Status |
|----------|------|---------------|--------------|--------|
| success | #286736 Dark Emerald | #39934D Sea Green | #173B1F Deep Forest | Locked |
| warning | #A8862B Raw Sienna | #D4AD4A Harvest Gold | #6B5518 Bronze | Locked |
| error | #AE1C09 Oxidized Iron | #F5533D Tomato | #741306 Molten Lava | Locked |
| info | #49696E Blue Slate | #91B1B6 Cool Steel | #314649 Dark Slate Gray | Locked |

### Functional Badge Backgrounds

| Status | Light BG | Light Text | Dark BG | Dark Text |
|--------|----------|------------|---------|-----------|
| success | rgba(40,103,54,0.10) | #173B1F | rgba(57,147,77,0.15) | #39934D |
| warning | rgba(168,134,43,0.10) | #6B5518 | rgba(212,173,74,0.15) | #D4AD4A |
| error | rgba(174,28,9,0.10) | #741306 | rgba(245,83,61,0.15) | #F5533D |
| info | rgba(73,105,110,0.10) | #314649 | rgba(145,177,182,0.15) | #91B1B6 |

---

## Accent (Configurable Per App)

The accent is the only color that changes between apps. Everything else is locked. Default: Gold (#B9975C). Set via `crisp.config.json`.

| Token | Light | Dark |
|-------|-------|------|
| accent | #B9975C Camel | #D4BF9B Pale Oak |
| accent-hover | #725A31 Olive Bark | #B9975C Camel |
| accent-surface | #FFEBD6 Antique White | rgba(185,151,92,0.15) |
| accent-foreground | #1F1F1F | #1F1F1F |

Use sparingly for:
- Focus states (2px outline)
- Single emphasized CTA (btn-accent)
- New/highlighted badges

---

## Usage Rules

1. **Color communicates function only.** No decorative color.
2. **Status dots** are the ONLY place functional colors appear as solid fills.
3. **Numbers and values are NEVER colored.** Use text colors only; place a colored badge or dot next to the value if needed.
4. **No pure black (#000) or white (#FFF).** Use the off-black/off-white tokens.
5. **No gradients.** Flat fills only.

---

## CSS Custom Properties

```css
:root {
  --color-canvas: #fff8f2;
  --color-surface: #FFFBF7;
  --color-surface-elevated: #FFFBF7;
  --color-text: #1F1F1F;
  --color-text-secondary: #454545;
  --color-text-muted: #7A7A7A;
  --color-border: rgba(212,191,155,0.40);
  --color-border-emphasis: rgba(122,122,122,0.40);
  --color-accent: #B9975C;
  --color-accent-hover: #725A31;
  --color-success: #286736;
  --color-warning: #A8862B;
  --color-error: #AE1C09;
  --color-info: #49696E;
}
```

See `references/dark-mode.md` for the dark mode variable overrides.
