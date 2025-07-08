'use client'
import { useState } from 'react'
import PromptEditor from '../../../components/ui/PromptEditor'
import OutputPanel from '../../../components/ui/OutputPanel'
import { api } from '../../../lib/api'

export default function ArchitectAgentPage() {
  const [goal, setGoal] = useState('')
  const [plan, setPlan] = useState('')

  async function runPlan() {
    const res = await api.plan({ goal })
    setPlan(JSON.stringify(res, null, 2))
  }

  return (
    <div className="p-4 space-y-4">
      <PromptEditor value={goal} onChange={setGoal} onSubmit={runPlan} />
      <OutputPanel title="Plan Output" content={plan} />
    </div>
  )
}
