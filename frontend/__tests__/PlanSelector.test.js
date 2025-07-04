import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import PlanSelector from '../components/PlanSelector.jsx';

global.fetch = jest.fn(() =>
  Promise.resolve({ ok: true, json: () => Promise.resolve({ checkout_url: '/' }) })
);

test('renders plan options', () => {
  render(<PlanSelector />);
  expect(screen.getByText(/starter Plan/i)).toBeInTheDocument();
});

test('calls charge endpoint on continue', async () => {
  render(<PlanSelector />);
  fireEvent.click(screen.getByText(/Continue to Checkout/));
  expect(fetch).toHaveBeenCalled();
});

test('uses NEXT_PUBLIC_API_BASE_URL if set', () => {
  process.env.NEXT_PUBLIC_API_BASE_URL = 'http://api.test';
  render(<PlanSelector />);
  fireEvent.click(screen.getByText('Basic - $10'));
  expect(fetch).toHaveBeenCalledWith(
    'http://api.test/charge',
    expect.any(Object)
  );
  delete process.env.NEXT_PUBLIC_API_BASE_URL;
});
