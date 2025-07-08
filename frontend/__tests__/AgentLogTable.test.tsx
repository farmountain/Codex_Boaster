import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import AgentLogTable from '../components/tables/AgentLogTable'

test('renders mock log rows', () => {
  render(<AgentLogTable />)
  expect(screen.getByText('architect')).toBeInTheDocument()
  expect(screen.getByText('tester')).toBeInTheDocument()
})
