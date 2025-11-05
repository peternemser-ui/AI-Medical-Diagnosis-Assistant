const typography = require('@tailwindcss/typography')

module.exports = {
  darkMode: 'class', // Enable class-based dark mode
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif']
      },
      colors: {
        bg: "var(--bg)",
        surface: "var(--surface)",
        "surface-2": "var(--surface-2)",
        "surface-lighter": "var(--surface-lighter)",
        text: "var(--text)",
        "text-muted": "var(--text-muted)",
        border: "var(--border)",
        primary: {
          DEFAULT: "var(--primary)",
          600: "var(--primary-600)",
        },
        "on-primary": "var(--on-primary)",
        accent: {
          DEFAULT: "var(--accent)",
          600: "var(--accent-600)",
        },
        "on-accent": "var(--on-accent)",
        info: "var(--info)",
        success: "var(--success)",
        warning: "var(--warning)",
        danger: "var(--danger)",
        link: {
          DEFAULT: "var(--link)",
          hover: "var(--link-hover)",
        },
        bubble: "var(--bubble)",
        "on-bubble": "var(--on-bubble)",
        focus: "var(--focus)",
      },
      borderRadius: {
        DEFAULT: "var(--radius)",
      },
      boxShadow: {
        xs: "var(--shadow-xs)",
        sm: "var(--shadow-sm)",
        md: "var(--shadow-md)",
        lg: "var(--shadow-lg)",
        xl: "var(--shadow-xl)",
      }
    }
  },
  plugins: [typography]
}
