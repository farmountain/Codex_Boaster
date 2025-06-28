import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import RepoInitPanel from '../components/RepoInitPanel.tsx';

global.fetch = jest.fn(() =>
  Promise.resolve({ json: () => Promise.resolve({ message: 'Repo created' }) })
);

test('renders all fields and submits form', async () => {
  render(<RepoInitPanel />);
  ['github_token', 'github_user', 'repo_name', 'description'].forEach((p) => {
    expect(screen.getByPlaceholderText(p)).toBeInTheDocument();
  });
  fireEvent.click(screen.getByText(/Create Repository/));
  expect(fetch).toHaveBeenCalled();
  await screen.findByText('Repo created');
});
