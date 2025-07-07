import { render, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import AgentCard from '../components/ui/AgentCard.tsx'

test('calls onClick when clicked', () => {
  const handler = jest.fn()
  const { getByText } = render(<AgentCard name="Builder" onClick={handler} />)
  fireEvent.click(getByText('Builder'))
  expect(handler).toHaveBeenCalled()
})
