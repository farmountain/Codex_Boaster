import { useState } from 'react'
import { SignedIn, SignedOut, SignInButton } from '@clerk/nextjs'
import CodeEditor from '../components/CodeEditor'
import ReasoningPanel from '../components/ReasoningPanel'
import UsageMeter from '../components/UsageMeter'
import TestMatrix from '../components/TestMatrix'
import TestResultPanel from '../components/TestResultPanel'
import ChatPanel from '../components/ChatPanel'
import ThemeToggle from '../components/ui/ThemeToggle'
import AgentCard from '../components/ui/AgentCard'
import PromptEditor from '../components/ui/PromptEditor'
import OutputPanel from '../components/ui/OutputPanel'
import { callAgent } from '../lib/api'

const clerkEnabled = !!process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;

export default function Dashboard() {
  const [tests, setTests] = useState('')
  const [code, setCode] = useState('')
  const [output, setOutput] = useState('')
  const [prompt, setPrompt] = useState('')
  const [plan, setPlan] = useState({ steps: [] })
  const [testResult, setTestResult] = useState<{
    success?: boolean;
    stdout?: string;
    stderr?: string;
  }>({});

  async function handlePlanSubmit() {
    const data = await callAgent('/plan', { prompt })
    setPlan({ steps: data.modules || [] })
  }

  async function build() {
    const data = await callAgent('/build', { tests })
    setCode(data.code)
  }

  async function runTest() {
    const data = await callAgent('/test', { runtime: 'python' })
    setTestResult(data)
  }

  const content = (
    <div className="flex h-screen">
      <aside className="w-56 p-4 space-y-2 border-r bg-gray-50 dark:bg-gray-900">
        <div className="flex justify-between items-center mb-4">
          <h1 className="font-bold">Codex Booster</h1>
          <ThemeToggle />
        </div>
        <AgentCard name="Plan" onClick={handlePlanSubmit} />
        <AgentCard name="Build" onClick={build} />
        <AgentCard name="Test" onClick={runTest} />
        <a href="/configure-env" className="text-blue-600 underline text-sm block">
          Configure
        </a>
        <UsageMeter />
      </aside>
      <main className="flex-1 p-4 space-y-4 overflow-auto">
        <PromptEditor value={prompt} onChange={setPrompt} />
        <CodeEditor code={code} onChange={setCode} />
        <textarea
          className="w-full h-32 border p-2"
          value={tests}
          onChange={e => setTests(e.target.value)}
          placeholder="Write tests here"
        />
        <OutputPanel title="Agent Output" content={output} />
        <ReasoningPanel plan={plan} />
        {typeof testResult.success !== 'undefined' && (
          <TestResultPanel stdout={testResult.stdout} stderr={testResult.stderr} />
        )}
        <ChatPanel />
      </main>
    </div>
  );

  return (
    <div>
      {clerkEnabled ? (
        <>
          <SignedOut>
            <p>Please <SignInButton /></p>
          </SignedOut>
          <SignedIn>{content}</SignedIn>
        </>
      ) : (
        content
      )}
    </div>
  );
}
