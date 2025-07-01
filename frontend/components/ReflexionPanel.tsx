import { useEffect, useState } from "react";
import ConfidenceScore from "./ConfidenceScore";

export default function ReflexionPanel() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    fetch("/api/hipcortex/logs?session_id=demo-session")
      .then(res => res.json())
      .then(setLogs);
  }, []);

  return (
    <div className="p-4 space-y-4">
      <h2 className="text-xl font-bold">Reflexion History</h2>
      {logs.map((log, index) => (
        <div key={index} className="p-3 border rounded shadow">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-500">{log.timestamp} ({log.version})</span>
            <ConfidenceScore score={log.confidence} />
          </div>
          {log.reflexion_classification && (
            <div className="text-xs text-purple-700 mt-1">{log.reflexion_classification}</div>
          )}
          <pre className="text-xs bg-gray-50 p-2 mt-2 whitespace-pre-wrap">{log.diff}</pre>
        </div>
      ))}
    </div>
  );
}
