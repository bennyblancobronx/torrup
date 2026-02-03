# Accessibility

## Contrast Requirements

| Element | Minimum Ratio |
|---------|---------------|
| Normal text (< 24px) | 4.5:1 |
| Large text (24px+) | 3:1 |
| UI components | 3:1 |
| Focus indicators | 3:1 |

All Crisp Design Language color combinations meet or exceed these ratios. See `references/dark-mode.md` for verified contrast values.

### Light Mode Contrast (on #fff8f2)

| Combination | Ratio | Pass |
|-------------|-------|------|
| #1F1F1F on #fff8f2 | 15.67:1 | AA |
| #454545 on #fff8f2 | 9.11:1 | AA |
| #7A7A7A on #fff8f2 | 4.08:1 | AA-large/UI only (captions, icons) |
| #725A31 on #fff8f2 | 6.19:1 | AA |
| #B9975C on #fff8f2 | 2.61:1 | Fails 3:1 -- never use as text on canvas |
| #AE1C09 on #fff8f2 | 6.72:1 | AA |
| #286736 on #fff8f2 | 6.47:1 | AA |
| #A8862B on #fff8f2 | 3.27:1 | AA-large/UI only |
| #49696E on #fff8f2 | 5.66:1 | AA |

Accent (#B9975C) is safe as a button fill where text sits on the accent, not against canvas. Focus rings are 2px solid which meets non-text UI at 3:1 against adjacent colors. The generate-accent.js script enforces 3:1 for UI components and 4.5:1 for accent-foreground on accent fill.

### Dark Mode Contrast (on #1F1F1F)

| Combination | Ratio | Pass |
|-------------|-------|------|
| rgba(255,251,247,0.87) on #1F1F1F | 12.33:1 | AA |
| rgba(255,251,247,0.60) on #1F1F1F | 6.56:1 | AA |
| rgba(255,251,247,0.38) on #1F1F1F | 3.48:1 | AA-large/UI only (captions, icons) |
| #D4BF9B on #1F1F1F | 9.20:1 | AA |
| #39934D on #1F1F1F | 4.28:1 | AA-large/UI only |
| #D4AD4A on #1F1F1F | 7.75:1 | AA |
| #F5533D on #1F1F1F | 4.86:1 | AA |
| #91B1B6 on #1F1F1F | 7.20:1 | AA |

---

## Touch Targets

- Minimum: 44x44px
- Recommended: 48x48px

All interactive components (buttons, inputs, checkboxes, radios, toggles) have `min-height: 44px` by default.

Small buttons (32px height) should only be used in toolbars where adjacent spacing provides adequate combined target area.

---

## Focus States

All focusable elements must show a visible focus indicator:

```css
:focus-visible {
  outline: 2px solid #B9975C;
  outline-offset: 2px;
}
```

Inputs use border color instead of outline:

```css
.input:focus {
  border-color: #B9975C;
  outline: none;
}
```

Focus must be visible in both light and dark modes. The accent color (#B9975C / #D4BF9B) provides sufficient contrast against all background colors.

---

## ARIA Patterns

### Buttons

- Use `<button>` for actions, `<a>` for navigation
- Destructive actions: `aria-label` describing the action
- Loading state: `aria-busy="true"`, `aria-label="Loading"`
- Icon-only buttons: always include `aria-label`

### Forms

- Every input needs a `<label>` or `aria-label`
- Error messages: `aria-describedby` linking input to error text
- Required fields: `aria-required="true"`
- Invalid fields: `aria-invalid="true"`

### Modals

- `role="dialog"` and `aria-modal="true"`
- `aria-labelledby` pointing to the modal title
- Focus trap: tab cycles within the modal
- Escape key closes the modal
- Return focus to trigger element on close

### Navigation

- Sidebar: `<nav>` with `aria-label="Main navigation"`
- Active item: `aria-current="page"`
- Tabs: `role="tablist"`, `role="tab"`, `role="tabpanel"`
- Selected tab: `aria-selected="true"`

### Tables

- Use `<th scope="col">` for column headers
- Sortable columns: `aria-sort="ascending"` / `"descending"` / `"none"`
- Row selection: `aria-selected="true"`

### Toasts

- `role="alert"` for error toasts
- `role="status"` for success/info toasts
- Auto-dismiss after 5-8 seconds (not less)
- Provide a dismiss button

---

## Keyboard Navigation

- Tab moves between interactive elements
- Enter/Space activates buttons
- Arrow keys navigate within tabs, radios, menus
- Escape closes modals, dropdowns, popovers
- Home/End jumps to first/last item in lists

---

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
  }
}
```

The Crisp design language already minimizes motion (max 350ms, no decorative animations), but this media query respects users who prefer even less.
