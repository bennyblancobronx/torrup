# Layout Templates

Exact specifications for common page layouts. Copy these patterns exactly.

---

## Dashboard Layout

```
+------------------------------------------------------------------+
|  HEADER (64px)                                      [Avatar] [⋮] |
|  [Logo]  breadcrumb / title                                      |
+----------+-------------------------------------------------------+
|          |                                                       |
| SIDEBAR  |  MAIN CONTENT                                         |
| (240px)  |                                                       |
|          |  +-------------+ +-------------+ +-------------+      |
| [Nav]    |  |   CARD      | |   CARD      | |   CARD      |      |
| [Nav]    |  |             | |             | |             |      |
| [Nav]    |  +-------------+ +-------------+ +-------------+      |
| ------   |                                                       |
| [Nav]    |  +--------------------------------------------------+ |
| [Nav]    |  |                                                  | |
|          |  |  CONTENT AREA                                    | |
|          |  |                                                  | |
|          |  +--------------------------------------------------+ |
+----------+-------------------------------------------------------+
```

### Specifications

```css
/* Header */
.header {
  height: 64px;
  padding: 0 24px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Sidebar */
.sidebar {
  width: 240px;
  padding: 24px 16px;
  border-right: 1px solid var(--color-border);
}

/* Main Content */
.main {
  padding: 32px;
  flex: 1;
}

/* Card Grid */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}
```

---

## Settings/Form Layout

```
+------------------------------------------------------------------+
|  HEADER (64px)                                                   |
+----------+-------------------------------------------------------+
|          |                                                       |
| NAV      |  FORM CONTENT (max-width: 640px)                      |
| (200px)  |                                                       |
|          |  Section Title (24px / 700)                           |
| [Tab]    |  Description text (15px / 400)                        |
| [Tab]    |                                                       |
| [Tab]    |  +--------------------------------------------------+ |
| [Tab]    |  | Form Field                                       | |
|          |  +--------------------------------------------------+ |
|          |                                                       |
|          |  +--------------------------------------------------+ |
|          |  | Form Field                                       | |
|          |  +--------------------------------------------------+ |
|          |                                                       |
|          |  [Cancel]                    [Save Changes]           |
+----------+-------------------------------------------------------+
```

### Specifications

```css
/* Settings Nav */
.settings-nav {
  width: 200px;
  padding: 24px 0;
}

.settings-nav-item {
  padding: 10px 16px;
  font-size: 15px;
  font-weight: 400;
  color: var(--color-text-secondary);
  border-radius: 6px;
}

.settings-nav-item.is-active {
  background: rgba(0, 0, 0, 0.03); /* light */
  color: var(--color-text);
  font-weight: 500;
}

/* Form Container */
.form-container {
  max-width: 640px;
  padding: 32px;
}

/* Form Sections */
.form-section {
  margin-bottom: 48px;
}

.form-section-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 8px;
}

.form-section-desc {
  font-size: 15px;
  color: var(--color-text-secondary);
  margin-bottom: 24px;
}

/* Form Fields */
.form-field {
  margin-bottom: 16px;
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--color-border);
}
```

---

## Data Table Layout

```
+------------------------------------------------------------------+
|  TOOLBAR                                                         |
|  [Search________]  [Filter ▼]  [Sort ▼]        [+ Add] [Actions] |
+------------------------------------------------------------------+
|  NAME ▲      | STATUS    | DATE       | AMOUNT    | ACTIONS      |
+------------------------------------------------------------------+
|  Item One    | Active    | Jan 15     | $1,234    | [⋮]          |
|  Item Two    | Pending   | Jan 14     | $567      | [⋮]          |
|  Item Three  | Complete  | Jan 13     | $8,901    | [⋮]          |
+------------------------------------------------------------------+
|  [<] Page 1 of 10 [>]                            Showing 1-10    |
+------------------------------------------------------------------+
```

### Specifications

```css
/* Toolbar */
.table-toolbar {
  padding: 16px 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  border-bottom: 1px solid var(--color-border);
}

/* Table */
.data-table {
  width: 100%;
  border-collapse: collapse;
}

/* Header */
.data-table th {
  height: 48px;
  padding: 12px 16px;
  text-align: left;
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-text-muted);
  border-bottom: 1px solid var(--color-border);
}

/* Rows */
.data-table td {
  height: 52px;
  padding: 12px 16px;
  font-size: 15px;
  font-weight: 400;
  border-bottom: 1px solid var(--color-border);
}

/* Hover */
.data-table tr:hover td {
  background: rgba(0, 0, 0, 0.02); /* light */
}

/* Pagination */
.table-pagination {
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  color: var(--color-text-secondary);
}
```

---

## Modal Layout

```
+----------------------------------------+
|  Modal Title                      [×]  |
+----------------------------------------+
|                                        |
|  Content area with form or message     |
|                                        |
|  +----------------------------------+  |
|  | Input field                      |  |
|  +----------------------------------+  |
|                                        |
|  +----------------------------------+  |
|  | Input field                      |  |
|  +----------------------------------+  |
|                                        |
+----------------------------------------+
|                    [Cancel]  [Confirm] |
+----------------------------------------+
```

### Specifications

