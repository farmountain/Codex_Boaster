import { useState } from "react"
import axios from "axios"

export default function TerminalPanel() {
  const [command, setCommand] = useState("pytest -q")
  const [output, setOutput] = useState("")
  const [stderr, setStderr] = useState("")
  const [exitCode, setExitCode] = useState(null)
  const [loading, setLoading] = useState(false)
  const [logId, setLogId] = useState("")

  const runCommand = async () => {
    setLoading(true)
    setOutput("")
    setStderr("")
    setExitCode(null)
    try {
      const res = await axios.post("/api/run-setup", {
        command,
        cwd: "./workspace",
        env: {}
      })
      setOutput(res.data.stdout)
      setStderr(res.data.stderr)
      setExitCode(res.data.exit_code)
      setLogId(res.data.log_id)
    } catch (err) {
      setStderr("Error running command.")
    } finally {
      setLoading(false)
    }
  }

  const downloadLog = () => {
    if (logId) {
      window.open(`/logs/runtime/${logId}.log`, "_blank")
    }
  }

  return (
    <div className="bg-black text-white font-mono p-4 rounded shadow-md h-[400px] flex flex-col">
      <div className="mb-2 flex items-center gap-2">
        <input
          className="flex-1 bg-gray-900 border border-gray-700 px-2 py-1 rounded"
          value={command}
          onChange={e => setCommand(e.target.value)}
          disabled={loading}
        />
        <button
          onClick={runCommand}
          disabled={loading}
          className="bg-green-600 px-4 py-1 rounded text-white"
        >
          {loading ? "Running..." : "Run"}
        </button>
        {logId && (
          <button
            onClick={downloadLog}
            className="bg-gray-700 px-3 py-1 rounded text-white"
          >
            Download Log
          </button>
        )}
      </div>

      <div className="flex-1 bg-gray-800 p-2 rounded overflow-auto text-sm whitespace-pre-wrap">
        {output && <pre className="text-green-300">{output}</pre>}
        {stderr && <pre className="text-red-400">{stderr}</pre>}
      </div>

      <div className="mt-2 text-xs text-gray-400">
        Exit Code: {exitCode} | Log ID: {logId}
      </div>
    </div>
  )
}

