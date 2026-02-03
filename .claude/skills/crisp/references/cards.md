# Cards

## Base Card

```css
.card {
  display: flex;
  flex-direction: column;

  background-color: #FFFBF7;
  border: 1px solid rgba(212,191,155,0.40);
  border-radius: 8px;
  overflow: hidden;

  transition: border-color 150ms ease;
}

.card:hover { border-color: rgba(122,122,122,0.40); }
.card.card-selected { border-color: #1F1F1F; }

[data-theme="dark"] .card { background-color: #353535; border-color: #353535; }
[data-theme="dark"] .card:hover { border-color: #4A4A4A; }
[data-theme="dark"] .card.card-selected { border-color: rgba(255,251,247,0.87); }
```

---

## Card Sizes

```css
.card-sm { padding: 12px; }
.card-md { padding: 16px; }
.card-lg { padding: 24px; }
```

---

## Card with Image

```css
.card-image {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  background-color: #FFFBF7;
}

.card-content { padding: 16px; }

.card-title {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 17px;
  font-weight: 500;
  color: #1F1F1F;
  margin-bottom: 4px;
}

.card-description {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 400;
  color: #454545;
}

.card-meta {
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 13px;
  font-weight: 300;
  color: #7A7A7A;
}

[data-theme="dark"] .card-image { background-color: #404040; }
[data-theme="dark"] .card-title { color: rgba(255,251,247,0.87); }
[data-theme="dark"] .card-description { color: rgba(255,251,247,0.60); }
[data-theme="dark"] .card-meta { color: rgba(255,251,247,0.38); }
```

---

## Card States

### Light Mode

| State | Background | Border | Shadow |
|-------|------------|--------|--------|
| default | #FFFBF7 | 1px solid rgba(212,191,155,0.40) | 0 1px 2px rgba(0,0,0,0.04) |
| hover | #FFFBF7 | 1px solid rgba(122,122,122,0.40) | 0 2px 4px rgba(0,0,0,0.06) |
| selected | #FFFBF7 | 1px solid #1F1F1F | 0 1px 2px rgba(0,0,0,0.04) |
| active | #FFFBF7 | 1px solid #1F1F1F | none |

### Dark Mode

| State | Background | Border | Shadow |
|-------|------------|--------|--------|
| default | #353535 | 1px solid #353535 | none |
| hover | #353535 | 1px solid #4A4A4A | none |
| selected | #353535 | 1px solid rgba(255,251,247,0.87) | none |
| active | #404040 | 1px solid rgba(255,251,247,0.87) | none |

---

## Card Grid

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}
```

Responsive behavior:
- Desktop (1024+): 3-4 columns
- Tablet (640-1023): 2 columns
- Mobile (<640): 1 column
