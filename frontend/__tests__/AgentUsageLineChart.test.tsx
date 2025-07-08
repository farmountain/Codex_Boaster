import { render } from '@testing-library/react'
import '@testing-library/jest-dom'
import AgentUsageLineChart from '../components/charts/AgentUsageLineChart'

test('renders svg polyline', () => {
  const { container } = render(<AgentUsageLineChart data={[{ day: 'Mon', count: 1 }, { day: 'Tue', count: 2 }]} />)
  const poly = container.querySelector('polyline')
  expect(poly).toBeInTheDocument()
})
