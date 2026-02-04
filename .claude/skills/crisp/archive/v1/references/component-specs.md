# Component Specifications

Complete CSS specifications for Crisp Design Language components.

**IMPORTANT: All components use CrispByYosi font exclusively.**

---

## Buttons

### Primary Button

```css
.btn-primary {
  /* Layout */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;
  padding: 10px 20px;

  /* Typography */
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 500;
  line-height: 1.4;

  /* Colors - Light */
  background-color: #1C1C1A;
  color: #FFFFFF;
  border: none;

  /* Shape */
  border-radius: 6px;

  /* Interaction */
  cursor: pointer;
  transition: background-color 150ms ease;
}

.btn-primary:hover {
  background-color: #333330;
}

.btn-primary:active {
  background-color: #1C1C1A;
}

.btn-primary:disabled {
  background-color: #E2E1DE;
  color: #8A8A86;
  cursor: not-allowed;
}

.btn-primary:focus-visible {
  outline: 2px solid #f59e0b;
  outline-offset: 2px;
}

/* Dark mode */
[data-theme="dark"] .btn-primary {
  background-color: rgba(250, 250, 248, 0.87);
  color: #0a0a0b;
}

[data-theme="dark"] .btn-primary:hover {
  background-color: rgba(250, 250, 248, 0.75);
}

[data-theme="dark"] .btn-primary:disabled {
  background-color: #3A3A3E;
  color: rgba(250, 250, 248, 0.38);
}
```

### Secondary Button

```css
.btn-secondary {
  /* Layout */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;
  padding: 9px 19px; /* -1px for border */

  /* Typography */
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 500;
  line-height: 1.4;

  /* Colors - Light */
  background-color: transparent;
  color: #1C1C1A;
  border: 1px solid #C0BFBC;

  /* Shape */
  border-radius: 6px;

  /* Interaction */
  cursor: pointer;
  transition: border-color 150ms ease;
}

.btn-secondary:hover {
  border-color: #8A8A86;
}

.btn-secondary:disabled {
  border-color: #EEEEED;
  color: #C0BFBC;
  cursor: not-allowed;
}

.btn-secondary:focus-visible {
  outline: 2px solid #f59e0b;
  outline-offset: 2px;
}

/* Dark mode */
[data-theme="dark"] .btn-secondary {
  border-color: #3A3A3E;
  color: rgba(250, 250, 248, 0.87);
}

[data-theme="dark"] .btn-secondary:hover {
  border-color: #5A5A5E;
}
```

### Ghost Button

```css
.btn-ghost {
  /* Layout */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;
  padding: 10px 20px;

  /* Typography */
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 500;

  /* Colors */
  background-color: transparent;
  color: #5C5C58;
  border: none;

  /* Interaction */
  cursor: pointer;
  transition: color 150ms ease;
}

.btn-ghost:hover {
  color: #1C1C1A;
}

.btn-ghost:focus-visible {
  outline: 2px solid #f59e0b;
  outline-offset: 2px;
}

/* Dark mode */
[data-theme="dark"] .btn-ghost {
  color: rgba(250, 250, 248, 0.60);
}

[data-theme="dark"] .btn-ghost:hover {
  color: rgba(250, 250, 248, 0.87);
}
```

### Accent Button

```css
.btn-accent {
  /* Layout */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;
  padding: 10px 20px;

  /* Typography */
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 500;
  line-height: 1.4;

  /* Colors */
  background-color: #f59e0b;
  color: #1C1C1A;
  border: none;

  /* Shape */
  border-radius: 6px;

  /* Interaction */
  cursor: pointer;
  transition: background-color 150ms ease;
}

.btn-accent:hover {
  background-color: #d97706;
}

.btn-accent:focus-visible {
  outline: 2px solid #1C1C1A;
  outline-offset: 2px;
}

/* Dark mode */
[data-theme="dark"] .btn-accent {
  background-color: #fbbf24;
}

[data-theme="dark"] .btn-accent:hover {
  background-color: #f59e0b;
}
```

### Destructive Button

Use `btn-secondary` with error text color for destructive actions.

