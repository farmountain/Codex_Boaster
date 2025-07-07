'use client'
import { useState } from 'react'
import { callAgent } from '../../lib/api'

type Props = { command: string }

export default function TerminalRunner({ command }: Props) {
  const [result, setResult] = useState('')
  async function run() {
    if (!command) return
    const res = await callAgent('/api/run-setup', { command, cwd: './' })
    setResult(res.stdout + res.stderr)
  }
  return (
    <div>
      <button className="px-3 py-1 bg-gray-800 text-white rounded" onClick={run}>Run</button>
      <pre className="mt-2 p-2 bg-black text-green-300 h-48 overflow-auto">{result}</pre>
    </div>
  )
}
