import { render, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import RuntimeSelector from '../components/RuntimeSelector.tsx'
import axios from 'axios'

jest.mock('axios')

test('submits selected runtime', async () => {
  axios.post.mockResolvedValue({ data: { message: 'ok' } })

  const { getByText } = render(<RuntimeSelector />)
  fireEvent.click(getByText(/Set Runtime/))

  expect(axios.post).toHaveBeenCalledWith('/api/config/runtime', { language: 'Python', version: '3.8' })
})
