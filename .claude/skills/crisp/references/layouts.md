# Layouts

## Dashboard Layout

```
+------------------------------------------------------------------+
|  HEADER (64px)                                      [Avatar] [:]  |
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
| [Nav]    |  |  CONTENT AREA                                    | |
|          |  +--------------------------------------------------+ |
+----------+-------------------------------------------------------+
```

```css
.header {
  height: 64px;
  padding: 0 24px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar {
  width: 240px;
  padding: 24px 16px;
  border-right: 1px solid var(--color-border);
}

.main {
  padding: 32px;
  flex: 1;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}
```

---

## Settings / Form Layout

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
|          |  | Form Field                                       | |
|          |  +--------------------------------------------------+ |
|          |                                                       |
|          |  [Cancel]                    [Save Changes]           |
+----------+-------------------------------------------------------+
```

```css
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
  background: rgba(0,0,0,0.03);
  color: var(--color-text);
  font-weight: 500;
}

.form-container {
  max-width: 640px;
  padding: 32px;
}

.form-section { margin-bottom: 48px; }
.form-section-title { font-size: 24px; font-weight: 700; margin-bottom: 8px; }
.form-section-desc { font-size: 15px; color: var(--color-text-secondary); margin-bottom: 24px; }
.form-field { margin-bottom: 16px; }

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
|  [Search________]  [Filter v]  [Sort v]        [+ Add] [Actions] |
+------------------------------------------------------------------+
|  NAME ^      | STATUS    | DATE       | AMOUNT    | ACTIONS      |
+------------------------------------------------------------------+
|  Item One    | Active    | Jan 15     | $1,234    | [:]          |
|  Item Two    | Pending   | Jan 14     | $567      | [:]          |
+------------------------------------------------------------------+
|  [<] Page 1 of 10 [>]                            Showing 1-10    |
+------------------------------------------------------------------+
```

```css
.table-toolbar {
  padding: 16px 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  border-bottom: 1px solid var(--color-border);
}

.data-table { width: 100%; border-collapse: collapse; }

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

.data-table td {
  height: 52px;
  padding: 12px 16px;
  font-size: 15px;
  font-weight: 400;
  border-bottom: 1px solid var(--color-border);
}

.data-table tr:hover td { background: rgba(0,0,0,0.02); }

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
|  Modal Title                      [x]  |
+----------------------------------------+
|                                        |
|  Content area with form or message     |
|                                        |
+----------------------------------------+
|                    [Cancel]  [Confirm] |
+----------------------------------------+
```

```css
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 300;
}

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

.modal-sm { width: 480px; }
.modal-md { width: 640px; }
.modal-lg { width: 800px; }

.modal-header { padding: 24px 24px 0; display: flex; align-items: center; justify-content: space-between; }
.modal-title { font-size: 20px; font-weight: 500; }
.modal-body { padding: 24px; }
.modal-footer { padding: 0 24px 24px; display: flex; justify-content: flex-end; gap: 12px; }
```

---

## Card Detail Layout

```
+------------------------------------------------------------------+
|  HEADER                                                          |
|  [< Back]  Title                              [Edit] [Delete]    |
+------------------------------------------------------------------+
|                                                                  |
|  +----------------------+  +-----------------------------------+ |
|  |  IMAGE / PREVIEW     |  |  DETAILS                          | |
|  |  (aspect ratio)      |  |  Label: Value                     | |
|  +----------------------+  |  Label: Value                     | |
|                            +-----------------------------------+ |
|                                                                  |
|  +-------------------------------------------------------------+ |
|  |  DESCRIPTION / CONTENT                                      | |
|  +-------------------------------------------------------------+ |
+------------------------------------------------------------------+
```

```css
.detail-header {
  padding: 24px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--color-border);
}

.detail-header-title { display: flex; align-items: center; gap: 16px; }
.detail-header-actions { display: flex; gap: 12px; }

.detail-content { padding: 32px; }

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
  margin-bottom: 32px;
}

.detail-list { display: flex; flex-direction: column; gap: 16px; }
.detail-item { display: flex; flex-direction: column; gap: 4px; }

.detail-label {
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-text-muted);
}

.detail-value { font-size: 15px; font-weight: 400; }
```

---

## Empty State Layout

```
+------------------------------------------------------------------+
|                                                                  |
|                      [64px icon]                                 |
|                                                                  |
|                   No items found                                 |
|                                                                  |
|            Get started by creating your first item               |
|                                                                  |
|                    [Create Item]                                 |
|                                                                  |
+------------------------------------------------------------------+
```

```css
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 32px;
  text-align: center;
}

.empty-state-icon { width: 64px; height: 64px; color: var(--color-text-muted); margin-bottom: 24px; }
.empty-state-title { font-size: 20px; font-weight: 500; margin-bottom: 8px; }
.empty-state-desc { font-size: 15px; color: var(--color-text-secondary); margin-bottom: 24px; max-width: 400px; }
```
