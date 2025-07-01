import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatPanel from '../components/ChatPanel.tsx';

global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({ response: 'ok', actions: [], reflexion_summary: 'sum' })
  })
);

test('shows welcome message and sends chat', async () => {
  render(<ChatPanel />);
  expect(screen.getByText(/Ask me anything/)).toBeInTheDocument();
  fireEvent.change(screen.getByPlaceholderText(/Type your question/), { target: { value: 'Hi' } });
  fireEvent.keyDown(screen.getByPlaceholderText(/Type your question/), { key: 'Enter', code: 'Enter' });
  expect(fetch).toHaveBeenCalled();
  await screen.findByText('ok');
});
