import { useState } from 'react';

export default function DocViewer({ docs }: { docs: Record<string, string> }) {
  const [active, setActive] = useState('README.md');

  return (
    <div className="p-4 bg-white shadow rounded">
      <h2 className="text-xl font-bold mb-4">📚 Project Documentation</h2>
      <div className="flex space-x-4 mb-4">
        {Object.keys(docs).map((doc) => (
          <button
            key={doc}
            className={`px-3 py-1 rounded ${active === doc ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
            onClick={() => setActive(doc)}
          >
            {doc}
          </button>
        ))}
      </div>
      <pre className="whitespace-pre-wrap text-sm bg-gray-50 p-4 rounded">
        {docs[active]}
      </pre>
    </div>
  );
}
