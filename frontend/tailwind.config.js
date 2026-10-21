/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'slate-900': '#0F172A',
        'emerald-500': '#10B981',
        slate: {
          850: '#151F32',
          900: '#0F172A',
          950: '#020617',
        },
        emerald: {
          400: '#34D399',
          500: '#10B981',
          600: '#059669',
        },
        cluster: {
          civil: '#3B82F6',
          regulatory: '#10B981',
          defense: '#F59E0B',
          state: '#8B5CF6',
          psu: '#EC4899',
        },
        depth: {
          foundation: '#94A3B8',
          intermediate: '#3B82F6',
          advanced: '#8B5CF6',
          analytical: '#EC4899',
        },
      },
      fontFamily: {
        sans: [
          'Inter',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'sans-serif',
        ],
      },
    },
  },
  plugins: [],
};
