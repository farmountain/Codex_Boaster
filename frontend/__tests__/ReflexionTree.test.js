import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ReflexionTree from '../components/ReflexionTree.tsx';

test('renders reasoning trace tree', () => {
  const steps = [
    {
      version: '1',
      agent: 'tester',
      step: 'Investigate',
      content: 'check db',
      confidence: 0.9,
      timestamp: new Date().toISOString(),
    },
  ];
  render(<ReflexionTree steps={steps} />);
  expect(screen.getByText(/Investigate/)).toBeInTheDocument();
  expect(screen.getByText(/check db/)).toBeInTheDocument();
});
