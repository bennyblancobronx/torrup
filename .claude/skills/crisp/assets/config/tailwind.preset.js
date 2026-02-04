/**
 * Crisp Design Language - Tailwind Preset
 * Version: 0.1.3
 *
 * Usage in your tailwind.config.js:
 *
 *   import crispPreset from './path/to/tailwind.preset.js';
 *   export default {
 *     presets: [crispPreset],
 *     content: ['./src/**\/*.{html,js,svelte,ts,tsx}'],
 *   };
 *
 * RULES ENFORCED:
 * - 8px grid (spacing multiples of 8)
 * - Max border radius: 8px (except full circles)
 * - No pure black (#000) or pure white (#FFF)
 * - Single font: CrispByYosi
 */

/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Light mode surfaces
        canvas: '#fff8f2',
        surface: '#FFFBF7',
        'surface-elevated': '#FFFBF7',

        // Light mode text
        foreground: '#1F1F1F',
        'muted-foreground': '#454545',
        'subtle-foreground': '#7A7A7A',

        // Light mode borders (solid hex fallbacks)
        border: '#EDE3D4',
        'border-emphasis': '#C2BAB1',

        // Primary (Neutral)
        primary: {
          DEFAULT: '#454545',
          hover: '#1F1F1F',
          foreground: '#FFFBF7',
        },

        // Accent (configurable, default Gold)
        accent: {
          DEFAULT: '#B9975C',
          hover: '#725A31',
          surface: '#FFEBD6',
          foreground: '#1F1F1F',
        },

        // Functional colors
        success: {
          DEFAULT: '#286736',
          surface: 'rgba(40, 103, 54, 0.10)',
          foreground: '#173B1F',
        },
        warning: {
          DEFAULT: '#A8862B',
          surface: 'rgba(168, 134, 43, 0.10)',
          foreground: '#6B5518',
        },
        error: {
          DEFAULT: '#AE1C09',
          surface: 'rgba(174, 28, 9, 0.10)',
          foreground: '#741306',
        },
        info: {
          DEFAULT: '#49696E',
          surface: 'rgba(73, 105, 110, 0.10)',
          foreground: '#314649',
        },

        // Dark mode elevation surfaces
        elevation: {
          0: '#1F1F1F',
          1: '#2A2A2A',
          2: '#353535',
          3: '#404040',
          4: '#4A4A4A',
        },
      },

      fontFamily: {
        sans: ['CrispByYosi', 'system-ui', 'sans-serif'],
      },

      fontWeight: {
        thin: '100',
        light: '300',
        normal: '400',
        medium: '500',
        bold: '700',
        // Note: 600 (semibold) does NOT exist in CrispByYosi
      },

      fontSize: {
        xs: ['11px', { lineHeight: '1.3', letterSpacing: '0.1em' }],
        sm: ['13px', { lineHeight: '1.5', letterSpacing: '0' }],
        base: ['15px', { lineHeight: '1.6', letterSpacing: '0' }],
        lg: ['17px', { lineHeight: '1.5', letterSpacing: '0' }],
        xl: ['20px', { lineHeight: '1.4', letterSpacing: '-0.01em' }],
        '2xl': ['24px', { lineHeight: '1.3', letterSpacing: '-0.01em' }],
        '3xl': ['30px', { lineHeight: '1.2', letterSpacing: '-0.02em' }],
        '4xl': ['36px', { lineHeight: '1.2', letterSpacing: '-0.02em' }],
      },

      // 8pt grid spacing
      spacing: {
        '0': '0px',
        '0.5': '2px',
        '1': '4px',
        '2': '8px',
        '3': '12px',
        '4': '16px',
        '5': '20px',
        '6': '24px',
        '8': '32px',
        '10': '40px',
        '12': '48px',
        '16': '64px',
        '20': '80px',
        '24': '96px',
      },

      borderRadius: {
        none: '0px',
        sm: '4px',      // Badges, chips
        DEFAULT: '6px', // Buttons, inputs
        md: '6px',
        lg: '8px',      // Cards, modals - MAX
        full: '50%',    // Avatars, circles
        // Note: No xl, 2xl, etc. - 8px is maximum
      },

      boxShadow: {
        // Light mode only - use sparingly
        sm: '0 1px 2px rgba(0, 0, 0, 0.04)',
        DEFAULT: '0 2px 4px rgba(0, 0, 0, 0.06)',
        md: '0 2px 4px rgba(0, 0, 0, 0.06)',
        lg: '0 4px 8px rgba(0, 0, 0, 0.08)',
        // No shadows in dark mode - use elevation colors
        none: 'none',
      },

      transitionDuration: {
        '0': '0ms',
        '100': '100ms',   // Fast - hover states
        '150': '150ms',   // Normal - most transitions
        '250': '250ms',   // Slow - modal open/close
        '350': '350ms',   // Slower - page transitions (MAX)
        // No durations > 350ms
      },

      transitionTimingFunction: {
        DEFAULT: 'cubic-bezier(0.25, 0, 0.25, 1)',
        'ease-out': 'cubic-bezier(0.25, 0, 0.25, 1)',
        'ease-in': 'cubic-bezier(0.4, 0, 1, 1)',
        'ease-in-out': 'cubic-bezier(0.4, 0, 0.25, 1)',
      },

      zIndex: {
        'dropdown': '100',
        'sticky': '200',
        'modal-backdrop': '300',
        'modal': '400',
        'popover': '500',
        'tooltip': '600',
        'toast': '700',
      },

      // Layout constraints
      maxWidth: {
        'modal-sm': '480px',
        'modal-md': '640px',
        'modal-lg': '800px',
        'container': '1280px',
      },

      width: {
        'sidebar': '240px',
        'sidebar-narrow': '200px',
      },

      height: {
        'header': '64px',
        'table-header': '48px',
        'table-row': '52px',
      },

      minHeight: {
        'touch': '44px',  // Minimum touch target
        'touch-lg': '48px',
      },
    },
  },
  plugins: [],
};
