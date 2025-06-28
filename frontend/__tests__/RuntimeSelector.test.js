import { render, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import RuntimeSelector from '../components/RuntimeSelector.tsx';

test('loads and saves runtime config', async () => {
  const fetchMock = jest.fn()
    .mockResolvedValueOnce({ json: () => Promise.resolve({ python: '3.10', node: '18', go: '1.19' }) })
    .mockResolvedValueOnce({ json: () => Promise.resolve({ message: 'Runtime config saved.' }) });

  global.fetch = fetchMock;

  const { getByText, getByDisplayValue } = render(<RuntimeSelector />);
  await waitFor(() => getByDisplayValue('3.10'));

  fireEvent.change(getByDisplayValue('3.10'), { target: { value: '3.11' } });
  fireEvent.click(getByText(/Save Configuration/));

  expect(fetchMock).toHaveBeenCalledTimes(2);
  expect(fetchMock.mock.calls[1][0]).toBe('/api/runtime-config');
});