```css
.btn-destructive {
  /* Same as btn-secondary */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;
  padding: 9px 19px;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 500;

  /* Destructive styling */
  background-color: transparent;
  color: #ef4444;
  border: 1px solid #ef4444;
  border-radius: 6px;

  cursor: pointer;
  transition: all 150ms ease;
}

.btn-destructive:hover {
  background-color: #fee2e2;
}

.btn-destructive:focus-visible {
  outline: 2px solid #ef4444;
  outline-offset: 2px;
}

/* Dark mode */
[data-theme="dark"] .btn-destructive {
  color: #f87171;
  border-color: #f87171;
}

[data-theme="dark"] .btn-destructive:hover {
  background-color: rgba(239, 68, 68, 0.15);
}
```

### Button Sizes

```css
.btn-sm {
  min-height: 32px;
  padding: 6px 12px;
  font-size: 13px;
}

.btn-md {
  min-height: 44px;
  padding: 10px 20px;
  font-size: 15px;
}

.btn-lg {
  min-height: 52px;
  padding: 14px 28px;
  font-size: 17px;
}
```

---

## Inputs

### Text Input

```css
.input {
  /* Layout */
  width: 100%;
  min-height: 44px;
  padding: 10px 12px;

  /* Typography */
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 400;
  line-height: 1.4;

  /* Colors - Light */
  background-color: #FFFFFF;
  color: #1C1C1A;
  border: 1px solid #C0BFBC;

  /* Shape */
  border-radius: 6px;

  /* Interaction */
  transition: border-color 150ms ease;
}

.input::placeholder {
  color: #C0BFBC;
}

.input:hover {
  border-color: #8A8A86;
}

.input:focus {
  outline: none;
  border-color: #f59e0b;
}

.input:disabled {
  background-color: #F4F4F2;
  color: #8A8A86;
  cursor: not-allowed;
}

.input.input-error {
  border-color: #ef4444;
}

/* Dark mode */
[data-theme="dark"] .input {
  background-color: #111113;
  color: rgba(250, 250, 248, 0.87);
  border-color: #3A3A3E;
}

[data-theme="dark"] .input::placeholder {
  color: rgba(250, 250, 248, 0.38);
}

[data-theme="dark"] .input:hover {
  border-color: #5A5A5E;
}

[data-theme="dark"] .input:focus {
  border-color: #fbbf24;
}

[data-theme="dark"] .input:disabled {
  background-color: #1A1A1C;
  color: rgba(250, 250, 248, 0.38);
}
```

### Input Label

```css
.input-label {
  display: block;
  margin-bottom: 8px;

  /* Typography */
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 11px;
  font-weight: 500;
  line-height: 1.3;
  letter-spacing: 0.1em;
  text-transform: uppercase;

  /* Colors */
  color: #5C5C58;
}

[data-theme="dark"] .input-label {
  color: rgba(250, 250, 248, 0.60);
}
```

### Helper Text

```css
.input-helper {
  margin-top: 4px;
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 13px;
  font-weight: 300;
  color: #8A8A86;
}

.input-helper.input-helper-error {
  color: #ef4444;
}

[data-theme="dark"] .input-helper {
  color: rgba(250, 250, 248, 0.38);
}
```

### Select

```css
.select {
  /* Same as input */
  width: 100%;
  min-height: 44px;
  padding: 10px 12px;
  padding-right: 40px; /* Space for arrow */

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 400;

  background-color: #FFFFFF;
  color: #1C1C1A;
  border: 1px solid #C0BFBC;
  border-radius: 6px;

  /* Custom arrow */
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%235C5C58' stroke-width='2'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;

  cursor: pointer;
  transition: border-color 150ms ease;
}

.select:hover {
  border-color: #8A8A86;
}

.select:focus {
  outline: none;
  border-color: #f59e0b;
}
```

### Checkbox

```css
.checkbox {
  width: 20px;
  height: 20px;
  margin: 0;

  appearance: none;
  background-color: #FFFFFF;
  border: 1px solid #C0BFBC;
  border-radius: 4px;

  cursor: pointer;
  transition: all 150ms ease;
}

.checkbox:checked {
  background-color: #1C1C1A;
  border-color: #1C1C1A;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3'%3E%3Cpath d='M20 6 9 17l-5-5'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
}

.checkbox:focus-visible {
  outline: 2px solid #f59e0b;
  outline-offset: 2px;
}

/* Dark mode */
[data-theme="dark"] .checkbox {
  background-color: #111113;
  border-color: #3A3A3E;
}

[data-theme="dark"] .checkbox:checked {
  background-color: rgba(250, 250, 248, 0.87);
  border-color: rgba(250, 250, 248, 0.87);
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%230a0a0b' stroke-width='3'%3E%3Cpath d='M20 6 9 17l-5-5'/%3E%3C/svg%3E");
}
```

