'use client'
import { useState } from 'react'
import AgentCard from '../../components/ui/AgentCard'
import PromptEditor from '../../components/ui/PromptEditor'
import OutputPanel from '../../components/ui/OutputPanel'
import ChatPanel from '../../components/ui/ChatPanel'
import { callAgent } from '../../lib/api'

export default function DashboardPage() {
  const [prompt, setPrompt] = useState('')
  const [tests, setTests] = useState('')
  const [output, setOutput] = useState('')

  async function runPlan() {
    const res = await callAgent('/plan', { goal: prompt })
    setOutput(JSON.stringify(res, null, 2))
  }

  async function runBuild() {
    const res = await callAgent('/build', { tests })
    setOutput(JSON.stringify(res, null, 2))
  }

  async function runTests() {
    const res = await callAgent('/test', { code: '', tests })
    setOutput(JSON.stringify(res, null, 2))
  }

  return (
    <div className="flex h-[90vh]">
      <aside className="w-60 border-r p-4 space-y-4 overflow-y-auto">
        <AgentCard name="Plan" onClick={runPlan} />
        <AgentCard name="Build" onClick={runBuild} />
        <AgentCard name="Test" onClick={runTests} />
      </aside>
      <main className="flex-1 p-4 space-y-4 overflow-y-auto">
        <PromptEditor value={prompt} onChange={setPrompt} />
        <textarea className="w-full h-32 border p-2" value={tests} onChange={e=>setTests(e.target.value)} placeholder="Write tests here" />
        <OutputPanel title="Output" content={output} />
        <ChatPanel />
      </main>
    </div>
  )
}
