import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import DeployPanel from '../components/DeployPanel.tsx';

global.fetch = jest.fn(() =>
  Promise.resolve({ json: () => Promise.resolve({ status: 'success', output: '' }) })
);

test('renders deploy form and submits request', async () => {
  render(<DeployPanel />);
  fireEvent.change(screen.getByPlaceholderText('Project name'), { target: { value: 'demo' } });
  fireEvent.change(screen.getByPlaceholderText('Deploy token'), { target: { value: 'tok' } });
  fireEvent.click(screen.getByText(/Deploy Now/));
  expect(fetch).toHaveBeenCalled();
  await screen.findByText(/Status/);
});