### Radio Button

```css
.radio {
  width: 20px;
  height: 20px;
  margin: 0;

  appearance: none;
  background-color: #FFFFFF;
  border: 1px solid #C0BFBC;
  border-radius: 50%;

  cursor: pointer;
  transition: all 150ms ease;
}

.radio:hover {
  border-color: #8A8A86;
}

.radio:checked {
  background-color: #1C1C1A;
  border-color: #1C1C1A;
}

/* Inner dot for checked state */
.radio:checked::after {
  content: '';
  display: block;
  width: 8px;
  height: 8px;
  margin: 5px;
  background-color: #FFFFFF;
  border-radius: 50%;
}

.radio:focus-visible {
  outline: 2px solid #f59e0b;
  outline-offset: 2px;
}

.radio:disabled {
  background-color: #F4F4F2;
  border-color: #E2E1DE;
  cursor: not-allowed;
}

/* Dark mode */
[data-theme="dark"] .radio {
  background-color: #111113;
  border-color: #3A3A3E;
}

[data-theme="dark"] .radio:hover {
  border-color: #5A5A5E;
}

[data-theme="dark"] .radio:checked {
  background-color: rgba(250, 250, 248, 0.87);
  border-color: rgba(250, 250, 248, 0.87);
}

[data-theme="dark"] .radio:checked::after {
  background-color: #0a0a0b;
}
```

### Toggle Switch

```css
.toggle {
  position: relative;
  width: 44px;
  height: 24px;

  appearance: none;
  background-color: #E2E1DE;
  border: none;
  border-radius: 9999px; /* Exception: toggles use pill shape */

  cursor: pointer;
  transition: background-color 150ms ease;
}

.toggle::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;

  background-color: #FFFFFF;
  border-radius: 50%;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);

  transition: transform 150ms ease;
}

.toggle:checked {
  background-color: #1C1C1A;
}

.toggle:checked::after {
  transform: translateX(20px);
}

.toggle:focus-visible {
  outline: 2px solid #f59e0b;
  outline-offset: 2px;
}

/* Dark mode */
[data-theme="dark"] .toggle {
  background-color: #3A3A3E;
}

[data-theme="dark"] .toggle:checked {
  background-color: rgba(250, 250, 248, 0.87);
}

[data-theme="dark"] .toggle::after {
  background-color: #0a0a0b;
}
```

---

## Cards

### Base Card

```css
.card {
  /* Layout */
  display: flex;
  flex-direction: column;

  /* Colors - Light */
  background-color: #FFFFFF;
  border: 1px solid #E2E1DE;

  /* Shape */
  border-radius: 8px;
  overflow: hidden;

  /* Interaction */
  transition: border-color 150ms ease;
}

.card:hover {
  border-color: #C0BFBC;
}

.card.card-selected {
  border-color: #1C1C1A;
}

/* Dark mode */
[data-theme="dark"] .card {
  background-color: #1A1A1C;
  border-color: #1f1f23;
}

[data-theme="dark"] .card:hover {
  border-color: #2D2D30;
}

[data-theme="dark"] .card.card-selected {
  border-color: rgba(250, 250, 248, 0.87);
}
```

### Card Sizes

```css
.card-sm { padding: 12px; }
.card-md { padding: 16px; }
.card-lg { padding: 24px; }
```

### Card with Image

```css
.card-image {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  background-color: #F4F4F2;
}

.card-content {
  padding: 16px;
}

.card-title {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 17px;
  font-weight: 500;
  color: #1C1C1A;
  margin-bottom: 4px;
}

.card-description {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 400;
  color: #5C5C58;
}

.card-meta {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 13px;
  font-weight: 300;
  color: #8A8A86;
}

[data-theme="dark"] .card-image {
  background-color: #252527;
}

[data-theme="dark"] .card-title {
  color: rgba(250, 250, 248, 0.87);
}

[data-theme="dark"] .card-description {
  color: rgba(250, 250, 248, 0.60);
}

[data-theme="dark"] .card-meta {
  color: rgba(250, 250, 248, 0.38);
}
```

---

## Navigation

### Sidebar

