'use client'
import { useState } from 'react'
import { callAgent } from '../../lib/api'

export default function ExportPage() {
  const [path, setPath] = useState('')
  const [result, setResult] = useState('')
  async function runExport() {
    const res = await callAgent('/export', { path })
    setResult(JSON.stringify(res))
  }
  return (
    <div className="p-4 space-y-4">
      <input value={path} onChange={e=>setPath(e.target.value)} className="border p-2 w-full" placeholder="Artifact path" />
      <button className="px-3 py-1 bg-blue-600 text-white rounded" onClick={runExport}>Export</button>
      <pre>{result}</pre>
    </div>
  )
}
