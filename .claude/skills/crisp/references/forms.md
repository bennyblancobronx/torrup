# Forms

## Text Input

```css
.input {
  width: 100%;
  min-height: 44px;
  padding: 10px 12px;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 400;
  line-height: 1.4;

  background-color: #FFFBF7;
  color: #1F1F1F;
  border: 1px solid rgba(122,122,122,0.40);
  border-radius: 6px;

  transition: border-color 150ms ease;
}

.input::placeholder { color: #7A7A7A; }
.input:hover { border-color: #7A7A7A; }
.input:focus { outline: none; border-color: #B9975C; }
.input:disabled { background-color: #FFFBF7; color: #7A7A7A; cursor: not-allowed; }
.input.input-error { border-color: #AE1C09; }

[data-theme="dark"] .input {
  background-color: #2A2A2A;
  color: rgba(255,251,247,0.87);
  border-color: #4A4A4A;
}
[data-theme="dark"] .input::placeholder { color: rgba(255,251,247,0.38); }
[data-theme="dark"] .input:hover { border-color: #4A4A4A; }
[data-theme="dark"] .input:focus { border-color: #D4BF9B; }
[data-theme="dark"] .input:disabled {
  background-color: #353535;
  color: rgba(255,251,247,0.38);
}
```

---

## Input Label

```css
.input-label {
  display: block;
  margin-bottom: 8px;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 11px;
  font-weight: 500;
  line-height: 1.3;
  letter-spacing: 0.1em;
  text-transform: uppercase;

  color: #454545;
}

[data-theme="dark"] .input-label { color: rgba(255,251,247,0.60); }
```

---

## Helper Text

```css
.input-helper {
  margin-top: 4px;
  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 13px;
  font-weight: 300;
  color: #7A7A7A;
}

.input-helper.input-helper-error { color: #AE1C09; }

[data-theme="dark"] .input-helper { color: rgba(255,251,247,0.38); }
```

---

## Textarea

Same as text input with:
- `min-height: 120px`
- `resize: vertical`
- `padding: 12px`

---

## Select

```css
.select {
  width: 100%;
  min-height: 44px;
  padding: 10px 12px;
  padding-right: 40px;

  font-family: 'CrispByYosi', system-ui, sans-serif;
  font-size: 15px;
  font-weight: 400;

  background-color: #FFFBF7;
  color: #1F1F1F;
  border: 1px solid rgba(122,122,122,0.40);
  border-radius: 6px;

  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23454545' stroke-width='2'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;

  cursor: pointer;
  transition: border-color 150ms ease;
}

.select:hover { border-color: #7A7A7A; }
.select:focus { outline: none; border-color: #B9975C; }
```

---

## Checkbox

```css
.checkbox {
  width: 20px;
  height: 20px;
  margin: 0;

  appearance: none;
  background-color: #FFFBF7;
  border: 1px solid rgba(122,122,122,0.40);
  border-radius: 4px;

  cursor: pointer;
  transition: all 150ms ease;
}

.checkbox:checked {
  background-color: #454545;
  border-color: #454545;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23FFFBF7' stroke-width='3'%3E%3Cpath d='M20 6 9 17l-5-5'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: center;
}

.checkbox:focus-visible { outline: 2px solid #B9975C; outline-offset: 2px; }

[data-theme="dark"] .checkbox { background-color: #2A2A2A; border-color: #4A4A4A; }
[data-theme="dark"] .checkbox:checked {
  background-color: rgba(255,251,247,0.87);
  border-color: rgba(255,251,247,0.87);
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%231F1F1F' stroke-width='3'%3E%3Cpath d='M20 6 9 17l-5-5'/%3E%3C/svg%3E");
}
```

---

## Radio Button

```css
.radio {
  width: 20px;
  height: 20px;
  margin: 0;

  appearance: none;
  background-color: #FFFBF7;
  border: 1px solid rgba(122,122,122,0.40);
  border-radius: 50%;

  cursor: pointer;
  transition: all 150ms ease;
}

.radio:hover { border-color: #7A7A7A; }

.radio:checked {
  background-color: #454545;
  border-color: #454545;
}

.radio:checked::after {
  content: '';
  display: block;
  width: 8px;
  height: 8px;
  margin: 5px;
  background-color: #FFFBF7;
  border-radius: 50%;
}

.radio:focus-visible { outline: 2px solid #B9975C; outline-offset: 2px; }
.radio:disabled { background-color: #FFFBF7; border-color: rgba(212,191,155,0.40); cursor: not-allowed; }

[data-theme="dark"] .radio { background-color: #2A2A2A; border-color: #4A4A4A; }
[data-theme="dark"] .radio:hover { border-color: #4A4A4A; }
[data-theme="dark"] .radio:checked {
  background-color: rgba(255,251,247,0.87);
  border-color: rgba(255,251,247,0.87);
}
[data-theme="dark"] .radio:checked::after { background-color: #1F1F1F; }
```

---

## Toggle Switch

```css
.toggle {
  position: relative;
  width: 44px;
  height: 24px;

  appearance: none;
  background-color: rgba(212,191,155,0.40);
  border: none;
  border-radius: 9999px; /* Exception: toggles use pill shape */

  cursor: pointer;
  transition: background-color 150ms ease;
}

.toggle::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;

  background-color: #FFFBF7;
  border-radius: 50%;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);

  transition: transform 150ms ease;
}

.toggle:checked { background-color: #454545; }
.toggle:checked::after { transform: translateX(20px); }
.toggle:focus-visible { outline: 2px solid #B9975C; outline-offset: 2px; }

[data-theme="dark"] .toggle { background-color: #4A4A4A; }
[data-theme="dark"] .toggle:checked { background-color: rgba(255,251,247,0.87); }
[data-theme="dark"] .toggle::after { background-color: #1F1F1F; }
```

---

## Input States Summary

| State | Background | Border | Text |
|-------|------------|--------|------|
| default | #FFFBF7 | 1px rgba(122,122,122,0.40) | #1F1F1F |
| hover | #FFFBF7 | 1px #7A7A7A | #1F1F1F |
| focus | #FFFBF7 | 1px #B9975C | #1F1F1F |
| error | #FFFBF7 | 1px #AE1C09 | #1F1F1F |
| disabled | #FFFBF7 | 1px rgba(212,191,155,0.40) | #7A7A7A |

## Form Layout

- Label above input, 8px gap
- Between fields: 16px
- Between sections: 48px
- Form max-width: 640px
- Form actions: flex, justify space-between, border-top 1px
