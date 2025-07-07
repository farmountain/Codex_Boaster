import { render } from '@testing-library/react'
import '@testing-library/jest-dom'
import Sidebar from '../components/layout/Sidebar'

test('renders navigation items', () => {
  const { getByText } = render(<Sidebar />)
  expect(getByText('Dashboard')).toBeInTheDocument()
  expect(getByText('Build')).toBeInTheDocument()
})
