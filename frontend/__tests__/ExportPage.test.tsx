import { render, fireEvent, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import ExportPage from '../app/export/page'

// jsdom does not implement createObjectURL
// @ts-ignore
global.URL.createObjectURL = jest.fn(() => 'blob://test')

global.fetch = jest.fn(() =>
  Promise.resolve({ ok: true, blob: () => Promise.resolve(new Blob(['a'])) })
) as jest.Mock

test('calls export endpoint and shows link', async () => {
  render(<ExportPage />)
  fireEvent.click(screen.getByText('Export Frontend'))
  expect(fetch).toHaveBeenCalledWith('/export/frontend')
  await screen.findByText('Download Zip')
})
