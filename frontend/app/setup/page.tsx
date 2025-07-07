'use client'
import { useState } from 'react'
import TerminalRunner from '../../components/ui/TerminalRunner'

export default function SetupPage() {
  const [cmd, setCmd] = useState('')
  return (
    <div className="p-4 space-y-4">
      <input value={cmd} onChange={e=>setCmd(e.target.value)} className="border p-2 w-full" placeholder="Command" />
      <TerminalRunner command={cmd} />
    </div>
  )
}
