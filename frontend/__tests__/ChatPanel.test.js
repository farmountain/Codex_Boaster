import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';

window.HTMLElement.prototype.scrollIntoView = jest.fn();
import ChatPanel from '../components/ChatPanel.tsx';
import axios from 'axios';

jest.mock('axios');
axios.post.mockResolvedValue({
  data: { response: 'ok', actions: [], reflexion_summary: 'sum' },
});

test('shows welcome message and sends chat', async () => {
  render(<ChatPanel />);
  expect(screen.getByText(/What would you like to build/)).toBeInTheDocument();
  fireEvent.change(screen.getByPlaceholderText(/Ask Codex/), { target: { value: 'Hi' } });
  fireEvent.keyDown(screen.getByPlaceholderText(/Ask Codex/), { key: 'Enter', code: 'Enter' });
  expect(axios.post).toHaveBeenCalled();
  await screen.findByText('ok');
});
