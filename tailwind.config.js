const colors = require('tailwindcss/colors');

/**
 * Merged config for all portfolio pages. Each page previously carried its own
 * inline `tailwind.config` via the Play CDN; those are consolidated here so a
 * single precompiled stylesheet (assets/tailwind.css) serves the whole site.
 *
 * Collision note: `amber`, `blue`, `violet`, `cyan` shadow Tailwind's default
 * scales. Some pages use the bare token (e.g. `bg-amber` = #f5a623) while
 * Fluent uses the numbered defaults (`bg-amber-500`). Defining each as
 * `{ ...colors.x, DEFAULT }` keeps BOTH working.
 */
module.exports = {
  content: ['./*.html'],
  theme: {
    extend: {
      fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] },
      colors: {
        base: '#0b0a0a',
        card: '#141210',
        panel: '#16120e',
        header: '#171717',
        accent: '#ffd8e4',
        brown: '#ac7f5e',
        ink: '#131418',        // only Fluent uses this (from-ink gradients)
        paper: '#F4EFE8',
        crimson: '#A51C30',
        fluentBlue: '#2453E6',
        fluentCyan: '#00A3E0',
        talent: '#4f7cff',
        primary: '#2f6bff',
        leader: '#f5a623',
        company: '#16b364',
        finance: '#7c5cff',
        cHigh: '#16A34A',
        cMed: '#D97706',
        cLow: '#DC2626',
        amber: { ...colors.amber, DEFAULT: '#f5a623' },
        blue: { ...colors.blue, DEFAULT: '#3B82F6' },
        violet: { ...colors.violet, DEFAULT: '#8b5cf6' },
        cyan: { ...colors.cyan, DEFAULT: '#38d3ee' },
        // Light-theme palettes (homepage). Numbered 1 (lightest) → 10 (darkest).
        grey: { 1: '#e8e8e8', 2: '#c7c7c7', 3: '#9b9b9b', 4: '#6d6d6d', 5: '#414141', 6: '#171717', 7: '#141414', 8: '#101010', 9: '#0d0d0d', 10: '#0a0a0a' },
        royal: { 1: '#f1f1fe', 2: '#dedefd', 3: '#c4c5fc', 4: '#a9a9fa', 5: '#8f8ff8', 6: '#7677f7', 7: '#6465d2', 8: '#5454af', 9: '#43448d', 10: '#35366f' },
      },
    },
  },
};
