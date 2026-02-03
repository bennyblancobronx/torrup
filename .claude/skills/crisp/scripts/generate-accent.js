#!/usr/bin/env node

/**
 * Crisp Design Language - Accent Generator
 * Version: 0.1.3
 *
 * Generates accent color variants from a single hex value using OKLCH color math.
 * All derivations use perceptual uniformity for consistent visual steps.
 *
 * Usage:
 *   node generate-accent.js "#B9975C"
 *   node generate-accent.js "#B9975C" --name "Camel"
 *   node generate-accent.js "#B9975C" --force
 *
 * Dependencies: culori (npm install culori)
 *
 * Output files:
 *   accent-tokens.json   - Design token values
 *   accent-vars.css      - CSS custom properties
 *   accent-tailwind.js   - Tailwind color config
 */

import { parse, formatHex, formatRgb, oklch, wcagContrast } from 'culori';

const CANVAS_LIGHT = '#fff8f2';
const CANVAS_DARK = '#1F1F1F';
const TEXT_DARK = '#1F1F1F';
const TEXT_LIGHT_87 = 'rgba(255, 251, 247, 0.87)';

function hexToOklch(hex) {
  return oklch(parse(hex));
}

function adjustLightness(hex, delta) {
  const color = hexToOklch(hex);
  color.l = Math.max(0, Math.min(1, color.l + delta));
  return formatHex(color);
}

function blendOnCanvas(hex, opacity, canvasHex) {
  const fg = parse(hex);
  const bg = parse(canvasHex);
  return {
    r: fg.r * opacity + bg.r * (1 - opacity),
    g: fg.g * opacity + bg.g * (1 - opacity),
    b: fg.b * opacity + bg.b * (1 - opacity),
    mode: 'rgb',
  };
}

function checkContrast(fg, bg, minRatio) {
  const ratio = wcagContrast(fg, bg);
  return { ratio: Math.round(ratio * 100) / 100, passes: ratio >= minRatio };
}

async function main() {
  const args = process.argv.slice(2);
  const force = args.includes('--force');
  const nameIdx = args.indexOf('--name');
  const name = nameIdx !== -1 ? args[nameIdx + 1] : null;
  const hex = args.find(a => /^#?[0-9a-fA-F]{6}$/.test(a));

  if (!hex) {
    console.error('Usage: generate-accent.js <hex> [--name "Name"] [--force]');
    console.error('  hex: 6-digit hex color (e.g., #B9975C or B9975C)');
    process.exit(1);
  }

  const input = hex.startsWith('#') ? hex : `#${hex}`;

  // Derive variants
  let accentHover = adjustLightness(input, -0.15);
  const accentDark = adjustLightness(input, 0.15);

  // Foreground: dark text if accent is light, light text if accent is dark
  const inputOklch = hexToOklch(input);
  const foreground = inputOklch.l > 0.55 ? TEXT_DARK : TEXT_LIGHT_87;

  // Contrast checks
  const checks = [
    { label: 'accent vs light canvas', ...checkContrast(input, CANVAS_LIGHT, 3) },
    { label: 'accent-dark vs dark canvas', ...checkContrast(accentDark, CANVAS_DARK, 3) },
    { label: 'foreground vs accent', ...checkContrast(foreground, input, 4.5) },
  ];

  let failures = checks.filter(c => !c.passes);

  // Edge case: if hover still fails 3:1, darken further
  let hoverCheck = checkContrast(accentHover, CANVAS_LIGHT, 3);
  while (!hoverCheck.passes) {
    accentHover = adjustLightness(accentHover, -0.05);
    hoverCheck = checkContrast(accentHover, CANVAS_LIGHT, 3);
  }

  // Warn on gray
  if (inputOklch.c < 0.02) {
    console.warn('Warning: accent is near-gray and may be indistinct from locked neutrals.');
  }

  if (failures.length > 0 && !force) {
    console.error('Contrast check failures:');
    failures.forEach(f => console.error(`  ${f.label}: ${f.ratio}:1 (needs 3:1 or 4.5:1)`));
    console.error('Use --force to override.');
    process.exit(1);
  }

  const tokens = {
    accent: input,
    'accent-hover': accentHover,
    'accent-surface': `rgba(${parse(input).r * 255 | 0}, ${parse(input).g * 255 | 0}, ${parse(input).b * 255 | 0}, 0.10)`,
    'accent-surface-dark': `rgba(${parse(input).r * 255 | 0}, ${parse(input).g * 255 | 0}, ${parse(input).b * 255 | 0}, 0.15)`,
    'accent-foreground': foreground,
    'accent-dark': accentDark,
    'accent-hover-dark': input,
  };

  // accent-tokens.json
  const jsonOut = JSON.stringify({ accent: tokens, name: name || null }, null, 2);

  // accent-vars.css
  const cssOut = `:root {
  --color-accent: ${tokens.accent};
  --color-accent-hover: ${tokens['accent-hover']};
  --color-accent-surface: ${tokens['accent-surface']};
  --color-accent-foreground: ${tokens['accent-foreground']};
}

[data-theme="dark"],
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-accent: ${tokens['accent-dark']};
    --color-accent-hover: ${tokens['accent-hover-dark']};
    --color-accent-surface: ${tokens['accent-surface-dark']};
    --color-accent-foreground: ${tokens['accent-foreground']};
  }
}
`;

  // accent-tailwind.js
  const twOut = `export default {
  accent: {
    DEFAULT: '${tokens.accent}',
    hover: '${tokens['accent-hover']}',
    surface: '${tokens['accent-surface']}',
    foreground: '${tokens['accent-foreground']}',
  },
};
`;

  const fs = await import('node:fs');
  fs.writeFileSync('accent-tokens.json', jsonOut);
  fs.writeFileSync('accent-vars.css', cssOut);
  fs.writeFileSync('accent-tailwind.js', twOut);

  console.log('Generated:');
  console.log('  accent-tokens.json');
  console.log('  accent-vars.css');
  console.log('  accent-tailwind.js');
  console.log('');
  console.log('Contrast results:');
  checks.forEach(c => console.log(`  ${c.passes ? 'PASS' : 'FAIL'} ${c.label}: ${c.ratio}:1`));
}

main();
