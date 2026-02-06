# Torrup GUI Guide - Overview

Complete interface specification for the Torrup (Torrent Upload Tool) web application.

## Overview

| Property | Value |
|----------|-------|
| **App Name** | Torrup |
| **Logo** | Text-based "Torrup" (no graphics) |
| **Framework** | Flask + Jinja2 templates |
| **Styling** | Vanilla CSS (Crisp Design Language) |
| **JavaScript** | Vanilla JS (no framework) |
| **Target** | Docker web app, beginner-friendly |
| **Design Language** | Crisp |

---

## Page Structure

```
Torrup
+-- 1. Dashboard     /              Stats, quick actions, system status
+-- 2. Browse        /browse        Media library browser
+-- 3. Queue         /queue         Upload queue management
+-- 4. History       /history       Upload history and logs
+-- 5. Settings      /settings      All configuration
```

---

## Shared Layout

Every page uses the same header and optional footer.

### Header Bar

```
+----------------------------------------------------------------------+
|  Torrup                 [Dashboard] [Browse] [Queue] [History] [Settings]  |
|  v0.1.0                                                    [Worker: ON]   |
+----------------------------------------------------------------------+
```

| Element | Description |
|---------|-------------|
| **Logo** | "Torrup" in CrispByYosi Bold (700) |
| **Version** | text-sm muted below logo |
| **Nav Links** | 5 main pages, highlight current page |
| **Worker Status** | Green dot when running, red when stopped |

### Footer (Optional)

```
+----------------------------------------------------------------------+
|  Multi-tracker batch uploader  -  Local-first  -  Docker ready        |
+----------------------------------------------------------------------+
```

---

## Design System (Crisp)

### Font

CrispByYosi is the ONLY font. No exceptions.

```css
font-family: 'CrispByYosi', system-ui, sans-serif;
```

### Color Palette (Dark Mode - Default)

| Name | Value | Usage |
|------|-------|-------|
| `canvas` | `#1F1F1F` | Page background |
| `surface` | `#2A2A2A` | Card/panel background |
| `surface-elevated` | `#353535` | Modals, dropdowns |
| `border` | `#353535` | Panel borders |
| `border-emphasis` | `#4A4A4A` | Input borders |
| `text` | `rgba(255,251,247,0.87)` | Primary text |
| `text-secondary` | `rgba(255,251,247,0.60)` | Descriptions |
| `text-muted` | `rgba(255,251,247,0.38)` | Captions, meta |
| `accent` | `#D4BF9B` | Links, accent elements |
| `accent-hover` | `#B9975C` | Hover state |
| `success` | `#286736` | Success status |
| `error` | `#AE1C09` | Error/failed status |
| `warning` | `#A8862B` | Warning/duplicate status |
| `info` | `#49696E` | Info/uploading status |

### Color Palette (Light Mode)

| Name | Value | Usage |
|------|-------|-------|
| `canvas` | `#fff8f2` | Page background |
| `surface` | `#FFFBF7` | Card/panel background |
| `surface-elevated` | `#FFFBF7` | Modals, dropdowns |
| `border` | `rgba(212,191,155,0.40)` | Panel borders |
| `border-emphasis` | `rgba(122,122,122,0.40)` | Input borders |
| `text` | `#1F1F1F` | Primary text |
| `text-secondary` | `#454545` | Descriptions |
| `text-muted` | `#7A7A7A` | Captions, meta |
| `accent` | `#B9975C` | Links, accent elements |
| `accent-hover` | `#725A31` | Hover state |

### Typography

| Element | Size | Weight | Line Height | Use |
|---------|------|--------|-------------|-----|
| Logo | 24px | 700 | 1.3 | App name |
| Page Title | 24px | 700 | 1.3 | Page headings |
| Section Title | 20px | 500 | 1.4 | Card headers |
| Subsection | 17px | 500 | 1.5 | Sub-headers |
| Body | 15px | 400 | 1.6 | Default text |
| Caption/Meta | 13px | 300 | 1.5 | Muted text, code |
| Labels | 11px | 500 | 1.3 | Uppercase labels |

Weight 600 does NOT exist. Use 500 or 700.

### Spacing (8pt Grid)