```css
/* Backdrop */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5); /* light */
  /* background: rgba(0, 0, 0, 0.7); dark */
  z-index: 300;
}

/* Modal */
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: var(--color-surface-elevated);
  border-radius: 8px;
  z-index: 400;
  max-height: 90vh;
  overflow: auto;
}

/* Sizes */
.modal-sm { width: 480px; }
.modal-md { width: 640px; }
.modal-lg { width: 800px; }

/* Header */
.modal-header {
  padding: 24px 24px 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title {
  font-size: 20px;
  font-weight: 500;
}

/* Body */
.modal-body {
  padding: 24px;
}

/* Footer */
.modal-footer {
  padding: 0 24px 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
```

---

## Card Detail Layout

```
+------------------------------------------------------------------+
|  HEADER                                                          |
|  [← Back]  Title                              [Edit] [Delete]    |
+------------------------------------------------------------------+
|                                                                  |
|  +----------------------+  +-----------------------------------+ |
|  |                      |  |                                   | |
|  |  IMAGE / PREVIEW     |  |  DETAILS                          | |
|  |  (aspect ratio)      |  |                                   | |
|  |                      |  |  Label: Value                     | |
|  +----------------------+  |  Label: Value                     | |
|                            |  Label: Value                     | |
|                            |                                   | |
|                            +-----------------------------------+ |
|                                                                  |
|  +-------------------------------------------------------------+ |
|  |  DESCRIPTION / CONTENT                                      | |
|  |                                                             | |
|  +-------------------------------------------------------------+ |
+------------------------------------------------------------------+
```

### Specifications

```css
/* Header */
.detail-header {
  padding: 24px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--color-border);
}

.detail-header-title {
  display: flex;
  align-items: center;
  gap: 16px;
}

.detail-header-actions {
  display: flex;
  gap: 12px;
}

/* Content */
.detail-content {
  padding: 32px;
}

/* Two-column layout */
.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  margin-bottom: 32px;
}

/* Details list */
.detail-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-text-muted);
}

.detail-value {
  font-size: 15px;
  font-weight: 400;
}
```

---

## Empty State Layout

```
+------------------------------------------------------------------+
|                                                                  |
|                                                                  |
|                      [64px icon]                                 |
|                                                                  |
|                   No items found                                 |
|                                                                  |
|            Get started by creating your first item               |
|                                                                  |
|                    [Create Item]                                 |
|                                                                  |
|                                                                  |
+------------------------------------------------------------------+
```

### Specifications

```css
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 32px;
  text-align: center;
}

.empty-state-icon {
  width: 64px;
  height: 64px;
  color: var(--color-text-muted);
  margin-bottom: 24px;
}

.empty-state-title {
  font-size: 20px;
  font-weight: 500;
  margin-bottom: 8px;
}

.empty-state-desc {
  font-size: 15px;
  color: var(--color-text-secondary);
  margin-bottom: 24px;
  max-width: 400px;
}
```

---

## Breakpoint System

| Breakpoint | Width | Columns | Margin | Gutter |
|------------|-------|---------|--------|--------|
| Mobile | 0-639px | 4 | 16px | 16px |
| Tablet | 640-1023px | 8 | 24px | 24px |
| Desktop | 1024-1279px | 12 | 32px | 24px |
| Wide | 1280px+ | 12 | auto (centered) | 24px |

### CSS

```css
/* Mobile first */
.container {
  width: 100%;
  padding: 0 16px;
}

/* Tablet */
@media (min-width: 640px) {
  .container {
    padding: 0 24px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    padding: 0 32px;
  }
}

/* Wide */
@media (min-width: 1280px) {
  .container {
    max-width: 1280px;
    margin: 0 auto;
  }
}
```

---

## Content Density

### Compact (Data-heavy interfaces)

```css
.density-compact {
  /* Table rows */
  --row-height: 40px;
  --cell-padding: 8px 12px;

  /* Cards */
  --card-padding: 12px;

  /* Buttons */
  --btn-height: 32px;
  --btn-padding: 6px 12px;
}
```

### Default (Most interfaces)

```css
.density-default {
  /* Table rows */
  --row-height: 52px;
  --cell-padding: 12px 16px;

  /* Cards */
  --card-padding: 16px;

  /* Buttons */
  --btn-height: 44px;
  --btn-padding: 10px 20px;
}
```

### Spacious (Marketing, hero sections)

```css
.density-spacious {
  /* Cards */
  --card-padding: 24px;

  /* Buttons */
  --btn-height: 52px;
  --btn-padding: 14px 28px;

  /* Sections */
  --section-gap: 64px;
}
```

---

## Responsive Behavior

### Sidebar

```
Desktop (1024+): Visible, fixed 240px
Tablet (640-1023): Collapsible overlay
Mobile (<640): Hidden, hamburger menu
```

### Card Grid

```
Desktop (1024+): 3-4 columns
Tablet (640-1023): 2 columns
Mobile (<640): 1 column
```

### Data Table

```
Desktop: Full table
Tablet: Hide secondary columns
Mobile: Stack as cards OR horizontal scroll
```

### Modal

```
Desktop: Centered, sized (480/640/800px)
Mobile: Full screen with safe areas
```
