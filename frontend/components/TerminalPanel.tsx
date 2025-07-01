import { useState } from "react"

export default function TerminalPanel() {
  const [commands, setCommands] = useState(["npm install", "pytest"])
  const [logs, setLogs] = useState([])

  const runCommands = async () => {
    setLogs([])
    for (const cmd of commands) {
      const resp = await fetch('/api/run-setup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: cmd })
      })
      const data = await resp.json()
      setLogs(prev => [...prev, { command: cmd, ...data }])
    }
  }

  return (
    <div className="p-4">
      <h2 className="font-bold text-lg mb-2">Terminal Runner</h2>

      <textarea
        className="w-full p-2 border rounded text-sm"
        rows={4}
        value={commands.join("\n")}
        onChange={(e) => setCommands(e.target.value.split("\n"))}
      />

      <button
        className="mt-2 px-4 py-2 bg-blue-600 text-white rounded"
        onClick={runCommands}
      >
        Run Setup
      </button>

      <div className="mt-4 space-y-3">
        {logs.map((log, idx) => (
          <div
            key={idx}
            className={`p-2 border rounded text-sm ${log.exit_code === 0 ? "bg-green-100" : "bg-red-100"}`}
          >
            {log.command && (
              <div className="font-mono text-xs text-gray-500">{log.command}</div>
            )}
            {log.stdout && (
              <pre className="text-xs whitespace-pre-wrap">{log.stdout}</pre>
            )}
            {log.stderr && (
              <pre className="text-xs text-red-600">{log.stderr}</pre>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

