import { render } from '@testing-library/react'
import '@testing-library/jest-dom'
import RegisterPage from '../app/(auth)/register/page'

jest.mock('@clerk/nextjs', () => ({
  SignUp: () => <div>Sign Up Component</div>
}))

jest.mock('../components/PlanSelector', () => () => <div>Plan Selector</div>)

test('renders sign up and plan selector', () => {
  const { getByText } = render(<RegisterPage />)
  expect(getByText('Sign Up Component')).toBeInTheDocument()
  expect(getByText('Plan Selector')).toBeInTheDocument()
})
