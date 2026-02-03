# Interactive States

Complete specification for every interactive state. No state should be undefined.

---

## Button States

### Primary Button

| State | Background | Text | Border | Other |
|-------|------------|------|--------|-------|
| default | #1C1C1A | #FFFFFF | none | - |
| hover | #333330 | #FFFFFF | none | - |
| active | #1C1C1A | #FFFFFF | none | transform: scale(0.98) |
| focus | #1C1C1A | #FFFFFF | none | outline: 2px solid #f59e0b, offset 2px |
| disabled | #E2E1DE | #8A8A86 | none | cursor: not-allowed |
| loading | #1C1C1A | #FFFFFF | none | text: "Loading..." |

**Dark Mode:**

| State | Background | Text |
|-------|------------|------|
| default | rgba(250,250,248,0.87) | #0a0a0b |
| hover | rgba(250,250,248,0.75) | #0a0a0b |
| active | rgba(250,250,248,0.87) | #0a0a0b |
| focus | rgba(250,250,248,0.87) | #0a0a0b |
| disabled | #3A3A3E | rgba(250,250,248,0.38) |

### Secondary Button

| State | Background | Text | Border |
|-------|------------|------|--------|
| default | transparent | #1C1C1A | 1px solid #C0BFBC |
| hover | rgba(0,0,0,0.03) | #1C1C1A | 1px solid #8A8A86 |
| active | rgba(0,0,0,0.05) | #1C1C1A | 1px solid #1C1C1A |
| focus | transparent | #1C1C1A | 1px solid #C0BFBC + outline |
| disabled | transparent | #C0BFBC | 1px solid #E2E1DE |

**Dark Mode:**

| State | Background | Text | Border |
|-------|------------|------|--------|
| default | transparent | rgba(250,250,248,0.87) | 1px solid #3A3A3E |
| hover | rgba(255,255,255,0.05) | rgba(250,250,248,0.87) | 1px solid #5A5A5E |
| active | rgba(255,255,255,0.08) | rgba(250,250,248,0.87) | 1px solid rgba(250,250,248,0.87) |
| disabled | transparent | rgba(250,250,248,0.38) | 1px solid #252527 |

### Ghost Button

| State | Background | Text | Border |
|-------|------------|------|--------|
| default | transparent | #5C5C58 | none |
| hover | rgba(0,0,0,0.03) | #1C1C1A | none |
| active | rgba(0,0,0,0.05) | #1C1C1A | none |
| focus | transparent | #1C1C1A | outline only |
| disabled | transparent | #C0BFBC | none |

### Accent Button (Amber)

| State | Background | Text | Border |
|-------|------------|------|--------|
| default | #f59e0b | #1C1C1A | none |
| hover | #d97706 | #1C1C1A | none |
| active | #f59e0b | #1C1C1A | transform: scale(0.98) |
| focus | #f59e0b | #1C1C1A | outline: 2px solid #f59e0b |
| disabled | #fef3c7 | #d97706 | none |

---

## Input States

### Text Input

| State | Background | Border | Text | Placeholder |
|-------|------------|--------|------|-------------|
| default | #FFFFFF | 1px solid #C0BFBC | #1C1C1A | #8A8A86 |
| hover | #FFFFFF | 1px solid #8A8A86 | #1C1C1A | #8A8A86 |
| focus | #FFFFFF | 1px solid #f59e0b | #1C1C1A | #8A8A86 |
| filled | #FFFFFF | 1px solid #C0BFBC | #1C1C1A | - |
| error | #FFFFFF | 1px solid #ef4444 | #1C1C1A | #8A8A86 |
| disabled | #F4F4F2 | 1px solid #E2E1DE | #8A8A86 | #C0BFBC |
| readonly | #FFFFFF | 1px solid #E2E1DE | #1C1C1A | - |

**Dark Mode:**

| State | Background | Border | Text | Placeholder |
|-------|------------|--------|------|-------------|
| default | #111113 | 1px solid #3A3A3E | rgba(250,250,248,0.87) | rgba(250,250,248,0.38) |
| hover | #111113 | 1px solid #5A5A5E | rgba(250,250,248,0.87) | rgba(250,250,248,0.38) |
| focus | #111113 | 1px solid #fbbf24 | rgba(250,250,248,0.87) | rgba(250,250,248,0.38) |
| error | #111113 | 1px solid #f87171 | rgba(250,250,248,0.87) | rgba(250,250,248,0.38) |
| disabled | #0a0a0b | 1px solid #252527 | rgba(250,250,248,0.38) | rgba(250,250,248,0.25) |

