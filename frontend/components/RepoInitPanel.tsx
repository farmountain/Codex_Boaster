import { useState } from 'react';

export default function RepoInitPanel() {
  const [form, setForm] = useState({
    project_name: '',
    description: '',
    language: 'python',
    private: true,
    ci: 'github-actions',
  });
  const [message, setMessage] = useState('');

  async function handleSubmit() {
    const res = await fetch('/api/repo-init', {
      method: 'POST',
      body: JSON.stringify(form),
      headers: { 'Content-Type': 'application/json' },
    });
    const data = await res.json();
    setMessage(data.repo_url || data.error || data.detail);
  }

  return (
    <div className="p-4 border rounded shadow">
      <h2 className="text-xl font-bold mb-4">🗃️ Init New GitHub Repo</h2>
      {['project_name', 'description'].map(key => (
        <input
          key={key}
          className="mb-2 p-2 border w-full"
          placeholder={key}
          value={form[key]}
          onChange={e => setForm(prev => ({ ...prev, [key]: e.target.value }))}
        />
      ))}
      <select
        className="mb-2 p-2 border w-full"
        value={form.language}
        onChange={e => setForm(prev => ({ ...prev, language: e.target.value }))}
      >
        <option value="python">Python</option>
        <option value="node">Node.js</option>
      </select>
      <select
        className="mb-2 p-2 border w-full"
        value={form.ci}
        onChange={e => setForm(prev => ({ ...prev, ci: e.target.value }))}
      >
        <option value="github-actions">GitHub Actions</option>
        <option value="none">None</option>
      </select>
      <select
        className="mb-4 p-2 border w-full"
        value={form.private ? 'true' : 'false'}
        onChange={e =>
          setForm(prev => ({ ...prev, private: e.target.value === 'true' }))
        }
      >
        <option value="true">Private</option>
        <option value="false">Public</option>
      </select>
      <button onClick={handleSubmit} className="bg-blue-600 text-white px-4 py-2 rounded">
        🚀 Create Repository
      </button>
      {message && <p className="mt-4 text-green-600">{message}</p>}
    </div>
  );
}
