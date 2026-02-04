# Buttons

## Variants

### Primary Button

```css
.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;
  padding: 10px 20px;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 500;
  line-height: 1.4;

  background-color: #454545;
  color: #FFFBF7;
  border: none;
  border-radius: 6px;

  cursor: pointer;
  transition: background-color 150ms ease;
}

.btn-primary:hover { background-color: #1F1F1F; }
.btn-primary:active { background-color: #454545; }
.btn-primary:disabled { background-color: rgba(212,191,155,0.40); color: #7A7A7A; cursor: not-allowed; }
.btn-primary:focus-visible { outline: 2px solid #B9975C; outline-offset: 2px; }

[data-theme="dark"] .btn-primary { background-color: rgba(255,251,247,0.87); color: #1F1F1F; }
[data-theme="dark"] .btn-primary:hover { background-color: rgba(255,251,247,0.75); }
[data-theme="dark"] .btn-primary:disabled { background-color: #4A4A4A; color: rgba(255,251,247,0.38); }
```

---

### Secondary Button

```css
.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;
  padding: 9px 19px; /* -1px for border */

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 500;
  line-height: 1.4;

  background-color: transparent;
  color: #1F1F1F;
  border: 1px solid rgba(122,122,122,0.40);
  border-radius: 6px;

  cursor: pointer;
  transition: border-color 150ms ease;
}

.btn-secondary:hover { border-color: #7A7A7A; }
.btn-secondary:disabled { border-color: rgba(255,235,214,0.50); color: rgba(122,122,122,0.50); cursor: not-allowed; }
.btn-secondary:focus-visible { outline: 2px solid #B9975C; outline-offset: 2px; }

[data-theme="dark"] .btn-secondary { border-color: #4A4A4A; color: rgba(255,251,247,0.87); }
[data-theme="dark"] .btn-secondary:hover { border-color: #4A4A4A; }
```

---

### Ghost Button

```css
.btn-ghost {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;
  padding: 10px 20px;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 500;

  background-color: transparent;
  color: #454545;
  border: none;

  cursor: pointer;
  transition: color 150ms ease;
}

.btn-ghost:hover { color: #1F1F1F; }
.btn-ghost:focus-visible { outline: 2px solid #B9975C; outline-offset: 2px; }

[data-theme="dark"] .btn-ghost { color: rgba(255,251,247,0.60); }
[data-theme="dark"] .btn-ghost:hover { color: rgba(255,251,247,0.87); }
```

---

### Accent Button

```css
.btn-accent {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;
  padding: 10px 20px;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 500;
  line-height: 1.4;

  background-color: #B9975C;
  color: #1F1F1F;
  border: none;
  border-radius: 6px;

  cursor: pointer;
  transition: background-color 150ms ease;
}

.btn-accent:hover { background-color: #725A31; }
.btn-accent:focus-visible { outline: 2px solid #1F1F1F; outline-offset: 2px; }

[data-theme="dark"] .btn-accent { background-color: #D4BF9B; }
[data-theme="dark"] .btn-accent:hover { background-color: #B9975C; }
```

---

### Destructive Button

```css
.btn-destructive {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;
  padding: 9px 19px;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 500;

  background-color: transparent;
  color: #AE1C09;
  border: 1px solid #AE1C09;
  border-radius: 6px;

  cursor: pointer;
  transition: all 150ms ease;
}

.btn-destructive:hover { background-color: rgba(174,28,9,0.10); }
.btn-destructive:focus-visible { outline: 2px solid #AE1C09; outline-offset: 2px; }

[data-theme="dark"] .btn-destructive { color: #F5533D; border-color: #F5533D; }
[data-theme="dark"] .btn-destructive:hover { background-color: rgba(245,83,61,0.15); }
```

---

## Sizes

| Size | Height | Padding | Font Size |
|------|--------|---------|-----------|
| Small | 32px | 6px 12px | 13px |
| Medium | 44px | 10px 20px | 15px |
| Large | 52px | 14px 28px | 17px |

```css
.btn-sm { min-height: 32px; padding: 6px 12px; font-size: 13px; }
.btn-md { min-height: 44px; padding: 10px 20px; font-size: 15px; }
.btn-lg { min-height: 52px; padding: 14px 28px; font-size: 17px; }
```

---

## States Summary

### Primary

| State | Light BG | Light Text | Dark BG | Dark Text |
|-------|----------|------------|---------|-----------|
| default | #454545 | #FFFBF7 | rgba(255,251,247,0.87) | #1F1F1F |
| hover | #1F1F1F | #FFFBF7 | rgba(255,251,247,0.75) | #1F1F1F |
| active | #454545 | #FFFBF7 | rgba(255,251,247,0.87) | #1F1F1F |
| focus | + 2px accent outline | | + 2px accent outline | |
| disabled | rgba(212,191,155,0.40) | #7A7A7A | #4A4A4A | rgba(255,251,247,0.38) |
| loading | #454545 | text: "Loading..." | | |

### Secondary

| State | Light BG | Light Border | Dark Border |
|-------|----------|--------------|-------------|
| default | transparent | rgba(122,122,122,0.40) | #4A4A4A |
| hover | rgba(0,0,0,0.03) | #7A7A7A | #4A4A4A |
| active | rgba(0,0,0,0.05) | #1F1F1F | rgba(255,251,247,0.87) |
| disabled | transparent | rgba(255,235,214,0.50) | #2A2A2A |

### Accent

| State | Light BG | Dark BG |
|-------|----------|---------|
| default | #B9975C | #D4BF9B |
| hover | #725A31 | #B9975C |
| disabled | #FFEBD6 | |

---

## Decision Tree

```
Is it the PRIMARY action on the page?
  YES -> btn-primary (gunmetal/porcelain)
  NO  -> Is it a secondary/cancel action?
         YES -> btn-secondary (outline)
         NO  -> Is it destructive?
                YES -> btn-destructive (error outline)
                NO  -> Is it the ONLY CTA needing emphasis?
                       YES -> btn-accent (configurable, default Gold)
                       NO  -> btn-ghost (text only)

Size:
  Toolbar/tight space -> btn-sm (32px)
  Standard form/dialog -> btn-md (44px) [DEFAULT]
  Hero/standalone CTA -> btn-lg (52px)
```
