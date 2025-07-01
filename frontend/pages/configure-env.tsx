import { useState } from 'react'
import RuntimeSelector from '../components/RuntimeSelector'
import EnvVarForm from '../components/EnvVarForm'
import SetupPreview from '../components/SetupPreview'

export default function ConfigPage() {
  const [setupScript, setSetupScript] = useState([
    'npm install',
    'pip install -r requirements.txt',
  ]);

  async function handleSubmit() {
    await fetch('/api/configure-env', {
      method: 'POST',
      body: JSON.stringify({
        setup_script: setupScript,
      }),
      headers: { 'Content-Type': 'application/json' },
    })
  }

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold">Configure Environment</h1>
      <RuntimeSelector />
      <EnvVarForm />
      <textarea
        className="border p-2 w-full"
        value={setupScript.join('\n')}
        onChange={e => setSetupScript(e.target.value.split('\n'))}
        placeholder="Setup script commands"
      />
      <SetupPreview setupScript={setupScript} />
      <button onClick={handleSubmit} className="px-4 py-2 bg-blue-500 text-white rounded">
        Save
      </button>
    </div>
  );
}