```css
.sidebar {
  width: 240px;
  padding: 24px 16px;
  background-color: #FAFAF8;
  border-right: 1px solid #E2E1DE;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.sidebar-brand {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 17px;
  font-weight: 500;
  color: #1C1C1A;
  margin-bottom: 8px;
}

.sidebar-version {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 11px;
  font-weight: 300;
  color: #8A8A86;
  margin-bottom: 24px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.sidebar-nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 500;
  text-decoration: none;
  color: #5C5C58;

  border-radius: 6px;
  transition: background-color 150ms ease, color 150ms ease;
}

.sidebar-nav-item:hover {
  background-color: rgba(0, 0, 0, 0.03);
  color: #1C1C1A;
}

.sidebar-nav-item.is-active {
  background-color: rgba(0, 0, 0, 0.05);
  color: #1C1C1A;
}

/* Dark mode */
[data-theme="dark"] .sidebar {
  background-color: #0a0a0b;
  border-color: #1f1f23;
}

[data-theme="dark"] .sidebar-brand {
  color: rgba(250, 250, 248, 0.87);
}

[data-theme="dark"] .sidebar-nav-item {
  color: rgba(250, 250, 248, 0.60);
}

[data-theme="dark"] .sidebar-nav-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
  color: rgba(250, 250, 248, 0.87);
}

[data-theme="dark"] .sidebar-nav-item.is-active {
  background-color: rgba(255, 255, 255, 0.08);
  color: rgba(250, 250, 248, 0.87);
}
```

### Header

```css
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 24px;
  background-color: #FFFFFF;
  border-bottom: 1px solid #E2E1DE;
}

.header-title {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 17px;
  font-weight: 500;
  color: #1C1C1A;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* Dark mode */
[data-theme="dark"] .header {
  background-color: #111113;
  border-color: #1f1f23;
}

[data-theme="dark"] .header-title {
  color: rgba(250, 250, 248, 0.87);
}
```

### Tabs

```css
.tabs {
  display: flex;
  gap: 0;
  border-bottom: 1px solid #E2E1DE;
}

.tab {
  padding: 12px 16px;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 500;
  color: #5C5C58;
  text-decoration: none;

  border: none;
  background: transparent;
  cursor: pointer;
  transition: color 150ms ease;

  position: relative;
}

.tab:hover {
  color: #1C1C1A;
}

.tab.is-active {
  color: #1C1C1A;
}

.tab.is-active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #1C1C1A;
}

/* Dark mode */
[data-theme="dark"] .tabs {
  border-color: #1f1f23;
}

[data-theme="dark"] .tab {
  color: rgba(250, 250, 248, 0.60);
}

[data-theme="dark"] .tab:hover,
[data-theme="dark"] .tab.is-active {
  color: rgba(250, 250, 248, 0.87);
}

[data-theme="dark"] .tab.is-active::after {
  background-color: rgba(250, 250, 248, 0.87);
}
```

---

## Badges

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;

  background-color: #F4F4F2;
  color: #5C5C58;
  border-radius: 4px;
}

.badge-success {
  background-color: #dcfce7;
  color: #166534;
}

.badge-warning {
  background-color: #fef3c7;
  color: #92400e;
}

.badge-error {
  background-color: #fee2e2;
  color: #991b1b;
}

.badge-info {
  background-color: #dbeafe;
  color: #1e40af;
}

/* Dark mode */
[data-theme="dark"] .badge {
  background-color: #252527;
  color: rgba(250, 250, 248, 0.60);
}

[data-theme="dark"] .badge-success {
  background-color: rgba(34, 197, 94, 0.15);
  color: #4ade80;
}

[data-theme="dark"] .badge-warning {
  background-color: rgba(234, 179, 8, 0.15);
  color: #facc15;
}

