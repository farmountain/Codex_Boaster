"use client"
import { useState } from "react"
import AgentCard from "../../components/ui/AgentCard"
import PromptEditor from "../../components/ui/PromptEditor"
import OutputPanel from "../../components/ui/OutputPanel"
import ChatPanel from "../../components/ui/ChatPanel"
import ReflexionTreePage from "./reflexion-tree"
import { callAgent } from "../../lib/api"
import { useAgentStatus } from "../../lib/hooks"

export default function DashboardPage() {
  const [prompt, setPrompt] = useState("")
  const [logs, setLogs] = useState("")
  const [reason, setReason] = useState("")
  const status = useAgentStatus()

  async function runWorkflow() {
    setLogs("")
    setReason("")

    const plan = await callAgent("/plan", { goal: prompt })
    setLogs((l) => l + "Plan\n" + JSON.stringify(plan, null, 2) + "\n\n")

    const build = await callAgent("/build", { tests: prompt })
    setLogs((l) => l + "Build\n" + JSON.stringify(build, null, 2) + "\n\n")

    const test = await callAgent("/test", { code: build.code || "", tests: prompt })
    setLogs((l) => l + "Test\n" + JSON.stringify(test, null, 2) + "\n\n")

    const reflect = await callAgent("/reflect", { feedback: JSON.stringify(test) })
    setReason(JSON.stringify(reflect, null, 2))
  }

  return (
    <div className="h-screen md:flex" style={{ backgroundColor: "#f8fafc" }}>
      <aside className="md:w-60 w-full md:border-r p-4 space-y-4 overflow-y-auto bg-[#fdf6f6]">
        <AgentCard name="Plan" status={status?.plan} />
        <AgentCard name="Build" status={status?.build} />
        <AgentCard name="Test" status={status?.test} />
        <AgentCard name="Reflect" status={status?.reflect} />
      </aside>
      <main className="flex-1 md:grid md:grid-cols-2 h-full overflow-hidden">
        <div className="p-4 space-y-4 overflow-auto">
          <PromptEditor value={prompt} onChange={setPrompt} onSubmit={runWorkflow} />
          <OutputPanel title="Logs" content={logs} />
        </div>
        <div className="p-4 space-y-4 border-t md:border-l overflow-auto bg-[#fefefe]">
          <OutputPanel title="Reason Trace" content={reason} />
          <ReflexionTreePage />
        </div>
        <ChatPanel />
      </main>
    </div>
  )
}
