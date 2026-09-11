/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#FAF8F3',      // Warm half-white background
        surface: '#FFFFFF',         // Card & panel surface
        'surface-subtle': '#F5EFE6', // Subtle container beige
        'soft-beige': '#E8DDCC',    // Soft beige accent
        'light-beige': '#F2EBDD',   // Light beige border/tint
        taupe: '#A89B8A',          // Warm taupe
        'text-main': '#26231F',     // Dark slate text
        'text-muted': '#716A60',    // Secondary body text
        'border-warm': '#DDD5C8',   // Thin warm border
        // Accents for decision states
        'decision-auto': '#3B6E52',     // Forest sage green (restrained)
        'decision-auto-bg': '#EAF3ED',  // Tinted auto-handle background
        'decision-esc': '#9E4A3B',      // Terracotta brick (restrained, non-alarming)
        'decision-esc-bg': '#FDF1EE',   // Tinted escalation background
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        serif: ['Newsreader', 'Georgia', 'serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      boxShadow: {
        'subtle': '0 1px 3px rgba(38, 35, 31, 0.04), 0 1px 2px rgba(38, 35, 31, 0.02)',
        'elevated': '0 4px 12px rgba(38, 35, 31, 0.06), 0 1px 3px rgba(38, 35, 31, 0.03)',
      }
    },
  },
  plugins: [],
}
