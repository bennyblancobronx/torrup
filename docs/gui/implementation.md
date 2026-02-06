# Torrup GUI Guide - Implementation

File structure and technical details for the Torrup GUI.

---

## File Structure

```
templates/
+-- index.html          # Dashboard (/) - stats, browse, queue
+-- browse.html         # Dedicated media browser (/browse)
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
    +-- dashboard.js    # Dashboard page logic (browse, queue, stats, chart)
    +-- browse.js       # Browse page logic (file list, selection, add to queue)
    +-- queue.js        # Queue page logic (filter, edit, delete, retry)
    +-- history.js      # History page logic (uploads tab, activity tab, details)
    +-- settings.js     # Settings page logic (save, dir picker, qBT test)

src/
+-- routes.py           # Page routes + /api/browse, /api/browse-dirs, /api/stats, /api/settings
+-- routes_queue.py     # /api/queue, /api/queue/add, /api/queue/update, /api/queue/delete
+-- routes_activity.py  # /api/activity/health, /api/activity/history
+-- utils/
    +-- activity.py     # Activity health calculation, monthly history, ntfy notifications
```

Note: There is no shared `base.html` template. Each page is a standalone HTML document that repeats the header/nav markup. Each page includes its own inline `<style>` block for page-specific styles.

---

## Template Pattern

Every template follows this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="csrf-token" content="{{ csrf_token() }}" />
  <title>{{ app_name }} [- Page Name]</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='css/fonts.css') }}" />
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}" />
  <script>/* Theme detection (localStorage -> data-theme) */</script>
  <style>/* Page-specific styles */</style>
</head>
<body>
  <header class="header">
    <!-- Brand + nav (repeated per page, is-active on current) -->
  </header>
  <main class="container page">
    <!-- Page content -->
  </main>
  <script>/* Inline globals: window.categoryOptions, window.csrfToken */</script>
  <script src="{{ url_for('static', filename='js/[page].js') }}"></script>
</body>
</html>
```

---

## Font Setup

CrispByYosi font files are in `static/fonts/`. The `static/css/fonts.css` declares all five weights:

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

## Route Registration

Routes are split across three files for file-size compliance:

- `src/routes.py` - Main blueprint (`bp`), page routes, `/api/browse`, `/api/browse-dirs`, `/api/stats`, `/api/settings`, `/api/settings/qbt/test`, `/health`
- `src/routes_queue.py` - Imports `bp` from routes.py and adds `/api/queue/*` endpoints
- `src/routes_activity.py` - Imports `bp` from routes.py and adds `/api/activity/*` endpoints

The queue and activity modules are imported at the bottom of `routes.py` to register their routes on the shared blueprint.

---

## Rate Limiting

All POST endpoints and some GET endpoints have rate limits via Flask-Limiter:

| Endpoint | Limit |
|----------|-------|
| `POST /api/queue/add` | 10/min |
| `POST /api/queue/update` | 30/min |
| `POST /api/queue/delete` | 20/min |
| `POST /api/settings` | 5/min |
| `POST /api/settings/qbt/test` | 5/min |
| `GET /api/browse` | 60/min |
| `GET /api/browse-dirs` | 60/min |
| `GET /api/activity/health` | 60/min |
| `GET /api/activity/history` | 30/min |

---

## Accessibility

- All interactive elements must be keyboard accessible
- Use semantic HTML (`nav`, `main`, `section`, `button`)
- Provide `aria-label` for icon-only buttons (e.g. Settings gear icon)
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

- [ ] Stat cards show queue count, automation status, last scan
- [ ] Activity warning banner appears when critical
- [ ] Monthly bar chart renders with data
- [ ] Browse library loads default media root
- [ ] File checkboxes toggle selection
- [ ] Add to Queue creates items and reloads queue table
- [ ] Inline queue editing (save/delete) works
- [ ] Stats auto-refresh every 30s
- [ ] Activity health auto-refresh every 60s

### Browse

- [ ] Media type dropdown switches libraries (only music enabled)
- [ ] Breadcrumb shows current path
- [ ] Clicking folder navigates into it
- [ ] Checkboxes toggle selection
- [ ] Select All works
- [ ] Selected count and size update correctly
- [ ] Add to Queue creates items and redirects

### Queue

- [ ] Filter tabs filter correctly
- [ ] Auto-refresh toggle works
- [ ] Edit panel opens/closes
- [ ] Save updates item in database
- [ ] Delete removes item
- [ ] Status badges show correct colors
- [ ] Retry resets failed items to queued

### History

- [ ] Tab switcher toggles between Uploads and Activity
- [ ] Monthly counter shows "This month: X / Y"
- [ ] Filters narrow results (status, date, media type)
- [ ] Clicking row shows details panel
- [ ] Details panel shows TL ID, category, tags, timestamp, path, files
- [ ] Activity tab shows timestamped log entries

### Settings

- [ ] All fields pre-populate with current values from server
- [ ] Directory picker modal works for output_dir and media root paths
- [ ] Theme selector changes theme and persists to localStorage
- [ ] Save persists all changes
- [ ] qBitTorrent test connection button works
- [ ] Non-music media types are visually disabled ("coming soon")
- [ ] Validation prevents invalid input

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 0.3.0 | 2026-02-06 | Updated docs to match implemented code: corrected API endpoints, page descriptions, file structure, settings sections |
| 0.2.0 | 2026-02-03 | Updated to Crisp Design Language compliance |
| 0.1.0 | 2026-02-03 | Initial GUI guide |

---

## Related Documents

- [Overview](overview.md) - Design system and shared layout
- [Pages](pages.md) - Page wireframes and components
- [API](api.md) - API endpoints and responses
