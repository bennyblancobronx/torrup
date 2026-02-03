# Crisp Design Language Skill

A Claude Code skill that generates UI components and layouts following the Crisp Design Language -- functional minimalism based on Dieter Rams' 10 Principles of Good Design.

## What it does

When activated, the skill gives the LLM a complete design system: typography (CrispByYosi), color tokens, spacing grid, component specs, layout templates, dark mode, accessibility, and anti-patterns. The LLM produces CSS/HTML that conforms to the system without needing external references.

## Structure

- `SKILL.md` -- Quick reference card loaded into context on activation. Contains the minimum needed to start producing correct output.
- `references/` -- 19 detailed spec files organized by concern (typography, colors, buttons, forms, brand, etc.). Read on demand when building specific components.
- `assets/` -- Production CSS, font files, design tokens JSON, Tailwind preset, and Stylelint config. These ship with the output.
- `scripts/` -- Accent generator, project bootstrap, and migration helper.
- `archive/v1/` -- Original files from before the 0.1.0 rebuild. Kept for reference.

## Key constraints

- Single typeface: CrispByYosi (weights 100/300/400/500/700, never 600)
- 8pt spacing grid
- Max border-radius: 8px (exceptions: circles, toggle switches)
- No decorative elements, animations, gradients, or multiple fonts
- Color communicates function only (success/error/warning/info + configurable accent)
- Accent is the only color that changes per app (default Gold #B9975C)
- All functional colors are locked across all apps
- Dark mode uses elevation surfaces, never shadows
- All files under 400 lines

## Version

0.1.4