[data-theme="dark"] .badge-error {
  background-color: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

[data-theme="dark"] .badge-info {
  background-color: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
}
```

---

## Status Indicators (Dots)

Status indicators are small colored dots that communicate state.
**This is the ONLY place functional colors may be used as solid fills.**

```css
.status-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* Default (neutral) */
.status-indicator {
  background-color: #8A8A86;
}

/* Status variants - same in light and dark mode */
.status-indicator-success {
  background-color: #22c55e;
}

.status-indicator-warning {
  background-color: #eab308;
}

.status-indicator-error {
  background-color: #ef4444;
}

.status-indicator-info {
  background-color: #3b82f6;
}

/* Size variants */
.status-indicator-sm {
  width: 6px;
  height: 6px;
}

.status-indicator-lg {
  width: 10px;
  height: 10px;
}
```

### Usage with Text

```css
.status-with-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.status-with-label .status-indicator {
  /* Indicator styles above */
}

.status-with-label .status-label {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 13px;
  font-weight: 400;
  color: var(--color-text); /* NOT colored - only the dot is colored */
}
```

**Rule:** The dot is colored. The label text is NOT colored. Numbers and values are NEVER colored.

---

## Tables

```css
.table {
  width: 100%;
  border-collapse: collapse;
}

.table th {
  padding: 12px 16px;
  text-align: left;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #5C5C58;

  background-color: #F4F4F2;
  border-bottom: 1px solid #E2E1DE;
}

.table td {
  padding: 12px 16px;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 400;
  color: #1C1C1A;

  border-bottom: 1px solid #E2E1DE;
}

.table tr:hover td {
  background-color: rgba(0, 0, 0, 0.02);
}

/* Dark mode */
[data-theme="dark"] .table th {
  background-color: #1A1A1C;
  color: rgba(250, 250, 248, 0.60);
  border-color: #1f1f23;
}

[data-theme="dark"] .table td {
  color: rgba(250, 250, 248, 0.87);
  border-color: #1f1f23;
}

[data-theme="dark"] .table tr:hover td {
  background-color: rgba(255, 255, 255, 0.03);
}
```

---

## Modals

```css
.modal-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 300;
}

.modal {
  background-color: #FFFFFF;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  z-index: 400;
}

.modal-sm { width: 480px; }
.modal-md { width: 640px; }
.modal-lg { width: 800px; }

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  border-bottom: 1px solid #E2E1DE;
}

.modal-title {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 17px;
  font-weight: 500;
  color: #1C1C1A;
}

.modal-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;

  background: transparent;
  border: none;
  border-radius: 4px;
  color: #5C5C58;
  cursor: pointer;
  transition: background-color 150ms ease;
}

.modal-close:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #E2E1DE;
}

/* Dark mode */
[data-theme="dark"] .modal-backdrop {
  background-color: rgba(0, 0, 0, 0.7);
}

[data-theme="dark"] .modal {
  background-color: #1A1A1C;
  box-shadow: none;
}

[data-theme="dark"] .modal-header,
[data-theme="dark"] .modal-footer {
  border-color: #1f1f23;
}

[data-theme="dark"] .modal-title {
  color: rgba(250, 250, 248, 0.87);
}

[data-theme="dark"] .modal-close {
  color: rgba(250, 250, 248, 0.60);
}

[data-theme="dark"] .modal-close:hover {
  background-color: rgba(255, 255, 255, 0.05);
}
```

---

## Empty States

```css
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 48px 24px;
}

.empty-state-icon {
  width: 48px;
  height: 48px;
  color: #C0BFBC;
  margin-bottom: 16px;
}

.empty-state-title {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 17px;
  font-weight: 500;
  color: #1C1C1A;
  margin-bottom: 8px;
}

.empty-state-description {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 400;
  color: #5C5C58;
  max-width: 320px;
  margin-bottom: 24px;
}

/* No illustrations. No decorative elements. */

/* Dark mode */
[data-theme="dark"] .empty-state-icon {
  color: #3A3A3E;
}

[data-theme="dark"] .empty-state-title {
  color: rgba(250, 250, 248, 0.87);
}

[data-theme="dark"] .empty-state-description {
  color: rgba(250, 250, 248, 0.60);
}
```

---

## Loading States

```css
/* Static placeholder - NO animations */
.loading-placeholder {
  background-color: #F4F4F2;
  border-radius: 4px;
}

.loading-text {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 13px;
  font-weight: 300;
  color: #8A8A86;
}

/* Progress bar - static, no animation */
.progress-bar {
  height: 4px;
  background-color: #E2E1DE;
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background-color: #1C1C1A;
  /* NO transition - instant updates only */
}

/* Dark mode */
[data-theme="dark"] .loading-placeholder {
  background-color: #252527;
}

[data-theme="dark"] .loading-text {
  color: rgba(250, 250, 248, 0.38);
}

[data-theme="dark"] .progress-bar {
  background-color: #2D2D30;
}

[data-theme="dark"] .progress-bar-fill {
  background-color: rgba(250, 250, 248, 0.87);
}
```

---

## Icons

```css
.icon {
  display: inline-block;
  width: 20px;
  height: 20px;
  stroke: currentColor;
  stroke-width: 2;
  fill: none;
  flex-shrink: 0;
}

