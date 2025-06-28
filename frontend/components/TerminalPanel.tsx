import { useState } from "react"

export default function TerminalPanel() {
  const [commands, setCommands] = useState(["npm install", "pytest"])
  const [logs, setLogs] = useState([])

  const runCommands = () => {
    const ws = new WebSocket("ws://localhost:8000/ws/run-setup")
    ws.onopen = () => {
      ws.send(JSON.stringify({ commands }))
    }
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setLogs((prev) => [...prev, data])
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
            className={`p-2 border rounded text-sm ${log.status === "error" ? "bg-red-100" : log.status ? "bg-green-100" : ""}`}
          >
            {log.command && (
              <div className="font-mono text-xs text-gray-500">{log.command}</div>
            )}
            {log.output && (
              <pre className="text-xs whitespace-pre-wrap">{log.output}</pre>
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

