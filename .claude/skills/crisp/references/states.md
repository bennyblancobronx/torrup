# Interactive States

Complete specification for every interactive state. No state should be undefined.

---

## Button States

### Primary Button

| State | Light BG | Light Text | Dark BG | Dark Text |
|-------|----------|------------|---------|-----------|
| default | #454545 | #FFFBF7 | rgba(255,251,247,0.87) | #1F1F1F |
| hover | #1F1F1F | #FFFBF7 | rgba(255,251,247,0.75) | #1F1F1F |
| active | #454545 | #FFFBF7 | rgba(255,251,247,0.87) | #1F1F1F |
| focus | + 2px accent outline | | + 2px accent outline | |
| disabled | rgba(212,191,155,0.40) | #7A7A7A | #4A4A4A | rgba(255,251,247,0.38) |
| loading | text: "Loading..." | | | |

### Secondary Button

| State | Light BG | Light Border | Dark Border |
|-------|----------|--------------|-------------|
| default | transparent | rgba(122,122,122,0.40) | #4A4A4A |
| hover | rgba(0,0,0,0.03) | #7A7A7A | #4A4A4A |
| active | rgba(0,0,0,0.05) | #1F1F1F | rgba(255,251,247,0.87) |
| disabled | transparent | rgba(255,235,214,0.50) | #2A2A2A |

### Ghost Button

| State | Light BG | Light Text |
|-------|----------|------------|
| default | transparent | #454545 |
| hover | rgba(0,0,0,0.03) | #1F1F1F |
| active | rgba(0,0,0,0.05) | #1F1F1F |
| disabled | transparent | rgba(122,122,122,0.50) |

### Accent Button (configurable, default Gold)

| State | Light BG | Dark BG |
|-------|----------|---------|
| default | #B9975C | #D4BF9B |
| hover | #725A31 | #B9975C |
| active | #B9975C | #D4BF9B |
| disabled | #FFEBD6 | |

---

## Input States

### Text Input

| State | Light BG | Light Border | Dark BG | Dark Border |
|-------|----------|--------------|---------|-------------|
| default | #FFFBF7 | rgba(122,122,122,0.40) | #2A2A2A | #4A4A4A |
| hover | #FFFBF7 | #7A7A7A | #2A2A2A | #4A4A4A |
| focus | #FFFBF7 | #B9975C | #2A2A2A | #D4BF9B |
| filled | #FFFBF7 | rgba(122,122,122,0.40) | #2A2A2A | #4A4A4A |
| error | #FFFBF7 | #AE1C09 | #2A2A2A | #F5533D |
| disabled | #FFFBF7 | rgba(212,191,155,0.40) | #1F1F1F | #2A2A2A |
| readonly | #FFFBF7 | rgba(212,191,155,0.40) | #2A2A2A | #353535 |

### Textarea

Same as text input. Additional: min-height 120px, resize vertical, padding 12px.

### Select

Same as text input. Additional: dropdown icon 20x20, right-aligned 12px from edge.

### Checkbox

| State | Light Box | Light Check |
|-------|-----------|-------------|
| unchecked | #FFFBF7, 1px rgba(122,122,122,0.40) | hidden |
| unchecked:hover | #FFFBF7, 1px #7A7A7A | hidden |
| checked | #454545 | #FFFBF7 stroke |
| checked:hover | #1F1F1F | #FFFBF7 |
| indeterminate | #454545 | #FFFBF7 dash |
| disabled | #FFFBF7, 1px rgba(212,191,155,0.40) | hidden |
| disabled:checked | rgba(122,122,122,0.50) | #7A7A7A |

Size: 20x20, border-radius 4px.

### Radio

| State | Light Circle | Light Dot |
|-------|-------------|-----------|
| unselected | #FFFBF7, 1px rgba(122,122,122,0.40) | hidden |
| unselected:hover | #FFFBF7, 1px #7A7A7A | hidden |
| selected | #454545 | #FFFBF7 (8px) |
| selected:hover | #1F1F1F | #FFFBF7 |
| disabled | #FFFBF7, 1px rgba(212,191,155,0.40) | hidden |
| disabled:selected | rgba(122,122,122,0.50) | #7A7A7A |

