import { render, fireEvent, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import DeployPanel from '../components/DeployPanel.tsx'
import axios from 'axios'

jest.mock('axios')

test('renders deploy form and submits request', async () => {
axios.post.mockResolvedValue({ data: { status: 'success', deployment_url: 'url', logs_url: 'log', message: 'ok' } })
axios.get.mockResolvedValue({ data: { status: 'success', logs: 'done' } })

  render(<DeployPanel />)
  fireEvent.change(screen.getByPlaceholderText('Project Name'), { target: { value: 'demo' } })
  fireEvent.change(screen.getByPlaceholderText('GitHub Repo URL'), { target: { value: 'http://repo' } })
fireEvent.click(screen.getByRole('button', { name: /Deploy Now/ }))

  expect(axios.post).toHaveBeenCalledWith('/api/deploy', {
    project_name: 'demo',
    repo_url: 'http://repo',
    provider: 'vercel',
    framework: 'nextjs'
  })
await screen.findByText(/Deployment Triggered/)
await screen.findByText('done')
});
