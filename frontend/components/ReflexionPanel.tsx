import { useEffect, useState } from "react"
import ConfidenceScore from "./ConfidenceScore"

export default function ReflexionPanel() {
  const [logs, setLogs] = useState([])

  useEffect(() => {
    fetch("/api/reflexion/logs")
      .then(res => res.json())
      .then(setLogs)
  }, [])

  return (
    <div className="p-4 space-y-4">
      <h2 className="text-xl font-bold">Reflexion History</h2>
      {logs.map((log, index) => (
        <div key={index} className="p-3 border rounded shadow">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-500">{log.timestamp}</span>
            <ConfidenceScore score={log.confidence} />
          </div>
          <div className="mt-2 text-sm font-medium text-blue-800">{log.suggestion}</div>
          <div className="text-sm text-gray-600 mt-1">{log.log}</div>
        </div>
      ))}
    </div>
  )
}
