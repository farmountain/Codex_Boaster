import { useState } from 'react';

export default function DeployPanel() {
  const [form, setForm] = useState({
    provider: 'vercel',
    framework: 'nextjs',
    project_name: '',
    repo_url: '',
  });
  const [result, setResult] = useState(null);

  async function handleDeploy() {
    const res = await fetch('/api/deploy', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
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

      <input
        className="input mt-2"
        placeholder="Repository URL"
        value={form.repo_url}
        onChange={(e) => setForm((prev) => ({ ...prev, repo_url: e.target.value }))}
      />

      <select
        className="input mt-2"
        value={form.framework}
        onChange={(e) => setForm((prev) => ({ ...prev, framework: e.target.value }))}
      >
        <option value="nextjs">Next.js</option>
        <option value="node">Node.js</option>
        <option value="python">Python</option>
      </select>

      <select
        className="input mt-2"
        value={form.provider}
        onChange={(e) => setForm((prev) => ({ ...prev, provider: e.target.value }))}
      >
        <option value="vercel">Vercel</option>
        <option value="fly">Fly.io</option>
      </select>

      <button className="mt-4 bg-blue-600 text-white px-4 py-2 rounded" onClick={handleDeploy}>
        Deploy Now
      </button>

      {result && (
        <div className="mt-4 bg-gray-100 p-2 rounded">
          <p className="font-semibold">Status: {result.status}</p>
          {result.deployment_url && (
            <p className="text-sm">Preview: <a className="text-blue-600" href={result.deployment_url}>{result.deployment_url}</a></p>
          )}
          {result.logs_url && (
            <p className="text-sm">Logs: <a className="text-blue-600" href={result.logs_url}>{result.logs_url}</a></p>
          )}
          {result.message && <p className="text-xs mt-1">{result.message}</p>}
        </div>
      )}
    </div>
  );
}
