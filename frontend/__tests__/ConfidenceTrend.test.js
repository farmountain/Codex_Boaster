import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import ConfidenceTrend from '../components/ConfidenceTrend.tsx'

test('renders svg line', () => {
  render(<ConfidenceTrend scores={[0.2, 0.8]} />)
  const svg = document.querySelector('svg')
  expect(svg).toBeInTheDocument()
  expect(svg.querySelector('polyline')).toBeInTheDocument()
})
