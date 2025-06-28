import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import PlanSelector from '../components/PlanSelector.tsx';

global.fetch = jest.fn(() =>
  Promise.resolve({ ok: true, json: () => Promise.resolve({ checkout_url: '/' }) })
);

test('renders plan options', () => {
  render(<PlanSelector userId="1" email="t@example.com" />);
  expect(screen.getByText(/starter Plan/i)).toBeInTheDocument();
});

test('calls charge endpoint on continue', async () => {
  render(<PlanSelector userId="1" email="t@example.com" />);
  fireEvent.click(screen.getByText(/Continue to Checkout/));
  expect(fetch).toHaveBeenCalled();
});
