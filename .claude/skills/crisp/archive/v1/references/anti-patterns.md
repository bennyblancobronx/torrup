# Anti-Patterns Guide

Visual patterns that violate Crisp Design Language principles. If you see these, reject and fix them.

---

## Color Anti-Patterns

### Colored Accent Buttons

**VIOLATION:** Using colored backgrounds for primary actions.

```css
/* WRONG */
.btn-primary {
  background: #3B82F6; /* Blue */
  background: #10B981; /* Green */
  background: #8B5CF6; /* Purple */
}

/* CORRECT */
.btn-primary {
  background: #1C1C1A; /* Near black (light mode) */
}

[data-theme="dark"] .btn-primary {
  background: rgba(250, 250, 248, 0.87); /* Near white (dark mode) */
}
```

**Exception:** Amber accent buttons (`#f59e0b`) are allowed when specifically needed for emphasis.

---

### Gradient Overlays on Photography

**VIOLATION:** Adding colored gradients over images.

```css
/* WRONG */
.hero-image::after {
  background: linear-gradient(to bottom, rgba(0,0,0,0.5), transparent);
  background: linear-gradient(135deg, #667eea, #764ba2);
}

/* CORRECT */
.hero-image {
  /* No overlay. Let photography speak. */
}

.hero-caption {
  /* Put text below image on solid surface */
  background: var(--color-surface);
}
```

---

### Decorative Color

**VIOLATION:** Using color for visual interest rather than function.

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

**Rule:** Color communicates function only: success, error, warning, info.

---

### Pure Black or White

**VIOLATION:** Using `#000000` or `#FFFFFF`.

```css
/* WRONG */
body { background: #000000; }
.text { color: #FFFFFF; }
.card { background: #FFF; }

/* CORRECT */
body { background: #0a0a0b; }
.text { color: rgba(250, 250, 248, 0.87); }
.card { background: #FFFFFF; } /* Light mode only, #1A1A1C for dark */
```

---

## Shape Anti-Patterns

### Rounded Corners > 8px

**VIOLATION:** Large border radii creating "pill" or "bubble" shapes.

```css
/* WRONG */
.card { border-radius: 12px; }
.btn { border-radius: 9999px; }
.avatar { border-radius: 16px; }
.panel { border-radius: 20px; }

/* CORRECT */
.card { border-radius: 8px; }
.btn { border-radius: 6px; }
.avatar { border-radius: 50%; } /* Full circle OK */
.panel { border-radius: 8px; }
```

**Exception:** Toggle switches and indicators may use pill shape (`9999px`).

---

### Arbitrary Curves

**VIOLATION:** Organic, expressive, or "blob" shapes.

```css
/* WRONG */
.decoration {
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
}

.wave-divider {
  clip-path: url(#wave-path);
}

.blob {
  border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
}

/* CORRECT */
.divider {
  border-bottom: 1px solid var(--color-border);
}
```

**Rule:** All curves must be mathematically derived. Circles, straight lines, rectangles only.

---

## Shadow Anti-Patterns

### Decorative Shadows

**VIOLATION:** Heavy shadows for visual effect.

```css
/* WRONG */
.card {
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

/* CORRECT - Light mode only */
.card {
  border: 1px solid var(--color-border);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

/* CORRECT - Dark mode */
[data-theme="dark"] .card {
  background: var(--elevation-2);
  box-shadow: none;
}
```

---

### Decorative Glows

**VIOLATION:** Colored glows or halos.

```css
/* WRONG */
.btn:hover {
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
}

.input:focus {
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.3);
}

.card-glow {
  box-shadow: 0 0 30px rgba(139, 92, 246, 0.3);
}

/* CORRECT */
.btn:hover {
  background: #333330;
}

.input:focus {
  border-color: var(--color-accent);
  outline: none;
}

.card {
  border: 1px solid var(--color-border);
}
```

---

## Typography Anti-Patterns

### Multiple Font Families

**VIOLATION:** Using different typefaces for different elements.

```css
/* WRONG - ANY of these */
h1 { font-family: 'Playfair Display', serif; }
body { font-family: 'Inter', sans-serif; }
code { font-family: 'JetBrains Mono', monospace; }
.accent { font-family: 'Lobster', cursive; }
.heading { font-family: 'Montserrat', sans-serif; }

/* CORRECT - CrispByYosi ONLY */
* {
  font-family: 'CrispByYosi', system-ui, sans-serif;
}

code, pre {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-weight: 300; /* Use Light weight for code */
}
```

---

### Text Shadows

**VIOLATION:** Shadows on text for style.

```css
/* WRONG */
.hero-title {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.glow-text {
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

/* CORRECT */
.hero-title {
  color: var(--color-text);
  /* No shadow */
}
```

---

### Gradient Text

**VIOLATION:** Gradient fills on text.

```css
/* WRONG */
.fancy-title {
  background: linear-gradient(90deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* CORRECT */
.title {
  color: var(--color-text);
}
```

---

### Wrong Font Weights

**VIOLATION:** Using weights that don't exist in CrispByYosi.

```css
/* WRONG - 600 doesn't exist */
.heading { font-weight: 600; }
.semi-bold { font-weight: 600; }

/* CORRECT */
.heading { font-weight: 500; } /* Medium */
/* OR */
.heading { font-weight: 700; } /* Bold */
```

