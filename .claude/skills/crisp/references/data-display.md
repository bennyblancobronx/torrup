# Data Display

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
  color: #454545;

  background-color: #FFFBF7;
  border-bottom: 1px solid rgba(212,191,155,0.40);
}

.table td {
  padding: 12px 16px;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 400;
  color: #1F1F1F;

  border-bottom: 1px solid rgba(212,191,155,0.40);
}

.table tr:hover td { background-color: rgba(0,0,0,0.02); }

[data-theme="dark"] .table th {
  background-color: #353535;
  color: rgba(255,251,247,0.60);
  border-color: #353535;
}

[data-theme="dark"] .table td {
  color: rgba(255,251,247,0.87);
  border-color: #353535;
}

[data-theme="dark"] .table tr:hover td { background-color: rgba(255,255,255,0.03); }
```

### Table Dimensions

- Header height: 48px
- Row height: 52px
- Cell padding: 12px 16px
- Header font: 11px / 500 / uppercase / 0.1em
- Cell font: 15px / 400

### Table Row States

| State | Light Background | Dark Background |
|-------|------------------|-----------------|
| default | transparent | transparent |
| hover | rgba(0,0,0,0.02) | rgba(255,255,255,0.03) |
| selected | rgba(0,0,0,0.04) | rgba(255,255,255,0.05) |
| active | rgba(0,0,0,0.05) | rgba(255,255,255,0.08) |

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

  background-color: #FFFBF7;
  color: #454545;
  border-radius: 4px;
}

.badge-success { background-color: rgba(40,103,54,0.10); color: #173B1F; }
.badge-warning { background-color: rgba(168,134,43,0.10); color: #6B5518; }
.badge-error { background-color: rgba(174,28,9,0.10); color: #741306; }
.badge-info { background-color: rgba(73,105,110,0.10); color: #314649; }
.badge-accent { background-color: rgba(185,151,92,0.10); color: #725A31; }

[data-theme="dark"] .badge { background-color: #404040; color: rgba(255,251,247,0.60); }
[data-theme="dark"] .badge-success { background-color: rgba(57,147,77,0.15); color: #39934D; }
[data-theme="dark"] .badge-warning { background-color: rgba(212,173,74,0.15); color: #D4AD4A; }
[data-theme="dark"] .badge-error { background-color: rgba(245,83,61,0.15); color: #F5533D; }
[data-theme="dark"] .badge-info { background-color: rgba(145,177,182,0.15); color: #91B1B6; }
[data-theme="dark"] .badge-accent { background-color: rgba(212,191,155,0.15); color: #D4BF9B; }
```

Badges are static. No interactive states.

---

## Status Indicators (Dots)

The ONLY place functional colors may appear as solid fills.

```css
.status-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
  background-color: #7A7A7A;
}

.status-indicator-success { background-color: #286736; }
.status-indicator-warning { background-color: #A8862B; }
.status-indicator-error { background-color: #AE1C09; }
.status-indicator-info { background-color: #49696E; }

.status-indicator-sm { width: 6px; height: 6px; }
.status-indicator-lg { width: 10px; height: 10px; }
```

### Usage with Text

```css
.status-with-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
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

## Avatars

```css
.avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background-color: #FFFBF7;
  border-radius: 50%;
  flex-shrink: 0;
}

.avatar-sm { width: 32px; height: 32px; font-size: 13px; }
.avatar-md { width: 40px; height: 40px; font-size: 15px; }
.avatar-lg { width: 48px; height: 48px; font-size: 17px; }
.avatar-xl { width: 64px; height: 64px; font-size: 20px; }

.avatar img { width: 100%; height: 100%; object-fit: cover; }

.avatar-initials {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-weight: 500;
  color: #454545;
  text-transform: uppercase;
}

[data-theme="dark"] .avatar { background-color: #404040; }
[data-theme="dark"] .avatar-initials { color: rgba(255,251,247,0.60); }
```

---

## Dividers

```css
.divider {
  width: 100%;
  height: 1px;
  background-color: rgba(212,191,155,0.40);
  border: none;
  margin: 16px 0;
}

.divider-vertical {
  width: 1px;
  height: 100%;
  background-color: rgba(212,191,155,0.40);
  margin: 0 16px;
}

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
  background-color: rgba(212,191,155,0.40);
}

.divider-text {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #7A7A7A;
}

[data-theme="dark"] .divider,
[data-theme="dark"] .divider-vertical,
[data-theme="dark"] .divider-with-text::before,
[data-theme="dark"] .divider-with-text::after { background-color: #353535; }

[data-theme="dark"] .divider-text { color: rgba(255,251,247,0.38); }
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

.icon-sm { width: 16px; height: 16px; stroke-width: 1.5; }
.icon-lg { width: 24px; height: 24px; }
.icon-xl { width: 32px; height: 32px; stroke-width: 2.5; }
```
