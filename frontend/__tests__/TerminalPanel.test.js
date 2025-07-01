import { render, fireEvent, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import TerminalPanel from '../components/TerminalPanel.tsx'

test('displays command output', async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({ stdout: 'hi', stderr: '', exit_code: 0, log_id: '1' })
    })
  )

  render(<TerminalPanel />)
  fireEvent.click(screen.getByText(/Run Setup/))
  expect(fetch).toHaveBeenCalled()
  const outputs = await screen.findAllByText('hi')
  expect(outputs.length).toBeGreaterThan(0)
})
