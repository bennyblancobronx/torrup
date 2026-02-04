# Responsive

## Breakpoints

| Breakpoint | Width | Columns | Margin | Gutter |
|------------|-------|---------|--------|--------|
| Mobile | 0-639px | 4 | 16px | 16px |
| Tablet | 640-1023px | 8 | 24px | 24px |
| Desktop | 1024-1279px | 12 | 32px | 24px |
| Wide | 1280px+ | 12 | auto (centered) | 24px |

```css
.container {
  width: 100%;
  padding: 0 16px;
}

@media (min-width: 640px) {
  .container { padding: 0 24px; }
}

@media (min-width: 1024px) {
  .container { padding: 0 32px; }
}

@media (min-width: 1280px) {
  .container { max-width: 1280px; margin: 0 auto; }
}
```

---

## Content Density

### Compact (Data-heavy interfaces)

```css
.density-compact {
  --row-height: 40px;
  --cell-padding: 8px 12px;
  --card-padding: 12px;
  --btn-height: 32px;
  --btn-padding: 6px 12px;
}
```

### Default (Most interfaces)

```css
.density-default {
  --row-height: 52px;
  --cell-padding: 12px 16px;
  --card-padding: 16px;
  --btn-height: 44px;
  --btn-padding: 10px 20px;
}
```

### Spacious (Marketing, hero sections)

```css
.density-spacious {
  --card-padding: 24px;
  --btn-height: 52px;
  --btn-padding: 14px 28px;
  --section-gap: 64px;
}
```

---

## Sidebar Behavior

```
Desktop (1024+):   Visible, fixed 240px
Tablet (640-1023): Collapsible overlay
Mobile (<640):     Hidden, hamburger menu
```

```css
.sidebar {
  width: 240px;
  position: fixed;
  height: 100%;
}

@media (max-width: 1023px) {
  .sidebar {
    transform: translateX(-100%);
    z-index: 200;
    transition: transform 250ms ease;
  }
  .sidebar.is-open {
    transform: translateX(0);
  }
}
```

---

## Card Grid Reflow

```
Desktop (1024+):   3-4 columns
Tablet (640-1023): 2 columns
Mobile (<640):     1 column
```

```css
.card-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

@media (min-width: 640px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
}
```

---

## Table Behavior

```
Desktop:  Full table
Tablet:   Hide secondary columns
Mobile:   Stack as cards OR horizontal scroll
```

```css
/* Horizontal scroll on mobile */
.table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

/* Hide secondary columns on tablet */
@media (max-width: 1023px) {
  .table .col-secondary { display: none; }
}

/* Stack on mobile */
@media (max-width: 639px) {
  .table-stack thead { display: none; }
  .table-stack tr {
    display: block;
    padding: 16px;
    border-bottom: 1px solid var(--color-border);
  }
  .table-stack td {
    display: flex;
    justify-content: space-between;
    padding: 4px 0;
    border: none;
  }
  .table-stack td::before {
    content: attr(data-label);
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--color-text-muted);
  }
}
```

---

## Modal Behavior

```
Desktop:  Centered, sized (480/640/800px)
Mobile:   Full screen with safe areas
```

```css
@media (max-width: 639px) {
  .modal {
    width: 100% !important;
    height: 100%;
    max-height: 100%;
    border-radius: 0;
    padding-top: env(safe-area-inset-top);
    padding-bottom: env(safe-area-inset-bottom);
  }
}
```
