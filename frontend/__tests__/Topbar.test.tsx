import { render } from '@testing-library/react'
import '@testing-library/jest-dom'
import Topbar from '../components/layout/Topbar'

test('shows user name and API key status', () => {
  const { getByText } = render(<Topbar userName="Alice" apiKeyPresent />)
  expect(getByText('Alice')).toBeInTheDocument()
  expect(getByText('API Key')).toBeInTheDocument()
})
