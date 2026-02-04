# Typography

## CrispByYosi

CrispByYosi is the exclusive typeface for all implementations. Created by Iconwerk for Crisp Global.

```css
font-family: 'CrispByYosi', system-ui, sans-serif;
```

Single font family for ALL text. No exceptions. Code, headings, body, labels -- all CrispByYosi.

---

## Distinctive Characteristics

1. **Racetrack terminals** -- Character endings feature the signature "racetrack" shape (stadium curve), visible in letters like C, G, S, e, c, s

2. **Narrow capitals** -- Uppercase letters are proportionally narrower than typical sans-serifs

3. **Circular dots** -- Periods, dots on i/j, and diacritics are perfect circles

4. **Technical precision** -- Geometric construction with optical corrections

5. **Lowercase emphasis** -- The typeface is optimized for lowercase text, reflecting Crisp's preference for lowercase in product labeling

---

## Weight Usage

| Weight | Value | Character | Use |
|--------|-------|-----------|-----|
| Thin | 100 | Elegant, delicate | Display numerics, decorative (rare) |
| Light | 300 | Refined, subtle | Captions, metadata, code, hashes |
| Regular | 400 | Balanced, neutral | Body text, input values |
| Medium | 500 | Confident, clear | Buttons, navigation, labels, headings |
| Bold | 700 | Strong, authoritative | Titles, hero text |

**Weight 600 (semibold) does not exist. Always use 500 or 700.**

---

## Type Scale

| Token | Size | Weight | Line Height | Letter Spacing | Use |
|-------|------|--------|-------------|----------------|-----|
| text-xs | 11px | 500 | 1.3 | 0.1em | Labels (UPPERCASE) |
| text-sm | 13px | 300 | 1.5 | 0 | Captions, metadata, code |
| text-base | 15px | 400 | 1.6 | 0 | Body text |
| text-lg | 17px | 500 | 1.5 | 0 | Subsection heads |
| text-xl | 20px | 500 | 1.4 | -0.01em | Section heads |
| text-2xl | 24px | 700 | 1.3 | -0.01em | Page titles |
| text-3xl | 30px | 700 | 1.2 | -0.02em | Hero titles |
| text-4xl | 36px | 700 | 1.2 | -0.02em | Display (rare) |

---

## Font Face Setup

```css
@font-face {
  font-family: 'CrispByYosi';
  src: url('fonts/CrispByYosi-Thin.woff2') format('woff2');
  font-weight: 100;
  font-display: swap;
}

@font-face {
  font-family: 'CrispByYosi';
  src: url('fonts/CrispByYosi-Light.woff2') format('woff2');
  font-weight: 300;
  font-display: swap;
}

@font-face {
  font-family: 'CrispByYosi';
  src: url('fonts/CrispByYosi-Regular.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
}

@font-face {
  font-family: 'CrispByYosi';
  src: url('fonts/CrispByYosi-Medium.woff2') format('woff2');
  font-weight: 500;
  font-display: swap;
}

@font-face {
  font-family: 'CrispByYosi';
  src: url('fonts/CrispByYosi-Bold.woff2') format('woff2');
  font-weight: 700;
  font-display: swap;
}
```

See `assets/css/fonts.css` for the production version.

---

## Quick Decisions

```
Page title?           -> 700 Bold, 24px
Section heading?      -> 500 Medium, 20px
Subsection heading?   -> 500 Medium, 17px
Body text?            -> 400 Regular, 15px
Caption/meta?         -> 300 Light, 13px
Uppercase label?      -> 500 Medium, 11px, 0.1em spacing
Code/hash/ID?         -> 300 Light, 13px
```
