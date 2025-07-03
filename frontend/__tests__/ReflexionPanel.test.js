import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import ReflexionPanel from '../components/ReflexionPanel.tsx'

test('displays fetched logs in order', async () => {
  const logs = [
    { timestamp: 't1', version: 'v1', confidence: 0.5, diff: 'd1', reflexion_classification: 'why' },
    { timestamp: 't2', version: 'v2', confidence: 0.9, diff: 'd2' }
  ]
  global.fetch = jest.fn(() => Promise.resolve({ json: () => Promise.resolve(logs) }))
  render(<ReflexionPanel />)
  expect(fetch).toHaveBeenCalled()
  const first = await screen.findByText('d1')
  const items = screen.getAllByText(/d1|d2/)
  expect(items[0]).toBe(first)
  expect(items.length).toBe(2)
  expect(document.querySelector('svg')).toBeInTheDocument()
})
