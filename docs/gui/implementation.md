# Torrup GUI Guide - Implementation

Phased implementation plan and file structure.

---

## File Structure

```
templates/
+-- base.html           # Shared layout (header, nav, footer)
+-- index.html          # Dashboard (/)
+-- browse.html         # Media browser (/browse)
+-- queue.html          # Queue management (/queue)
+-- history.html        # Upload history (/history)
+-- settings.html       # Settings (/settings)

static/
+-- css/
|   +-- fonts.css       # CrispByYosi font-face declarations
|   +-- style.css       # Crisp Design Language styles
+-- fonts/
|   +-- CrispByYosi-Thin.woff2
|   +-- CrispByYosi-Light.woff2
|   +-- CrispByYosi-Regular.woff2
|   +-- CrispByYosi-Medium.woff2
|   +-- CrispByYosi-Bold.woff2
+-- js/
    +-- app.js          # Shared JavaScript (optional, can be inline)
```

---

## Font Setup

Copy CrispByYosi font files from `.claude/skills/crisp/assets/fonts/` to `static/fonts/`.

Create `static/css/fonts.css`:

```css
@font-face {
  font-family: 'CrispByYosi';
  src: url('../fonts/CrispByYosi-Thin.woff2') format('woff2');
  font-weight: 100;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'CrispByYosi';
  src: url('../fonts/CrispByYosi-Light.woff2') format('woff2');
  font-weight: 300;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'CrispByYosi';
  src: url('../fonts/CrispByYosi-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'CrispByYosi';
  src: url('../fonts/CrispByYosi-Medium.woff2') format('woff2');
  font-weight: 500;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'CrispByYosi';
  src: url('../fonts/CrispByYosi-Bold.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}
```

---

## Implementation Phases

### Phase 1: Base Layout and Crisp Setup

1. Copy CrispByYosi font files to `static/fonts/`
2. Create `fonts.css` with @font-face declarations
3. Create `style.css` with Crisp Design Language CSS variables
4. Create `base.html` with shared header and navigation
5. Update existing pages to extend `base.html`

**Files to create/modify:**
- `static/fonts/` (copy font files)
- `static/css/fonts.css` (new)
- `static/css/style.css` (new)
- `templates/base.html` (new)
- `templates/index.html` (modify)
- `templates/settings.html` (modify)

---

### Phase 2: Dashboard

6. Convert current index to dashboard with stats
7. Add `/api/stats` endpoint
8. Add `/api/system` endpoint

**Files to create/modify:**
- `templates/index.html` (modify)
- `src/routes.py` (add endpoints)

---

### Phase 3: Browse and Queue Pages

9. Create `/browse` page (extract from current index)
10. Create `/queue` page (extract from current index)
11. Improve queue editing UX with expandable panel

**Files to create/modify:**
- `templates/browse.html` (new)
- `templates/queue.html` (new)
- `src/routes.py` (add routes)

---

### Phase 4: History Page

12. Create `/history` page
13. Add `/api/history` endpoint
14. Add activity logging to queue operations

**Files to create/modify:**
- `templates/history.html` (new)
- `src/routes.py` (add endpoint)
- `src/db.py` (add history queries)

---

### Phase 5: Polish

15. Add loading states (simple opacity fade, no skeleton loaders)
16. Add error handling UI (toast notifications)
17. Add beginner tooltips and help text
18. Responsive adjustments for mobile

**Crisp Loading States:**
- Use opacity transitions (0 to 1)
- No animated skeleton loaders
- Simple "Loading..." text is acceptable
- Disabled button states during submission

---

## Accessibility

- All interactive elements must be keyboard accessible
- Use semantic HTML (`nav`, `main`, `section`, `button`)
- Provide `aria-label` for icon-only buttons
- Maintain color contrast ratio of at least 4.5:1
- Status indicators must not rely on color alone (add text/icons)
- Focus states: 2px accent outline with 2px offset
- Touch targets minimum 44px

---

## Browser Support

| Browser | Minimum Version |
|---------|-----------------|
| Chrome | 90+ |
| Firefox | 88+ |
| Safari | 14+ |
| Edge | 90+ |

No IE11 support required.

---

## Testing Checklist

### Crisp Compliance (Every Page)

- [ ] Font is CrispByYosi (inspect ALL text elements)
- [ ] All spacing on 8pt grid (4, 8, 12, 16, 24, 32, 48, 64)
- [ ] No border-radius > 8px (except 50% circles)
- [ ] No pure black (#000) or pure white (#FFF)
- [ ] No decorative shadows in dark mode
- [ ] No animated skeleton loaders
- [ ] No font-weight 600 (use 500 or 700)
- [ ] Touch targets >= 44px
- [ ] Focus states visible (2px accent outline)

### Functional (Every Page)

- [ ] Renders without JavaScript errors
- [ ] All links navigate correctly
- [ ] Forms submit and validate properly
- [ ] Loading states display during API calls
- [ ] Error states display on API failure
- [ ] Responsive on mobile (375px width)
- [ ] Keyboard navigation works
- [ ] Screen reader announces content correctly

### Dashboard

- [ ] Stat cards show correct counts
- [ ] Quick action buttons link to correct pages
- [ ] Recent activity shows latest 5 items
- [ ] System status shows dependency state
- [ ] Auto-refreshes periodically (optional)

### Browse

- [ ] Media type dropdown switches libraries
- [ ] Breadcrumb shows current path
- [ ] Clicking folder navigates into it
- [ ] Checkboxes toggle selection
- [ ] Selected count updates correctly
- [ ] Add to Queue creates items and redirects

### Queue

- [ ] Filter tabs filter correctly
- [ ] Edit panel opens/closes
- [ ] Save updates item in database
- [ ] Delete removes item
- [ ] Status badges show correct colors
- [ ] Retry resets failed items to queued

### History

- [ ] Tab switcher toggles views
- [ ] Filters narrow results
- [ ] Clicking row shows details
- [ ] Pagination works (if implemented)

### Settings

- [ ] All fields pre-populate with current values
- [ ] Save persists changes
- [ ] Validation prevents invalid input
- [ ] System status reflects actual state

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 0.2.0 | 2026-02-03 | Updated to Crisp Design Language compliance |
| 0.1.0 | 2026-02-03 | Initial GUI guide |

---

## Related Documents

- [Overview](overview.md) - Design system and shared layout
- [Pages](pages.md) - Page wireframes and components
- [API](api.md) - API endpoints and responses
