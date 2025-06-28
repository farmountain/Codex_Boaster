import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ReasoningPanel from '../components/ReasoningPanel.tsx';

test('renders reflexion steps with details', () => {
  const plan = {
    steps: [
      { step: 'Fix bug', why: 'error trace', fix: 'add try/except', confidence: 8 }
    ]
  };
  render(<ReasoningPanel plan={plan} />);
  expect(screen.getByText(/Fix bug/)).toBeInTheDocument();
  expect(screen.getByText(/error trace/)).toBeInTheDocument();
  expect(screen.getByText(/add try\/except/)).toBeInTheDocument();
});