### Textarea

Same as text input, with:
- min-height: 120px
- resize: vertical
- padding: 12px

### Select

Same as text input, with:
- Dropdown icon: 20x20, aligned right, 12px from edge
- Dropdown icon color: var(--color-text-muted)

### Checkbox

| State | Box | Check | Label |
|-------|-----|-------|-------|
| unchecked | #FFFFFF, 1px #C0BFBC | hidden | #1C1C1A |
| unchecked:hover | #FFFFFF, 1px #8A8A86 | hidden | #1C1C1A |
| checked | #1C1C1A | #FFFFFF (stroke) | #1C1C1A |
| checked:hover | #333330 | #FFFFFF | #1C1C1A |
| indeterminate | #1C1C1A | #FFFFFF (dash) | #1C1C1A |
| disabled | #F4F4F2, 1px #E2E1DE | hidden | #8A8A86 |
| disabled:checked | #C0BFBC | #8A8A86 | #8A8A86 |

Size: 20x20, border-radius: 4px

### Radio

| State | Circle | Dot | Label |
|-------|--------|-----|-------|
| unselected | #FFFFFF, 1px #C0BFBC | hidden | #1C1C1A |
| unselected:hover | #FFFFFF, 1px #8A8A86 | hidden | #1C1C1A |
| selected | #1C1C1A | #FFFFFF (8px) | #1C1C1A |
| selected:hover | #333330 | #FFFFFF | #1C1C1A |
| disabled | #F4F4F2, 1px #E2E1DE | hidden | #8A8A86 |
| disabled:selected | #C0BFBC | #8A8A86 | #8A8A86 |

Size: 20x20, border-radius: 50%

### Toggle/Switch

| State | Track | Thumb |
|-------|-------|-------|
| off | #E2E1DE | #FFFFFF |
| off:hover | #C0BFBC | #FFFFFF |
| on | #1C1C1A | #FFFFFF |
| on:hover | #333330 | #FFFFFF |
| disabled:off | #EEEEED | #F4F4F2 |
| disabled:on | #C0BFBC | #E2E1DE |

Track size: 44x24, border-radius: 9999px
Thumb size: 20x20, border-radius: 50%

---

## Card States

| State | Background | Border | Shadow |
|-------|------------|--------|--------|
| default | #FFFFFF | 1px solid #E2E1DE | 0 1px 2px rgba(0,0,0,0.04) |
| hover | #FFFFFF | 1px solid #C0BFBC | 0 2px 4px rgba(0,0,0,0.06) |
| selected | #FFFFFF | 1px solid #1C1C1A | 0 1px 2px rgba(0,0,0,0.04) |
| active | #FFFFFF | 1px solid #1C1C1A | none |

**Dark Mode:**

| State | Background | Border | Shadow |
|-------|------------|--------|--------|
| default | #1A1A1C | 1px solid #1f1f23 | none |
| hover | #1A1A1C | 1px solid #2D2D30 | none |
| selected | #1A1A1C | 1px solid rgba(250,250,248,0.87) | none |
| active | #252527 | 1px solid rgba(250,250,248,0.87) | none |

---

## Navigation Item States

| State | Background | Text | Border |
|-------|------------|------|--------|
| default | transparent | #5C5C58 | none |
| hover | rgba(0,0,0,0.03) | #1C1C1A | none |
| active | rgba(0,0,0,0.05) | #1C1C1A | left: 2px solid #1C1C1A |
| current | rgba(0,0,0,0.05) | #1C1C1A | left: 2px solid #1C1C1A |
| disabled | transparent | #C0BFBC | none |

**Dark Mode:**

| State | Background | Text | Border |
|-------|------------|------|--------|
| default | transparent | rgba(250,250,248,0.60) | none |
| hover | rgba(255,255,255,0.05) | rgba(250,250,248,0.87) | none |
| active | rgba(255,255,255,0.08) | rgba(250,250,248,0.87) | left: 2px solid rgba(250,250,248,0.87) |

---

## Table Row States

