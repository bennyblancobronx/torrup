# Overlays

## Modals

```css
.modal-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 300;
}

.modal {
  background-color: #FFFBF7;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.08);
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
  border-bottom: 1px solid rgba(212,191,155,0.40);
}

.modal-title {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 17px;
  font-weight: 500;
  color: #1F1F1F;
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
  color: #454545;
  cursor: pointer;
  transition: background-color 150ms ease;
}

.modal-close:hover { background-color: rgba(0,0,0,0.05); }

.modal-body { padding: 24px; overflow-y: auto; }

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid rgba(212,191,155,0.40);
}

[data-theme="dark"] .modal-backdrop { background-color: rgba(0,0,0,0.7); }
[data-theme="dark"] .modal { background-color: #404040; box-shadow: none; }
[data-theme="dark"] .modal-header,
[data-theme="dark"] .modal-footer { border-color: #4A4A4A; }
[data-theme="dark"] .modal-title { color: rgba(255,251,247,0.87); }
[data-theme="dark"] .modal-close { color: rgba(255,251,247,0.60); }
[data-theme="dark"] .modal-close:hover { background-color: rgba(255,255,255,0.05); }
```

### Modal Selection

```
Simple confirmation or alert -> modal-sm (480px)
Form or moderate content     -> modal-md (640px) [DEFAULT]
Complex content or wide form -> modal-lg (800px)

All modals: padding 24px, border-radius 8px, backdrop rgba(0,0,0,0.5/0.7)
Mobile: full-screen with safe areas
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
  color: #FFFBF7;

  background-color: #454545;
  border-radius: 4px;
  z-index: 600;
}

[data-theme="dark"] .tooltip {
  background-color: #4A4A4A;
  color: rgba(255,251,247,0.87);
}
```

Tooltips are informational. No interactive states. No animations.

---

## Toasts

```css
.toast {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;

  border-radius: 6px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 400;

  z-index: 700;
}
```

### Toast Types (Light)

| Type | Background | Text |
|------|------------|------|
| info | rgba(73,105,110,0.10) | #314649 |
| success | rgba(40,103,54,0.10) | #173B1F |
| warning | rgba(168,134,43,0.10) | #6B5518 |
| error | rgba(174,28,9,0.10) | #741306 |
| neutral | #454545 | #FFFBF7 |

### Toast Types (Dark)

| Type | Background | Text |
|------|------------|------|
| info | rgba(145,177,182,0.15) | #91B1B6 |
| success | rgba(57,147,77,0.15) | #39934D |
| warning | rgba(212,173,74,0.15) | #D4AD4A |
| error | rgba(245,83,61,0.15) | #F5533D |
| neutral | #4A4A4A | rgba(255,251,247,0.87) |

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
  color: rgba(122,122,122,0.50);
  margin-bottom: 16px;
}

.empty-state-title {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 17px;
  font-weight: 500;
  color: #1F1F1F;
  margin-bottom: 8px;
}

.empty-state-description {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 400;
  color: #454545;
  max-width: 320px;
  margin-bottom: 24px;
}

/* No illustrations. No decorative elements. */

[data-theme="dark"] .empty-state-icon { color: #4A4A4A; }
[data-theme="dark"] .empty-state-title { color: rgba(255,251,247,0.87); }
[data-theme="dark"] .empty-state-description { color: rgba(255,251,247,0.60); }
```

---

## Loading States

| Duration | Treatment |
|----------|-----------|
| < 300ms | No indicator |
| 300ms - 2s | Text "Loading..." |
| > 2s | Static progress bar |

**Never:** Animated skeletons, shimmer effects, pulse animations, spinning icons.

```css
.loading-placeholder {
  background-color: #FFFBF7;
  border-radius: 4px;
  /* Static. No animation. */
}

.loading-text {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 13px;
  font-weight: 300;
  color: #7A7A7A;
}

.progress-bar {
  height: 4px;
  background-color: rgba(212,191,155,0.40);
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background-color: #454545;
  /* NO transition - instant updates only */
}

[data-theme="dark"] .loading-placeholder { background-color: #404040; }
[data-theme="dark"] .loading-text { color: rgba(255,251,247,0.38); }
[data-theme="dark"] .progress-bar { background-color: #4A4A4A; }
[data-theme="dark"] .progress-bar-fill { background-color: rgba(255,251,247,0.87); }
```
