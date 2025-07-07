'use client'
import { useState } from 'react'
import { api } from '../../lib/api'

export default function ExportPage() {
  const [result, setResult] = useState('')
  async function runExport() {
    const blob = await api.exportZip()
    const url = URL.createObjectURL(blob)
    setResult(url)
  }
  return (
    <div className="p-4 space-y-4">
      <button className="px-3 py-1 bg-blue-600 text-white rounded" onClick={runExport}>Export Frontend</button>
      {result && (
        <a href={result} download="frontend.zip" className="text-blue-600 underline">
          Download Zip
        </a>
      )}
    </div>
  )
}
