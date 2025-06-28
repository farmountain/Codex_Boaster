import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import ConfidenceScore from '../components/ConfidenceScore.tsx'

test('shows percent and color', () => {
  render(<ConfidenceScore score={0.9} />)
  const el = screen.getByText(/Confidence: 90.0%/)
  expect(el).toBeInTheDocument()
  expect(el.className).toMatch(/bg-green-400/)
})
