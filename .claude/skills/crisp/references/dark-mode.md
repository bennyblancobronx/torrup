# Dark Mode

## Core Principles

1. **Never pure black** -- Use `#1F1F1F` minimum for backgrounds
2. **Never pure white** -- Use `rgba(255,251,247,0.87)` for text
3. **Elevation through lightness** -- Higher surfaces are lighter (no shadows)
4. **Desaturate slightly** -- Reduce color intensity by ~10-15%
5. **Maintain contrast** -- WCAG AA minimum (4.5:1 for text)

---

## Theme Detection

Default to system preference, fallback to light:

```css
:root {
  color-scheme: light dark;

  --color-canvas: #fff8f2;
  --color-surface: #FFFBF7;
  --color-surface-elevated: #FFFBF7;
  --color-text: #1F1F1F;
  --color-text-secondary: #454545;
  --color-text-muted: #7A7A7A;
  --color-border: rgba(212,191,155,0.40);
  --color-border-emphasis: rgba(122,122,122,0.40);
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-canvas: #1F1F1F;
    --color-surface: #2A2A2A;
    --color-surface-elevated: #353535;
    --color-text: rgba(255,251,247,0.87);
    --color-text-secondary: rgba(255,251,247,0.60);
    --color-text-muted: rgba(255,251,247,0.38);
    --color-border: #353535;
    --color-border-emphasis: #4A4A4A;
  }
}
```

---

## Manual Theme Override

```css
[data-theme="light"] {
  --color-canvas: #fff8f2;
  --color-surface: #FFFBF7;
  --color-surface-elevated: #FFFBF7;
  --color-text: #1F1F1F;
  --color-text-secondary: #454545;
  --color-text-muted: #7A7A7A;
  --color-border: rgba(212,191,155,0.40);
  --color-border-emphasis: rgba(122,122,122,0.40);
}

[data-theme="dark"] {
  --color-canvas: #1F1F1F;
  --color-surface: #2A2A2A;
  --color-surface-elevated: #353535;
  --color-text: rgba(255,251,247,0.87);
  --color-text-secondary: rgba(255,251,247,0.60);
  --color-text-muted: rgba(255,251,247,0.38);
  --color-border: #353535;
  --color-border-emphasis: #4A4A4A;
}
```

---

## JavaScript Toggle

```javascript
function setTheme(theme) {
  if (theme === 'system') {
    document.documentElement.removeAttribute('data-theme');
    localStorage.removeItem('theme');
  } else {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }
}

function initTheme() {
  const saved = localStorage.getItem('theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
  }
}
```

---

## Elevation System (Dark Mode Only)

In dark mode, elevation is communicated through surface lightness, not shadows.

| Level | Surface | Use |
|-------|---------|-----|
| 0 (Base) | #1F1F1F | App background |
| 1 | #2A2A2A | Cards, sidebars |
| 2 | #353535 | Elevated cards, dropdowns |
| 3 | #404040 | Modals, popovers |
| 4 | #4A4A4A | Tooltips, highest layer |

```css
[data-theme="dark"] {
  --elevation-0: #1F1F1F;
  --elevation-1: #2A2A2A;
  --elevation-2: #353535;
  --elevation-3: #404040;
  --elevation-4: #4A4A4A;
}
```

---

## Component Adaptations

### Buttons

```css
[data-theme="dark"] .btn-primary { background: rgba(255,251,247,0.87); color: #1F1F1F; }
[data-theme="dark"] .btn-primary:hover { background: rgba(255,251,247,0.75); }
[data-theme="dark"] .btn-secondary { border-color: #4A4A4A; color: rgba(255,251,247,0.87); }
[data-theme="dark"] .btn-secondary:hover { border-color: #4A4A4A; }
```

### Inputs

```css
[data-theme="dark"] .input { background: #2A2A2A; border-color: #4A4A4A; color: rgba(255,251,247,0.87); }
[data-theme="dark"] .input:focus { border-color: #D4BF9B; }
[data-theme="dark"] .input::placeholder { color: rgba(255,251,247,0.38); }
```

### Cards

```css
[data-theme="dark"] .card { background: #353535; border-color: #353535; box-shadow: none; }
[data-theme="dark"] .card:hover { border-color: #4A4A4A; }
```

### Navigation

```css
[data-theme="dark"] .nav-item { color: rgba(255,251,247,0.60); }
[data-theme="dark"] .nav-item:hover,
[data-theme="dark"] .nav-item.is-active {
  background: rgba(255,255,255,0.05);
  color: rgba(255,251,247,0.87);
}
```

---

## Shadow Rules

### Light Mode

```css
--shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
--shadow-md: 0 2px 4px rgba(0,0,0,0.06);
--shadow-lg: 0 4px 8px rgba(0,0,0,0.08);
```

### Dark Mode

**NO shadows.** Use surface lightness for elevation instead.

```css
[data-theme="dark"] .card { box-shadow: none; background: var(--elevation-2); }
[data-theme="dark"] .modal { box-shadow: none; background: var(--elevation-3); }
```

---

## Contrast Verification

| Combination | Ratio | Pass |
|-------------|-------|------|
| #FFFBF7 on #1F1F1F | ~14.5:1 | Yes |
| rgba(255,251,247,0.87) on #1F1F1F | ~12.0:1 | Yes |
| rgba(255,251,247,0.60) on #2A2A2A | ~7.5:1 | Yes |
| rgba(255,251,247,0.38) on #353535 | ~4.2:1 | Borderline -- captions only |
| #D4BF9B on #1F1F1F | ~8.5:1 | Yes |

---

## Implementation Checklist

- [ ] Add `color-scheme: light dark` to `:root`
- [ ] Define all tokens with CSS custom properties
- [ ] Add `@media (prefers-color-scheme: dark)` rules
- [ ] Add `[data-theme="dark"]` override rules
- [ ] Remove all shadows in dark mode
- [ ] Use elevation surfaces instead of shadows
- [ ] Test all functional colors for contrast
- [ ] Verify focus states are visible
- [ ] Check scrollbar styling
- [ ] Test images against dark background
- [ ] Verify form elements are readable
- [ ] Test all badge/status colors
