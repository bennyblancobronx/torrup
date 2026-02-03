/**
 * Crisp Design Language - Stylelint Configuration
 * Version: 0.1.3
 *
 * Automated enforcement of Crisp Design Language rules.
 *
 * Usage:
 *   npm install stylelint stylelint-config-standard stylelint-declaration-strict-value --save-dev
 *   Add to package.json: "stylelint": { "extends": "./path/to/stylelint.config.js" }
 *   Run: npx stylelint "**/*.css"
 */

module.exports = {
  extends: ['stylelint-config-standard'],
  plugins: ['stylelint-declaration-strict-value'],
  rules: {
    // ====================================
    // CRISP DESIGN LANGUAGE ENFORCEMENT
    // ====================================

    // COLORS: Force var() usage for all color properties (except design-system.css)
    'scale-unlimited/declaration-strict-value': [
      ['/color/', 'background-color', 'border-color', 'outline-color', 'fill', 'stroke'],
      {
        ignoreValues: ['transparent', 'inherit', 'currentColor', 'none', 'unset'],
        disableFix: true,
        message: 'Use var(--color-*) tokens instead of raw hex values',
      },
    ],

    // COLORS: No named colors
    'color-named': 'never',

    // Disallow pure black, gradients, text-shadow, animations
    'declaration-property-value-disallowed-list': {
      'color': ['/^#000/', '/^#000000/', '/^rgb\\(0,\\s*0,\\s*0\\)/', '/^black/'],
      'background-color': ['/^#000/', '/^#000000/', '/^rgb\\(0,\\s*0,\\s*0\\)/', '/^black/'],
      'background': ['/^#000/', '/^#000000/', '/^rgb\\(0,\\s*0,\\s*0\\)/', '/^black/'],
      'border-color': ['/^#000/', '/^#000000/', '/^rgb\\(0,\\s*0,\\s*0\\)/', '/^black/'],
      'border': ['/^#000/', '/^#000000/', '/^rgb\\(0,\\s*0,\\s*0\\)/', '/^black/'],
      'background-image': ['/^linear-gradient/', '/^radial-gradient/'],
      'text-shadow': ['/.+/'],
      'animation': ['/.+/'],
      'animation-name': ['/.+/'],
      'font-weight': ['600', 'semibold'],
    },

    // BORDER RADIUS: Max 8px (except 50% for circles)
    'declaration-property-value-allowed-list': {
      'border-radius': [
        '0',
        '0px',
        '4px',
        '6px',
        '8px',
        '50%',
        '9999px',
        'var(--radius-none)',
        'var(--radius-sm)',
        'var(--radius-md)',
        'var(--radius-lg)',
        'var(--radius-full)',
      ],
      'font-family': ['/CrispByYosi/', 'inherit', 'unset'],
    },

    // FONT FAMILY: Only CrispByYosi allowed
    'font-family-name-quotes': 'always-where-required',
    'font-family-no-missing-generic-family-keyword': null,

    // FONT WEIGHT: Only allowed weights (no 600)
    'font-weight-notation': 'numeric',

    // ====================================
    // GENERAL BEST PRACTICES
    // ====================================

    // No !important (except utilities)
    'declaration-no-important': true,

    // Consistent formatting
    'indentation': 2,
    'string-quotes': 'single',

    // No vendor prefixes (use autoprefixer)
    'property-no-vendor-prefix': true,
    'value-no-vendor-prefix': true,
    'selector-no-vendor-prefix': true,

    // No duplicate properties
    'declaration-block-no-duplicate-properties': true,

    // No unknown properties
    'property-no-unknown': [true, {
      ignoreProperties: [
        '/^--/',
      ],
    }],

    // Selector specificity
    'selector-max-id': 0,
    'selector-max-specificity': '0,4,0',

    // No units on zero values
    'length-zero-no-unit': true,

    // Shorthand properties
    'declaration-block-no-redundant-longhand-properties': true,

    // ====================================
    // NAMING CONVENTIONS
    // ====================================

    // BEM-like class naming
    'selector-class-pattern': [
      '^[a-z][a-z0-9]*(-[a-z0-9]+)*(__[a-z0-9]+(-[a-z0-9]+)*)?(--[a-z0-9]+(-[a-z0-9]+)*)?$|^is-[a-z]+$|^has-[a-z]+$',
      {
        message: 'Class names should follow pattern: block-name__element--modifier, is-state, or has-feature',
      },
    ],

    // Custom property naming
    'custom-property-pattern': [
      '^[a-z]+(-[a-z0-9]+)*$',
      {
        message: 'Custom properties should be lowercase with hyphens (e.g., --color-text)',
      },
    ],
  },

  // Ignore certain files
  ignoreFiles: [
    'node_modules/**',
    'dist/**',
    'build/**',
    '**/*.min.css',
    '**/design-system.css',
  ],
};
