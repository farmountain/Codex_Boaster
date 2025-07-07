import { render } from '@testing-library/react'
import '@testing-library/jest-dom'
import LoginPage from '../app/(auth)/login/page'

jest.mock('@clerk/nextjs', () => ({
  SignIn: () => <div>Sign In Component</div>
}))

test('renders sign in component', () => {
  const { getByText } = render(<LoginPage />)
  expect(getByText('Sign In Component')).toBeInTheDocument()
})
