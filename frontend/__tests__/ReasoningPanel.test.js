import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ReasoningPanel from '../components/ReasoningPanel.tsx';

test('renders reasoning panel with modules', () => {
  render(
    <ReasoningPanel
      reasoning="This is a test."
      plan={[{ name: 'Auth', description: 'OAuth 2.0 setup' }]}
    />
  );
  expect(screen.getByText('Auth')).toBeInTheDocument();
  expect(screen.getByText(/OAuth 2\.0 setup/)).toBeInTheDocument();
});
