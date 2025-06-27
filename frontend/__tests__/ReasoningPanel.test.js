import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ReasoningPanel from '../components/ReasoningPanel.tsx';

global.fetch = jest.fn(() =>
  Promise.resolve({ ok: true, json: () => Promise.resolve({ suggestion: 'try' }) })
);

test('shows improvement suggestion', async () => {
  render(<ReasoningPanel />);
  const text = await screen.findByText(/try/);
  expect(text).toBeInTheDocument();
});
