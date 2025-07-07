import type { Config } from 'tailwindcss'
import tokens from './styles/tokens.json'

const { colors, spacing, fonts } = tokens as any

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}', './pages/**/*.{ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        ...colors,
      },
      spacing: {
        ...spacing,
      },
      fontFamily: {
        base: [fonts.base],
      },
      borderRadius: {
        '2xl': '1rem',
      },
      boxShadow: {
        magic: '0 2px 8px rgba(0,0,0,0.1)',
        soft: '0 2px 4px rgba(0,0,0,0.05)'
      },
    },
  },
  plugins: [],
}
export default config
