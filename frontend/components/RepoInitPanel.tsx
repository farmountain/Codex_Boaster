import { useState } from 'react';

export default function RepoInitPanel() {
  const [form, setForm] = useState({
    github_token: '',
    github_user: '',
    repo_name: '',
    description: '',
    visibility: 'private',
    template: 'node',
  });
  const [message, setMessage] = useState('');

  async function handleSubmit() {
    const res = await fetch('/api/repo-init', {
      method: 'POST',
      body: JSON.stringify(form),
      headers: { 'Content-Type': 'application/json' },
    });
    const data = await res.json();
    setMessage(data.message || data.error);
  }

  return (
    <div className="p-4 border rounded shadow">
      <h2 className="text-xl font-bold mb-4">🗃️ Init New GitHub Repo</h2>
      {['github_token', 'github_user', 'repo_name', 'description'].map(key => (
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
        value={form.template}
        onChange={e => setForm(prev => ({ ...prev, template: e.target.value }))}
      >
        <option value="default">Default</option>
        <option value="node">Node.js</option>
        <option value="python">Python</option>
      </select>
      <select
        className="mb-4 p-2 border w-full"
        value={form.visibility}
        onChange={e => setForm(prev => ({ ...prev, visibility: e.target.value }))}
      >
        <option value="private">Private</option>
        <option value="public">Public</option>
      </select>
      <button onClick={handleSubmit} className="bg-blue-600 text-white px-4 py-2 rounded">
        🚀 Create Repository
      </button>
      {message && <p className="mt-4 text-green-600">{message}</p>}
    </div>
  );
}