**Available weights:** 100 (Thin), 300 (Light), 400 (Regular), 500 (Medium), 700 (Bold)

---

## Animation Anti-Patterns

### Animated Loading Skeletons

**VIOLATION:** Shimmer/pulse animations on placeholders.

```css
/* WRONG */
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* CORRECT */
.loading-placeholder {
  background: var(--color-surface);
  /* Static. No animation. */
}
```

---

### Decorative Motion

**VIOLATION:** Bounces, pulses, attention-seeking animation.

```css
/* WRONG */
.notification-badge {
  animation: pulse 2s infinite;
}

.cta-button {
  animation: bounce 1s infinite;
}

.icon {
  animation: spin 2s linear infinite;
}

.floating {
  animation: float 3s ease-in-out infinite;
}

/* CORRECT */
/* No decorative animations */
.element {
  transition: opacity 150ms ease;
}
```

**Rule:** Motion informs, not entertains. Transitions only, no animations.

---

### Slow Transitions

**VIOLATION:** Transitions longer than 350ms.

```css
/* WRONG */
.card {
  transition: all 500ms ease;
  transition: transform 1s ease-out;
}

/* CORRECT */
.card {
  transition: border-color 150ms ease;
}
```

**Allowed durations:** 100ms (fast), 150ms (normal), 250ms (slow), 350ms (slower/max)

---

## Spacing Anti-Patterns

### Non-Grid Spacing

**VIOLATION:** Arbitrary spacing values not on 8pt grid.

```css
/* WRONG */
.card { padding: 18px; }
.section { margin-bottom: 50px; }
.button { padding: 10px 22px; }
.gap { gap: 15px; }
.margin { margin: 30px; }

/* CORRECT */
.card { padding: 16px; }
.section { margin-bottom: 48px; }
.button { padding: 10px 20px; }
.gap { gap: 16px; }
.margin { margin: 32px; }
```

**Allowed values:** 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96...

---

## Icon Anti-Patterns

### Ornamental Icons

**VIOLATION:** Decorative icons without function.

```css
/* WRONG */
.feature::before {
  content: '★';
}

.section-header .decorative-icon {
  /* purely visual */
}

.sparkle-icon {
  /* decoration only */
}

/* CORRECT */
/* Icons only when they communicate function */
/* Search icon for search */
/* Settings icon for settings */
/* No decorative stars, sparkles, etc. */
```

---

### Filled/Colored Icons

**VIOLATION:** Icons with fills or multiple colors.

```css
/* WRONG */
.icon {
  fill: linear-gradient(#667eea, #764ba2);
  fill: #3B82F6;
}

.icon-colored {
  fill: var(--color-success);
}

/* CORRECT */
.icon {
  stroke: currentColor;
  fill: none;
  stroke-width: 2;
}
```

**Exception:** Status indicators (dots) may use functional colors.

---

### Wrong Icon Sizes

**VIOLATION:** Non-standard icon sizes.

```css
/* WRONG */
.icon { width: 18px; height: 18px; }
.icon { width: 22px; height: 22px; }
.icon { width: 28px; height: 28px; }

/* CORRECT */
.icon-sm { width: 16px; height: 16px; }
.icon-md { width: 20px; height: 20px; }
.icon-lg { width: 24px; height: 24px; }
.icon-xl { width: 32px; height: 32px; }
```

---

## Layout Anti-Patterns

### Non-Standard Widths

**VIOLATION:** Arbitrary container or modal widths.

```css
/* WRONG */
.modal { width: 500px; }
.sidebar { width: 260px; }
.container { max-width: 1400px; }

/* CORRECT */
.modal-sm { width: 480px; }
.modal-md { width: 640px; }
.modal-lg { width: 800px; }
.sidebar { width: 240px; }
.container { max-width: 1280px; }
```

---

## Quick Verification

For any UI element, ask:

| Question | If Yes... |
|----------|-----------|
| Is there color? | Must communicate function (success/error/warning) |
| Is there a shadow? | Must communicate elevation (light mode only) |
| Is there animation? | Must be functional feedback only (transitions) |
| Is there decoration? | Remove it |
| Is spacing off-grid? | Fix to 8pt multiple |
| Is border-radius > 8px? | Reduce (unless 50% circle or toggle) |
| Is font CrispByYosi? | If not, fix it - ONLY CrispByYosi allowed |
| Is it pure black/white? | Use off-black/off-white instead |

**If any element exists purely for visual interest, it violates the design language.**

---

## Rejection Checklist

Reject any UI that contains:

- [ ] Colored buttons (except amber accent)
- [ ] Gradient backgrounds or overlays
- [ ] Drop shadows in dark mode
- [ ] Decorative shadows or glows
- [ ] Border-radius > 8px (except circles/toggles)
- [ ] Animated loading skeletons
- [ ] Pulse, bounce, or spin animations
- [ ] Text shadows or gradient text
- [ ] Multiple font families
- [ ] Non-Crisp-Linear fonts
- [ ] Non-grid spacing values
- [ ] Pure black (#000) or white (#FFF)
- [ ] Decorative icons or illustrations
- [ ] Filled or colored icons
- [ ] Blob or organic shapes
- [ ] Wave dividers
