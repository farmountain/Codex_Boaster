import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import PlanSelector from '../components/PlanSelector.jsx';

global.fetch = jest.fn(() =>
  Promise.resolve({ ok: true, json: () => Promise.resolve({}) })
);

test('renders plan buttons', () => {
  render(<PlanSelector />);
  expect(screen.getByText(/Basic/)).toBeInTheDocument();
});

test('calls charge endpoint on click', async () => {
  render(<PlanSelector />);
  fireEvent.click(screen.getByText(/Basic/));
  expect(fetch).toHaveBeenCalled();
});
