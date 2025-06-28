import { useState } from 'react';

export default function BuildPanel({ onFilesGenerated }) {
  const [input, setInput] = useState({
    file_name: '',
    purpose: '',
    language: 'python',
    context: '',
  });

  async function handleBuild() {
    const res = await fetch('/api/builder', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify([input]),
    });
    const data = await res.json();
    if (onFilesGenerated) onFilesGenerated(data.files);
  }

  return (
    <div className="p-4 border rounded">
      <h2 className="text-xl font-bold mb-4">🛠️ Build Code</h2>
      <input
        className="input"
        placeholder="File name (e.g., main.py)"
        value={input.file_name}
        onChange={(e) => setInput((prev) => ({ ...prev, file_name: e.target.value }))}
      />
      <input
        className="input mt-2"
        placeholder="What should this file do?"
        value={input.purpose}
        onChange={(e) => setInput((prev) => ({ ...prev, purpose: e.target.value }))}
      />
      <textarea
        className="textarea mt-2"
        rows={5}
        placeholder="Additional context..."
        value={input.context}
        onChange={(e) => setInput((prev) => ({ ...prev, context: e.target.value }))}
      />
      <button
        onClick={handleBuild}
        className="mt-4 bg-blue-600 text-white px-4 py-2 rounded"
      >
        Generate Code
      </button>
    </div>
  );
}
