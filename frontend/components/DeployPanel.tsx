import { useState } from 'react';

export default function DeployPanel() {
  const [form, setForm] = useState({
    platform: 'vercel',
    runtime: 'node',
    project_name: '',
    token: '',
  });
  const [result, setResult] = useState(null);

  async function handleDeploy() {
    const res = await fetch('/api/deploy', {
      method: 'POST',
      body: JSON.stringify(form),
      headers: { 'Content-Type': 'application/json' },
    });
    const data = await res.json();
    setResult(data);
  }

  return (
    <div className="p-4 border rounded bg-white shadow">
      <h2 className="text-xl font-bold mb-4">🚀 Deploy Project</h2>

      <input
        className="input"
        placeholder="Project name"
        value={form.project_name}
        onChange={(e) => setForm((prev) => ({ ...prev, project_name: e.target.value }))}
      />

      <select
        className="input mt-2"
        value={form.runtime}
        onChange={(e) => setForm((prev) => ({ ...prev, runtime: e.target.value }))}
      >
        <option value="node">Node.js</option>
        <option value="python">Python</option>
        <option value="nextjs">Next.js</option>
      </select>

      <select
        className="input mt-2"
        value={form.platform}
        onChange={(e) => setForm((prev) => ({ ...prev, platform: e.target.value }))}
      >
        <option value="vercel">Vercel</option>
        <option value="render">Render</option>
      </select>

      <input
        className="input mt-2"
        placeholder="Deploy token"
        value={form.token}
        onChange={(e) => setForm((prev) => ({ ...prev, token: e.target.value }))}
      />

      <button className="mt-4 bg-blue-600 text-white px-4 py-2 rounded" onClick={handleDeploy}>
        Deploy Now
      </button>

      {result && (
        <div className="mt-4 bg-gray-100 p-2 rounded">
          <p className="font-semibold">Status: {result.status}</p>
          <pre className="text-sm text-green-600">{result.output}</pre>
          {result.error && <pre className="text-sm text-red-500 mt-2">Error: {result.error}</pre>}
        </div>
      )}
    </div>
  );
}

