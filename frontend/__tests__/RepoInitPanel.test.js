import { render, fireEvent, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import RepoInitPanel from '../components/RepoInitPanel.tsx'
import axios from 'axios'

jest.mock('axios')

test('renders all fields and submits form', async () => {
  axios.post.mockResolvedValue({ data: { repo_url: 'Repo created', ci_setup: 'github-actions' } })

  render(<RepoInitPanel />)

  expect(screen.getByPlaceholderText('Project Name')).toBeInTheDocument()
  expect(screen.getByPlaceholderText('Project Description')).toBeInTheDocument()

  fireEvent.click(screen.getByText(/Create Repository/))
  expect(axios.post).toHaveBeenCalledWith('/api/repo-init', expect.any(Object))
  await screen.findByText('Repo created')
})
