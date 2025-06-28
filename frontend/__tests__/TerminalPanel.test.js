import { render, fireEvent, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import TerminalPanel from '../components/TerminalPanel.tsx'

test('displays websocket logs', async () => {
  const wsMock = {
    send: jest.fn(),
    close: jest.fn(),
    onopen: null,
    onmessage: null
  }
  global.WebSocket = jest.fn(() => wsMock)
  render(<TerminalPanel />)
  fireEvent.click(screen.getByText(/Run Setup/))
  wsMock.onopen && wsMock.onopen()
  const msg = { command: 'echo hi', status: 'success' }
  wsMock.onmessage && wsMock.onmessage({ data: JSON.stringify(msg) })
  expect(await screen.findByText('echo hi')).toBeInTheDocument()
})

