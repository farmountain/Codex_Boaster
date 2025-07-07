import { render, fireEvent, act } from '@testing-library/react'
import '@testing-library/jest-dom'
import RuntimeSelector from '../components/RuntimeSelector.tsx'
import axios from 'axios'

jest.mock('axios')


test('saves runtime config', async () => {
  axios.get.mockResolvedValue({ data: {} })
  axios.post.mockResolvedValue({ data: { message: 'ok' } })
  const { getByText } = render(<RuntimeSelector />)
  await act(async () => {
    fireEvent.click(getByText(/Save/))
  })
  expect(axios.post).toHaveBeenCalledWith('/runtime-config', expect.any(Object))
})