Size: 20x20, border-radius 50%.

### Toggle/Switch

| State | Track | Thumb |
|-------|-------|-------|
| off | rgba(212,191,155,0.40) | #FFFBF7 |
| off:hover | rgba(122,122,122,0.40) | #FFFBF7 |
| on | #454545 | #FFFBF7 |
| on:hover | #1F1F1F | #FFFBF7 |
| disabled:off | rgba(255,235,214,0.50) | #FFFBF7 |
| disabled:on | rgba(122,122,122,0.50) | rgba(212,191,155,0.40) |

Track: 44x24, radius 9999px. Thumb: 20x20, radius 50%.

---

## Card States

| State | Light BG | Light Border | Light Shadow |
|-------|----------|--------------|--------------|
| default | #FFFBF7 | rgba(212,191,155,0.40) | 0 1px 2px rgba(0,0,0,0.04) |
| hover | #FFFBF7 | rgba(122,122,122,0.40) | 0 2px 4px rgba(0,0,0,0.06) |
| selected | #FFFBF7 | #1F1F1F | 0 1px 2px rgba(0,0,0,0.04) |
| active | #FFFBF7 | #1F1F1F | none |

| State | Dark BG | Dark Border | Dark Shadow |
|-------|---------|-------------|-------------|
| default | #353535 | #353535 | none |
| hover | #353535 | #4A4A4A | none |
| selected | #353535 | rgba(255,251,247,0.87) | none |
| active | #404040 | rgba(255,251,247,0.87) | none |

---

## Navigation Item States

| State | Light BG | Light Text |
|-------|----------|------------|
| default | transparent | #454545 |
| hover | rgba(0,0,0,0.03) | #1F1F1F |
| active | rgba(0,0,0,0.05) | #1F1F1F |
| disabled | transparent | rgba(122,122,122,0.50) |

| State | Dark BG | Dark Text |
|-------|---------|-----------|
| default | transparent | rgba(255,251,247,0.60) |
| hover | rgba(255,255,255,0.05) | rgba(255,251,247,0.87) |
| active | rgba(255,255,255,0.08) | rgba(255,251,247,0.87) |

---

## Tab States

| State | Text | Bottom Border |
|-------|------|---------------|
| default | #454545 | 2px transparent |
| hover | #1F1F1F | 2px transparent |
| active | #1F1F1F | 2px #1F1F1F |
| disabled | rgba(122,122,122,0.50) | 2px transparent |

---

## Table Row States

| State | Light BG | Dark BG |
|-------|----------|---------|
| default | transparent | transparent |
| hover | rgba(0,0,0,0.02) | rgba(255,255,255,0.03) |
| selected | rgba(0,0,0,0.04) | rgba(255,255,255,0.05) |
| active | rgba(0,0,0,0.05) | rgba(255,255,255,0.08) |

---

## Link States

| State | Light Color | Decoration |
|-------|-------------|------------|
| default | #1F1F1F | underline |
| hover | #1F1F1F | none |
| active | #1F1F1F | underline |
| visited | #454545 | underline |

Dark: default rgba(255,251,247,0.87), visited rgba(255,251,247,0.60).

---

## Badge States

Badges are static. No interactive states. Status communicated through color only. See `references/data-display.md` for badge specs.

---

## Dropdown Menu States

| Element | State | Light BG | Light Text |
|---------|-------|----------|------------|
| Item | default | transparent | #1F1F1F |
| Item | hover | rgba(0,0,0,0.03) | #1F1F1F |
| Item | active | rgba(0,0,0,0.05) | #1F1F1F |
| Item | disabled | transparent | rgba(122,122,122,0.50) |
| Separator | -- | rgba(212,191,155,0.40) | -- |

Dark menu background: #404040 (elevation-3).

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

Max duration: 350ms. No decorative animations.

---

## Focus Ring

```css
:focus-visible {
  outline: 2px solid #B9975C;
  outline-offset: 2px;
}

:focus { outline: none; }

.input:focus {
  border-color: #B9975C;
  outline: none;
}
```
