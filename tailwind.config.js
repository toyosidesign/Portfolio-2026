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
      },
    },
  },
};