.icon-sm {
  width: 16px;
  height: 16px;
  stroke-width: 1.5;
}

.icon-lg {
  width: 24px;
  height: 24px;
}

.icon-xl {
  width: 32px;
  height: 32px;
  stroke-width: 2.5;
}
```

---

## Tooltips

```css
.tooltip {
  position: absolute;
  padding: 6px 10px;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 13px;
  font-weight: 400;
  color: #FFFFFF;

  background-color: #1C1C1A;
  border-radius: 4px;
  z-index: 600;

  /* No animations */
}

/* Dark mode */
[data-theme="dark"] .tooltip {
  background-color: #3A3A3E;
  color: rgba(250, 250, 248, 0.87);
}
```

---

## Toasts

```css
.toast {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;

  background-color: #1C1C1A;
  color: #FFFFFF;
  border-radius: 6px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 400;

  z-index: 700;
}

.toast-success {
  background-color: #166534;
}

.toast-error {
  background-color: #991b1b;
}

/* Dark mode */
[data-theme="dark"] .toast {
  background-color: #3A3A3E;
  color: rgba(250, 250, 248, 0.87);
  box-shadow: none;
}
```

---

## Avatars

```css
.avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background-color: #F4F4F2;
  border-radius: 50%; /* Full circle - exception to 8px max */
  flex-shrink: 0;
}

/* Sizes */
.avatar-sm {
  width: 32px;
  height: 32px;
  font-size: 13px;
}

.avatar-md {
  width: 40px;
  height: 40px;
  font-size: 15px;
}

.avatar-lg {
  width: 48px;
  height: 48px;
  font-size: 17px;
}

.avatar-xl {
  width: 64px;
  height: 64px;
  font-size: 20px;
}

/* Image avatar */
.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Initials avatar */
.avatar-initials {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-weight: 500;
  color: #5C5C58;
  text-transform: uppercase;
}

/* Dark mode */
[data-theme="dark"] .avatar {
  background-color: #252527;
}

[data-theme="dark"] .avatar-initials {
  color: rgba(250, 250, 248, 0.60);
}
```

---

## Dropdown Menu

```css
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 180px;
  margin-top: 4px;
  padding: 4px 0;

  background-color: #FFFFFF;
  border: 1px solid #E2E1DE;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);

  z-index: 100;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 10px 16px;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 400;
  color: #1C1C1A;
  text-align: left;
  text-decoration: none;

  background: transparent;
  border: none;
  cursor: pointer;
  transition: background-color 100ms ease;
}

.dropdown-item:hover {
  background-color: rgba(0, 0, 0, 0.03);
}

.dropdown-item:focus-visible {
  background-color: rgba(0, 0, 0, 0.05);
  outline: none;
}

.dropdown-item-destructive {
  color: #ef4444;
}

.dropdown-separator {
  height: 1px;
  margin: 4px 0;
  background-color: #E2E1DE;
}

/* Dark mode */
[data-theme="dark"] .dropdown-menu {
  background-color: #252527;
  border-color: #3A3A3E;
  box-shadow: none;
}

[data-theme="dark"] .dropdown-item {
  color: rgba(250, 250, 248, 0.87);
}

[data-theme="dark"] .dropdown-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

[data-theme="dark"] .dropdown-item-destructive {
  color: #f87171;
}

[data-theme="dark"] .dropdown-separator {
  background-color: #3A3A3E;
}
```

---

## Dividers

```css
/* Horizontal divider */
.divider {
  width: 100%;
  height: 1px;
  background-color: #E2E1DE;
  border: none;
  margin: 16px 0;
}

/* Vertical divider */
.divider-vertical {
  width: 1px;
  height: 100%;
  background-color: #E2E1DE;
  margin: 0 16px;
}

/* With text label */
.divider-with-text {
  display: flex;
  align-items: center;
  gap: 16px;
}

.divider-with-text::before,
.divider-with-text::after {
  content: '';
  flex: 1;
  height: 1px;
  background-color: #E2E1DE;
}

.divider-text {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #8A8A86;
}

/* Dark mode */
[data-theme="dark"] .divider,
[data-theme="dark"] .divider-vertical,
[data-theme="dark"] .divider-with-text::before,
[data-theme="dark"] .divider-with-text::after {
  background-color: #1f1f23;
}

[data-theme="dark"] .divider-text {
  color: rgba(250, 250, 248, 0.38);
}
```
