import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ReflexionTree from '../components/ReflexionTree.tsx';

test('renders reasoning trace tree', () => {
  const steps = [
    { step: 'Investigate', why: 'failure', fix: 'check db', confidence: 7 }
  ];
  render(<ReflexionTree steps={steps} />);
  expect(screen.getByText(/Investigate/)).toBeInTheDocument();
  expect(screen.getByText(/check db/)).toBeInTheDocument();
});
