import { render, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import RuntimeSelector from '../components/RuntimeSelector.tsx';

test('selects version and triggers onChange', () => {
  const onChange = jest.fn();
  const { getAllByRole } = render(<RuntimeSelector onChange={onChange} />);
  const selects = getAllByRole('combobox');
  fireEvent.change(selects[0], { target: { value: '3.12' } });
  expect(onChange).toHaveBeenCalledWith('python', '3.12');
});
