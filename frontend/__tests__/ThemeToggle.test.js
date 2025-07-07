import { render, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import ThemeToggle from '../components/ui/ThemeToggle.tsx'

test('toggles dark mode class', () => {
  const { getByRole } = render(<ThemeToggle />)
  const btn = getByRole('button')
  fireEvent.click(btn)
  expect(document.documentElement.classList.contains('dark')).toBe(true)
})