| Context | Value |
|---------|-------|
| Icon margin | 4px |
| Button icon gap | 8px |
| Input padding | 10-12px |
| Card padding | 16px |
| Section gap | 24px |
| Card grid gap | 24px |
| Page sections | 48-64px |

### Border Radius

| Use | Value |
|-----|-------|
| Badges | 4px |
| Buttons, inputs | 6px |
| Cards, panels | 8px |
| Avatars, circles | 50% |

Never exceed 8px except for full circles.

---

## Components

### Panel

```css
.panel {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}
```

### Button Primary

```css
.btn-primary {
  background: rgba(255, 251, 247, 0.87);
  color: #1F1F1F;
  border: none;
  border-radius: 6px;
  padding: 10px 20px;
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-weight: 500;
  font-size: 15px;
  cursor: pointer;
  transition: background-color 100ms ease-out;
}

.btn-primary:hover:not(:disabled) {
  background: rgba(255, 251, 247, 0.75);
}
```

### Button Secondary

```css
.btn-secondary {
  background: transparent;
  color: var(--color-text);
  border: 1px solid var(--color-border-emphasis);
  border-radius: 6px;
  padding: 10px 20px;
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-weight: 500;
  font-size: 15px;
  cursor: pointer;
}

.btn-secondary:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.05);
  border-color: #4A4A4A;
}
```

### Button Ghost

```css
.btn-ghost {
  background: transparent;
  color: var(--color-text-secondary);
  border: none;
  border-radius: 6px;
  padding: 10px 20px;
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-weight: 500;
  font-size: 15px;
  cursor: pointer;
}

.btn-ghost:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-text);
}
```

### Input

```css
input, select, textarea {
  display: block;
  width: 100%;
  height: 44px;
  padding: 10px 12px;
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 400;
  color: var(--color-text);
  background: var(--color-surface-elevated);
  border: 1px solid var(--color-border-emphasis);
  border-radius: 6px;
  transition: border-color 100ms ease-out;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--color-accent);
}
```

### Status Badge

```css
.badge {
  display: inline-flex;
  align-items: center;
  height: 24px;
  padding: 0 8px;
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border-radius: 4px;
}

.badge-neutral {
  background: var(--color-surface);
  color: var(--color-text-secondary);
}

.badge-info {
  background: var(--color-info-surface);
  color: var(--color-info-foreground);
}

.badge-success {
  background: var(--color-success-surface);
  color: var(--color-success-foreground);
}

.badge-error {
  background: var(--color-error-surface);
  color: var(--color-error-foreground);
}

.badge-warning {
  background: var(--color-warning-surface);
  color: var(--color-warning-foreground);
}
```

### Table

```css
table {
  width: 100%;
  border-collapse: collapse;
}

th {
  height: 48px;
  padding: 12px 16px;
  text-align: left;
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-text-muted);
  border-bottom: 1px solid var(--color-border);
}

td {
  height: 52px;
  padding: 12px 16px;
  font-size: 15px;
  border-bottom: 1px solid var(--color-border);
}

tr:hover td {
  background: rgba(255, 255, 255, 0.03);
}
```

---

## Crisp Verification Checklist

Before committing any UI:

- [ ] Font is CrispByYosi (check ALL text)
- [ ] All spacing values on 8pt grid
- [ ] No border-radius > 8px (except 50% circles)
- [ ] No pure black (#000) or pure white (#FFF)
- [ ] No decorative colors (color = function only)
- [ ] No decorative shadows in dark mode
- [ ] No animated skeletons or loaders
- [ ] All interactive states defined
- [ ] Touch targets >= 44px
- [ ] Contrast ratio >= 4.5:1
- [ ] Focus states visible (2px accent outline)
- [ ] Dark mode tested

---

## Anti-Patterns (REJECT)

- Multiple font families
- Colored accent buttons (use neutral primary)
- Gradient overlays
- Decorative shadows in dark mode
- Border-radius > 8px
- Animated loading skeletons
- Pure black (#000) or white (#FFF)
- Font-weight 600 (doesn't exist)
- Non-grid spacing values
- Decorative icons

---

## Related Documents

- [Pages](pages.md) - Page wireframes and components
- [API](api.md) - API endpoints and responses
- [Implementation](implementation.md) - Phases and file structure
