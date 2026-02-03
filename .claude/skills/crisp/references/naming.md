# Naming Conventions

## Components

```
btn-{variant}     -> btn-primary, btn-secondary, btn-ghost, btn-accent, btn-destructive
btn-{size}        -> btn-sm, btn-md, btn-lg
input-{variant}   -> input-default, input-error
card-{size}       -> card-sm, card-md, card-lg
card-{part}       -> card-image, card-content, card-title, card-description, card-meta
badge-{status}    -> badge-success, badge-warning, badge-error, badge-info, badge-accent
modal-{size}      -> modal-sm, modal-md, modal-lg
modal-{part}      -> modal-header, modal-body, modal-footer, modal-title, modal-close
avatar-{size}     -> avatar-sm, avatar-md, avatar-lg, avatar-xl
icon-{size}       -> icon-sm, icon-md, icon-lg, icon-xl
status-indicator-{status} -> status-indicator-success, status-indicator-error
toast-{type}      -> toast-success, toast-warning, toast-error, toast-info, toast-neutral
```

## Layout

```
layout-{type}         -> layout-dashboard, layout-settings
sidebar-{element}     -> sidebar-nav, sidebar-brand, sidebar-version
header-{element}      -> header-title, header-actions
detail-{element}      -> detail-header, detail-content, detail-grid, detail-list
form-{element}        -> form-container, form-section, form-field, form-actions
form-section-{part}   -> form-section-title, form-section-desc
table-{element}       -> table-toolbar, table-pagination
empty-state-{element} -> empty-state-icon, empty-state-title, empty-state-description
```

## Navigation

```
sidebar-nav-item      -> Individual nav link
tab                   -> Tab element
tabs                  -> Tab container
dropdown              -> Dropdown wrapper
dropdown-menu         -> Dropdown panel
dropdown-item         -> Dropdown option
dropdown-separator    -> Dropdown divider
settings-nav-item     -> Settings sidebar tab
```

## Utilities

```
text-{role}       -> text-primary, text-secondary, text-muted
bg-{surface}      -> bg-canvas, bg-surface, bg-elevated
divider           -> Horizontal rule
divider-vertical  -> Vertical rule
divider-with-text -> Rule with centered label
```

## States

```
is-{state}        -> is-active, is-disabled, is-loading, is-open
has-{feature}     -> has-error, has-icon
```

## Density

```
density-{level}   -> density-compact, density-default, density-spacious
```

## Dark Mode

```
[data-theme="dark"]  -> Applied to root element
[data-theme="light"] -> Applied to root element
```

Use `data-theme` attribute selectors for all theme-specific overrides. Use `@media (prefers-color-scheme: dark)` for system-level defaults.
