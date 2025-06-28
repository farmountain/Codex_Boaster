import { useState } from 'react';
import { SignedIn, SignedOut, SignInButton } from '@clerk/nextjs';
import CodeEditor from '../components/CodeEditor';
import ReasoningPanel from '../components/ReasoningPanel';
import UsageMeter from '../components/UsageMeter';

export default function Dashboard() {
  const [tests, setTests] = useState('');
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [prompt, setPrompt] = useState('');
  const [plan, setPlan] = useState([]);
  const [reasoning, setReasoning] = useState('');

  async function handlePlanSubmit() {
    const res = await fetch('/api/architect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt })
    });
    const data = await res.json();
    setPlan(data.modules);
    setReasoning(data.reasoning);
  }

  async function build() {
    const res = await fetch('http://localhost:8000/build', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tests })
    });
    const data = await res.json();
    setCode(data.code);
  }

  async function run() {
    const res = await fetch('http://localhost:8000/test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, tests })
    });
    const data = await res.json();
    setOutput(data.output || '');
  }

  return (
    <div>
      <SignedOut>
        <p>Please <SignInButton /></p>
      </SignedOut>
      <SignedIn>
        <h1>Dashboard</h1>
        <UsageMeter />
        <input
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Project idea"
          className="border p-1 mr-2"
        />
        <button onClick={handlePlanSubmit}>Plan</button>
        <button onClick={build}>Build</button>
        <button onClick={run}>Test</button>
        <div style={{ marginTop: '1rem' }}>
          <CodeEditor code={code} onChange={setCode} />
        </div>
        <textarea
          style={{ width: '100%', height: '120px', marginTop: '1rem' }}
          value={tests}
          onChange={(e) => setTests(e.target.value)}
          placeholder="Write tests here"
        />
        <pre>{output}</pre>
        <ReasoningPanel reasoning={reasoning} plan={plan} />
      </SignedIn>
    </div>
  );
}