| State | Background | Border |
|-------|------------|--------|
| default | transparent | bottom: 1px solid #E2E1DE |
| hover | rgba(0,0,0,0.02) | bottom: 1px solid #E2E1DE |
| selected | rgba(0,0,0,0.04) | bottom: 1px solid #E2E1DE |
| active | rgba(0,0,0,0.05) | bottom: 1px solid #C0BFBC |

**Dark Mode:**

| State | Background |
|-------|------------|
| default | transparent |
| hover | rgba(255,255,255,0.03) |
| selected | rgba(255,255,255,0.05) |
| active | rgba(255,255,255,0.08) |

---

## Link States

| State | Color | Decoration |
|-------|-------|------------|
| default | #1C1C1A | underline |
| hover | #1C1C1A | none |
| active | #1C1C1A | underline |
| visited | #5C5C58 | underline |

**Dark Mode:**

| State | Color |
|-------|-------|
| default | rgba(250,250,248,0.87) |
| hover | rgba(250,250,248,0.87) |
| visited | rgba(250,250,248,0.60) |

---

## Badge States

Badges are static. No interactive states. Status is communicated through color:

| Status | Background (Light) | Text (Light) |
|--------|-------------------|--------------|
| neutral | #F4F4F2 | #5C5C58 |
| success | #dcfce7 | #166534 |
| warning | #fef3c7 | #92400e |
| error | #fee2e2 | #991b1b |
| info | #dbeafe | #1e40af |

| Status | Background (Dark) | Text (Dark) |
|--------|-------------------|-------------|
| neutral | #252527 | rgba(250,250,248,0.60) |
| success | rgba(34,197,94,0.15) | #4ade80 |
| warning | rgba(234,179,8,0.15) | #facc15 |
| error | rgba(239,68,68,0.15) | #f87171 |
| info | rgba(59,130,246,0.15) | #60a5fa |

---

## Tab States

| State | Background | Text | Border |
|-------|------------|------|--------|
| default | transparent | #5C5C58 | bottom: 2px solid transparent |
| hover | transparent | #1C1C1A | bottom: 2px solid transparent |
| active | transparent | #1C1C1A | bottom: 2px solid #1C1C1A |
| disabled | transparent | #C0BFBC | bottom: 2px solid transparent |

---

## Dropdown Menu States

| Element | State | Background | Text |
|---------|-------|------------|------|
| Menu | - | #FFFFFF | - |
| Item | default | transparent | #1C1C1A |
| Item | hover | rgba(0,0,0,0.03) | #1C1C1A |
| Item | active | rgba(0,0,0,0.05) | #1C1C1A |
| Item | disabled | transparent | #C0BFBC |
| Separator | - | #E2E1DE | - |

**Dark Mode Menu Background:** #252527 (elevation-3)

---

## Tooltip States

Tooltips are informational. No interactive states.

| Theme | Background | Text | Arrow |
|-------|------------|------|-------|
| Light | #1C1C1A | #FFFFFF | #1C1C1A |
| Dark | #2D2D30 | rgba(250,250,248,0.87) | #2D2D30 |

---

## Toast/Notification States

| Type | Background | Icon | Text |
|------|------------|------|------|
| info | #dbeafe | #3b82f6 | #1e40af |
| success | #dcfce7 | #22c55e | #166534 |
| warning | #fef3c7 | #eab308 | #92400e |
| error | #fee2e2 | #ef4444 | #991b1b |

**Dark Mode uses rgba backgrounds as per badge specs.**

---

## Transition Timing

| Interaction | Duration | Easing |
|-------------|----------|--------|
| hover | 100ms | ease-out |
| focus | 100ms | ease-out |
| active | 50ms | ease-out |
| color change | 150ms | ease |
| transform | 150ms | ease-out |
| modal open | 250ms | ease-out |
| modal close | 200ms | ease-in |

**Max duration: 350ms. No decorative animations.**

---

## Focus Ring Specification

```css
/* All focusable elements */
:focus-visible {
  outline: 2px solid #f59e0b;
  outline-offset: 2px;
}

/* Remove default outline */
:focus {
  outline: none;
}

/* Buttons with custom focus */
.btn:focus-visible {
  outline: 2px solid #f59e0b;
  outline-offset: 2px;
}

/* Inputs with custom focus */
.input:focus {
  border-color: #f59e0b;
  outline: none;
}
```
