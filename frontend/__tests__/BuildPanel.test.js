import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import BuildPanel from '../components/BuildPanel.tsx';

const files = [{ file_name: 'main.py', language: 'python', content: 'print(1)' }];

global.fetch = jest.fn(() =>
  Promise.resolve({ json: () => Promise.resolve({ files }) })
);

test('submits build request and returns files', async () => {
  const handler = jest.fn();
  render(<BuildPanel onFilesGenerated={handler} />);
  fireEvent.change(screen.getByPlaceholderText(/File name/), { target: { value: 'main.py' } });
  fireEvent.change(screen.getByPlaceholderText(/What should this file do/), { target: { value: 'test' } });
  fireEvent.click(screen.getByText(/Generate Code/));
  expect(fetch).toHaveBeenCalled();
  await screen.findByText(/Generate Code/);
  expect(handler).toHaveBeenCalledWith(files);
});
