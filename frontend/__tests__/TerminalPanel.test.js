import { render, fireEvent, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import TerminalPanel from '../components/TerminalPanel.tsx'
import axios from 'axios'

jest.mock('axios')

test('displays command output', async () => {
  axios.post.mockResolvedValue({ data: { stdout: 'hi', stderr: '', exit_code: 0, log_id: '1' } })

  render(<TerminalPanel />)
  fireEvent.click(screen.getByText(/Run/))
  expect(axios.post).toHaveBeenCalled()
  await screen.findByText('hi')
})
