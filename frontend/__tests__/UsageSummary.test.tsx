import { render, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import UsageSummary from '../components/cards/UsageSummary'
import * as api from '../lib/api'

test('displays usage info', async () => {
  jest.spyOn(api, 'getUsage').mockResolvedValue({ daily: 2, by_agent: { builder: 1 } })
  render(<UsageSummary />)
  await waitFor(() => screen.getByText(/Daily Calls/))
  expect(screen.getByText(/Daily Calls:\s*2/)).toBeInTheDocument()
  expect(screen.getByText('builder')).toBeInTheDocument()
})
