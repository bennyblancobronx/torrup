# Navigation

## Sidebar

```css
.sidebar {
  width: 240px;
  padding: 24px 16px;
  background-color: #fff8f2;
  border-right: 1px solid rgba(212,191,155,0.40);
  display: flex;
  flex-direction: column;
  height: 100%;
}

.sidebar-brand {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 17px;
  font-weight: 500;
  color: #1F1F1F;
  margin-bottom: 8px;
}

.sidebar-version {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 11px;
  font-weight: 300;
  color: #7A7A7A;
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
  color: #454545;

  border-radius: 6px;
  transition: background-color 150ms ease, color 150ms ease;
}

.sidebar-nav-item:hover {
  background-color: rgba(0,0,0,0.03);
  color: #1F1F1F;
}

.sidebar-nav-item.is-active {
  background-color: rgba(0,0,0,0.05);
  color: #1F1F1F;
}

[data-theme="dark"] .sidebar { background-color: #1F1F1F; border-color: #353535; }
[data-theme="dark"] .sidebar-brand { color: rgba(255,251,247,0.87); }
[data-theme="dark"] .sidebar-nav-item { color: rgba(255,251,247,0.60); }
[data-theme="dark"] .sidebar-nav-item:hover {
  background-color: rgba(255,255,255,0.05);
  color: rgba(255,251,247,0.87);
}
[data-theme="dark"] .sidebar-nav-item.is-active {
  background-color: rgba(255,255,255,0.08);
  color: rgba(255,251,247,0.87);
}
```

---

## Header

```css
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 24px;
  background-color: #FFFBF7;
  border-bottom: 1px solid rgba(212,191,155,0.40);
}

.header-title {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 17px;
  font-weight: 500;
  color: #1F1F1F;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

[data-theme="dark"] .header { background-color: #2A2A2A; border-color: #353535; }
[data-theme="dark"] .header-title { color: rgba(255,251,247,0.87); }
```

---

## Tabs

```css
.tabs {
  display: flex;
  gap: 0;
  border-bottom: 1px solid rgba(212,191,155,0.40);
}

.tab {
  padding: 12px 16px;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 500;
  color: #454545;
  text-decoration: none;

  border: none;
  background: transparent;
  cursor: pointer;
  transition: color 150ms ease;

  position: relative;
}

.tab:hover { color: #1F1F1F; }

.tab.is-active { color: #1F1F1F; }

.tab.is-active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #1F1F1F;
}

[data-theme="dark"] .tabs { border-color: #353535; }
[data-theme="dark"] .tab { color: rgba(255,251,247,0.60); }
[data-theme="dark"] .tab:hover,
[data-theme="dark"] .tab.is-active { color: rgba(255,251,247,0.87); }
[data-theme="dark"] .tab.is-active::after { background-color: rgba(255,251,247,0.87); }
```

---

## Dropdown Menu

```css
.dropdown { position: relative; display: inline-block; }

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 180px;
  margin-top: 4px;
  padding: 4px 0;

  background-color: #FFFBF7;
  border: 1px solid rgba(212,191,155,0.40);
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.08);

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
  color: #1F1F1F;
  text-align: left;
  text-decoration: none;

  background: transparent;
  border: none;
  cursor: pointer;
  transition: background-color 100ms ease;
}

.dropdown-item:hover { background-color: rgba(0,0,0,0.03); }
.dropdown-item:focus-visible { background-color: rgba(0,0,0,0.05); outline: none; }
.dropdown-item-destructive { color: #AE1C09; }

.dropdown-separator {
  height: 1px;
  margin: 4px 0;
  background-color: rgba(212,191,155,0.40);
}

[data-theme="dark"] .dropdown-menu {
  background-color: #404040;
  border-color: #4A4A4A;
  box-shadow: none;
}
[data-theme="dark"] .dropdown-item { color: rgba(255,251,247,0.87); }
[data-theme="dark"] .dropdown-item:hover { background-color: rgba(255,255,255,0.05); }
[data-theme="dark"] .dropdown-item-destructive { color: #F5533D; }
[data-theme="dark"] .dropdown-separator { background-color: #4A4A4A; }
```

---

## Navigation States

| State | Background | Text | Border |
|-------|------------|------|--------|
| default | transparent | #454545 | none |
| hover | rgba(0,0,0,0.03) | #1F1F1F | none |
| active | rgba(0,0,0,0.05) | #1F1F1F | left: 2px solid #1F1F1F |
| disabled | transparent | rgba(122,122,122,0.50) | none |

### Dark Mode

| State | Background | Text |
|-------|------------|------|
| default | transparent | rgba(255,251,247,0.60) |
| hover | rgba(255,255,255,0.05) | rgba(255,251,247,0.87) |
| active | rgba(255,255,255,0.08) | rgba(255,251,247,0.87) |
