import { useState } from 'react';

export default function ChatPanel() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! Ask me anything about your project.' }
  ]);
  const [input, setInput] = useState('');
  const [agent, setAgent] = useState('');

  async function sendMessage() {
    const newMsg = { role: 'user', content: input };
    const updated = [...messages, newMsg];
    setMessages(updated);
    setInput('');

    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: 'demo-session',
        messages: updated
      })
    });

    const data = await res.json();
    setMessages([...updated, { role: 'assistant', content: data.reply }]);
    setAgent(data.agent);
  }

  return (
    <div className="fixed bottom-0 right-0 w-96 bg-white border p-4 shadow-lg rounded-t-lg">
      <h2 className="font-bold text-blue-700 mb-2">🤖 Chat with Codex ({agent || 'Idle'})</h2>
      <div className="h-64 overflow-y-auto border p-2 mb-2 bg-gray-50 rounded">
        {messages.map((msg, i) => (
          <div key={i} className={`mb-2 text-${msg.role === 'user' ? 'right' : 'left'}`}>
            <p className={`inline-block p-2 rounded ${msg.role === 'user' ? 'bg-blue-200' : 'bg-gray-300'}`}>
              {msg.content}
            </p>
          </div>
        ))}
      </div>
      <input
        className="w-full border p-2 rounded"
        placeholder="Type your question..." value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && sendMessage()}
      />
    </div>
  );
}
