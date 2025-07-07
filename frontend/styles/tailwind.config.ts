import type { Config } from 'tailwindcss'
import tokens from './tokens.json'

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}', './pages/**/*.{ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: tokens.colors,
      spacing: tokens.spacing,
      borderRadius: {
        '2xl': '1rem',
      },
      boxShadow: {
        soft: '0 2px 4px rgba(0,0,0,0.05)',
      },
    },
  },
  plugins: [],
}
export default config
