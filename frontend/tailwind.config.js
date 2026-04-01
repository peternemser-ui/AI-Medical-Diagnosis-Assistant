const typography = require('@tailwindcss/typography')

module.exports = {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },

      /* ── Typography scale ────────────────────────────────── */
      fontSize: {
        'micro':  ['0.5rem',   { lineHeight: '0.75rem' }],   // 8px  — pill microcopy
        'tiny':   ['0.5625rem',{ lineHeight: '0.875rem' }],   // 9px  — dense metadata
        'detail': ['0.625rem', { lineHeight: '1rem' }],        // 10px — labels, badges
        'caption':['0.6875rem',{ lineHeight: '1rem' }],        // 11px — helper text
        'body-sm':['0.8125rem',{ lineHeight: '1.25rem' }],     // 13px — compact body
        'body':   ['0.875rem', { lineHeight: '1.375rem' }],    // 14px — standard body
        'body-lg':['0.9375rem',{ lineHeight: '1.5rem' }],      // 15px — comfortable body
        'subhead':['1rem',     { lineHeight: '1.5rem' }],      // 16px — subsection title
        'title':  ['1.125rem', { lineHeight: '1.625rem' }],    // 18px — section title
        'heading':['1.25rem',  { lineHeight: '1.75rem' }],     // 20px — page heading
        'display':['1.5rem',   { lineHeight: '2rem' }],        // 24px — hero/display
        'hero':   ['2rem',     { lineHeight: '2.5rem' }],      // 32px — landing hero
      },

      /* ── Semantic colors ─────────────────────────────────── */
      colors: {
        // Brand
        brand: {
          50:  '#ecfdf5',
          100: '#d1fae5',
          200: '#a7f3d0',
          300: '#6ee7b7',
          400: '#34d399',
          500: '#10b981',  // primary brand — emerald
          600: '#059669',
          700: '#047857',
        },
        // Clinical semantic
        clinical: {
          bg:       'var(--clinical-bg)',
          surface:  'var(--clinical-surface)',
          elevated: 'var(--clinical-elevated)',
          border:   'var(--clinical-border)',
          divider:  'var(--clinical-divider)',
        },
        // Urgency
        urgency: {
          routine:   '#10b981', // emerald
          moderate:  '#f59e0b', // amber
          urgent:    '#f97316', // orange
          emergency: '#ef4444', // red
          critical:  '#dc2626', // red-600
        },
        // Confidence scale
        confidence: {
          high:   '#10b981',
          medium: '#3b82f6',
          low:    '#f59e0b',
          poor:   '#ef4444',
        },
        // Status
        status: {
          pass:    '#10b981',
          warning: '#f59e0b',
          danger:  '#ef4444',
          info:    '#3b82f6',
          muted:   '#64748b',
        },
      },

      /* ── Shadow hierarchy ────────────────────────────────── */
      boxShadow: {
        'xs':       '0 1px 2px 0 rgb(0 0 0 / 0.03)',
        'subtle':   '0 1px 3px 0 rgb(0 0 0 / 0.04), 0 1px 2px -1px rgb(0 0 0 / 0.04)',
        'card':     '0 2px 8px -2px rgb(0 0 0 / 0.06), 0 1px 3px -1px rgb(0 0 0 / 0.04)',
        'elevated': '0 4px 16px -4px rgb(0 0 0 / 0.08), 0 2px 6px -2px rgb(0 0 0 / 0.04)',
        'panel':    '0 8px 30px -6px rgb(0 0 0 / 0.12), 0 4px 12px -4px rgb(0 0 0 / 0.06)',
        'modal':    '0 16px 48px -8px rgb(0 0 0 / 0.16), 0 8px 24px -6px rgb(0 0 0 / 0.08)',
        // Dark mode variants
        'card-dark':     '0 2px 8px -2px rgb(0 0 0 / 0.3), 0 1px 3px -1px rgb(0 0 0 / 0.2)',
        'elevated-dark': '0 4px 16px -4px rgb(0 0 0 / 0.4), 0 2px 6px -2px rgb(0 0 0 / 0.2)',
        'panel-dark':    '0 8px 30px -6px rgb(0 0 0 / 0.5), 0 4px 12px -4px rgb(0 0 0 / 0.3)',
        // Glow accents
        'glow-brand':  '0 0 16px -2px rgb(16 185 129 / 0.15)',
        'glow-blue':   '0 0 16px -2px rgb(59 130 246 / 0.15)',
        'glow-danger':  '0 0 16px -2px rgb(239 68 68 / 0.15)',
      },

      /* ── Border radius system ────────────────────────────── */
      borderRadius: {
        'pill':   '9999px',  // chips, badges, pills
        'btn':    '0.625rem', // 10px — buttons
        'input':  '0.75rem',  // 12px — inputs, selects
        'card':   '0.875rem', // 14px — standard cards
        'panel':  '1rem',     // 16px — large panels, modals
        'section':'1.25rem',  // 20px — page sections
      },

      /* ── Spacing tokens ──────────────────────────────────── */
      spacing: {
        'card-px':    '1.25rem',  // 20px — card horizontal padding
        'card-py':    '1rem',     // 16px — card vertical padding
        'section-gap':'1.5rem',   // 24px — gap between sections
        'page-px':    '1.5rem',   // 24px — page horizontal padding
        'page-py':    '2rem',     // 32px — page vertical padding
      },

      /* ── Animations ──────────────────────────────────────── */
      animation: {
        'shimmer':    'shimmer 2s infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow':       'glow 2s ease-in-out infinite alternate',
        'fade-in':    'fadeIn 0.2s ease-out',
        'slide-up':   'slideUp 0.25s ease-out',
        'slide-down': 'slideDown 0.2s ease-out',
        'slide-right':'slideRight 0.25s ease-out',
        'scale-in':   'scaleIn 0.15s ease-out',
      },
      keyframes: {
        shimmer: {
          '0%':   { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
        glow: {
          '0%':   { boxShadow: '0 0 5px rgba(59, 130, 246, 0.2)' },
          '100%': { boxShadow: '0 0 20px rgba(59, 130, 246, 0.4)' },
        },
        fadeIn: {
          '0%':   { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%':   { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideDown: {
          '0%':   { opacity: '0', transform: 'translateY(-8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideRight: {
          '0%':   { opacity: '0', transform: 'translateX(-8px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        scaleIn: {
          '0%':   { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
      },
    }
  },
  plugins: [typography]
}
