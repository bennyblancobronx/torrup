# Anti-Patterns

Patterns that violate the Crisp Design Language. Reject and fix.

---

## Color

### Colored Accent Buttons

```css
/* WRONG */
.btn-primary { background: #3B82F6; }
.btn-primary { background: #10B981; }
.btn-primary { background: #8B5CF6; }

/* CORRECT */
.btn-primary { background: #454545; }
[data-theme="dark"] .btn-primary { background: rgba(255,251,247,0.87); }
```

Exception: Accent buttons (configurable, default Gold #B9975C) for emphasis.

### Gradient Overlays

```css
/* WRONG */
.hero-image::after { background: linear-gradient(to bottom, rgba(0,0,0,0.5), transparent); }

/* CORRECT - no overlay, text below image on solid surface */
.hero-caption { background: var(--color-surface); }
```

### Decorative Color

```css
/* WRONG */
.sidebar { border-left: 4px solid #3B82F6; }
.card-accent { background: linear-gradient(90deg, #F0FDFA, #FFFFFF); }
.tag { background: #EEF2FF; color: #4F46E5; }

/* CORRECT */
.sidebar { border-left: none; }
.card-accent { background: var(--color-surface); }
.tag { background: var(--color-surface); color: var(--color-text-secondary); }
```

Color communicates function only: success, error, warning, info.

### Pure Black or White

```css
/* WRONG */
body { background: #000000; }
.text { color: #FFFFFF; }

/* CORRECT */
body { background: #1F1F1F; }
.text { color: rgba(255,251,247,0.87); }
```

---

## Shape

### Rounded Corners > 8px

```css
/* WRONG */
.card { border-radius: 12px; }
.btn { border-radius: 9999px; }
.panel { border-radius: 20px; }

/* CORRECT */
.card { border-radius: 8px; }
.btn { border-radius: 6px; }
.avatar { border-radius: 50%; } /* circles OK */
```

Exception: Toggle switches use pill shape (9999px).

### Arbitrary Curves

```css
/* WRONG */
.decoration { border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; }
.wave-divider { clip-path: url(#wave-path); }

/* CORRECT */
.divider { border-bottom: 1px solid var(--color-border); }
```

All curves must be mathematically derived. Circles, lines, rectangles only.

---

## Shadows

### Decorative Shadows

```css
/* WRONG */
.card { box-shadow: 0 10px 40px rgba(0,0,0,0.2); }

/* CORRECT - light mode only */
.card { border: 1px solid var(--color-border); box-shadow: 0 1px 3px rgba(0,0,0,0.04); }

/* CORRECT - dark mode */
[data-theme="dark"] .card { background: var(--elevation-2); box-shadow: none; }
```

### Glows

```css
/* WRONG */
.btn:hover { box-shadow: 0 0 20px rgba(59,130,246,0.5); }
.input:focus { box-shadow: 0 0 0 4px rgba(59,130,246,0.3); }

/* CORRECT */
.btn:hover { background: #1F1F1F; }
.input:focus { border-color: var(--color-accent); outline: none; }
```

---

## Typography

### Multiple Font Families

```css
/* WRONG */
h1 { font-family: 'Playfair Display', serif; }
body { font-family: 'Inter', sans-serif; }
code { font-family: 'JetBrains Mono', monospace; }

/* CORRECT */
* { font-family: 'CrispByYosi', system-ui, sans-serif; }
code { font-family: 'CrispByYosi', system-ui, sans-serif; font-weight: 300; }
```

### Text Shadows

```css
/* WRONG */
.hero-title { text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }

/* CORRECT */
.hero-title { color: var(--color-text); }
```

### Gradient Text

```css
/* WRONG */
.fancy-title {
  background: linear-gradient(90deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* CORRECT */
.title { color: var(--color-text); }
```

### Wrong Font Weights

```css
/* WRONG - 600 does not exist */
.heading { font-weight: 600; }

/* CORRECT */
.heading { font-weight: 500; } /* or 700 */
```

Available weights: 100, 300, 400, 500, 700.

---

## Animation

### Animated Loading Skeletons

```css
/* WRONG */
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  animation: shimmer 1.5s infinite;
}

/* CORRECT */
.loading-placeholder { background: var(--color-surface); }
```

### Decorative Motion

```css
/* WRONG */
.notification-badge { animation: pulse 2s infinite; }
.cta-button { animation: bounce 1s infinite; }
.icon { animation: spin 2s linear infinite; }

/* CORRECT */
.element { transition: opacity 150ms ease; }
```

Motion informs, not entertains. Transitions only, no animations.

### Slow Transitions

```css
/* WRONG */
.card { transition: all 500ms ease; }

/* CORRECT */
.card { transition: border-color 150ms ease; }
```

Allowed durations: 100ms, 150ms, 250ms, 350ms (max).

---

## Spacing

### Non-Grid Spacing

```css
/* WRONG */
.card { padding: 18px; }
.section { margin-bottom: 50px; }
.gap { gap: 15px; }

/* CORRECT */
.card { padding: 16px; }
.section { margin-bottom: 48px; }
.gap { gap: 16px; }
```

Allowed values: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96.

---

## Icons

### Ornamental Icons

```css
/* WRONG */
.feature::before { content: '*'; } /* decorative */

/* CORRECT - icons communicate function only */
```

### Filled/Colored Icons

```css
/* WRONG */
.icon { fill: #3B82F6; }

/* CORRECT */
.icon { stroke: currentColor; fill: none; stroke-width: 2; }
```

Exception: Status indicator dots use functional colors.

### Wrong Icon Sizes

```css
/* WRONG */
.icon { width: 18px; height: 18px; }

/* CORRECT */
.icon-sm { width: 16px; height: 16px; }
.icon-md { width: 20px; height: 20px; }
.icon-lg { width: 24px; height: 24px; }
.icon-xl { width: 32px; height: 32px; }
```

---

## Layout

### Non-Standard Widths

```css
/* WRONG */
.modal { width: 500px; }
.sidebar { width: 260px; }

/* CORRECT */
.modal-sm { width: 480px; }
.modal-md { width: 640px; }
.modal-lg { width: 800px; }
.sidebar { width: 240px; }
```

---

## Quick Verification

| Question | If Yes... |
|----------|-----------|
| Is there color? | Must communicate function |
| Is there a shadow? | Must communicate elevation (light only) |
| Is there animation? | Must be functional feedback only |
| Is there decoration? | Remove it |
| Is spacing off-grid? | Fix to 8pt multiple |
| Is radius > 8px? | Reduce (unless circle or toggle) |
| Is font CrispByYosi? | If not, fix it |
| Is it pure black/white? | Use off-black/off-white |

If any element exists purely for visual interest, it violates the design language.
