import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import ReflexionPanel from '../components/ReflexionPanel.tsx'

test('displays fetched logs in order', async () => {
  const logs = [
    { timestamp: 't1', agent: 'Ref', confidence: 0.5, suggestion: 'first', log: 'L1' },
    { timestamp: 't2', agent: 'Ref', confidence: 0.9, suggestion: 'second', log: 'L2' }
  ]
  global.fetch = jest.fn(() => Promise.resolve({ json: () => Promise.resolve(logs) }))
  render(<ReflexionPanel />)
  expect(fetch).toHaveBeenCalled()
  const first = await screen.findByText('first')
  const items = screen.getAllByText(/first|second/)
  expect(items[0]).toBe(first)
  expect(items.length).toBe(2)
})
