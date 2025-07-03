import { useEffect, useState } from "react";
import ConfidenceScore from "./ConfidenceScore";
import ConfidenceTrend from "./ConfidenceTrend";
import MemoryLogViewer from "./MemoryLogViewer";

export default function ReflexionPanel() {
  const [logs, setLogs] = useState([]);
  const [pendingRetry, setPendingRetry] = useState<any | null>(null);
  const [decision, setDecision] = useState<string | null>(null);
  const [tab, setTab] = useState<'history' | 'memory'>('history');

  useEffect(() => {
    fetch("/api/hipcortex/logs?session_id=demo-session")
      .then(res => res.json())
      .then(data => {
        setLogs(data);
        const last = data[data.length - 1];
        if (last && last.type === 'retry') setPendingRetry(last);
      });
  }, []);

  return (
    <div className="p-4 space-y-4">
      <div className="flex space-x-2">
        <button
          className={`px-3 py-1 rounded text-sm ${tab === 'history' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
          onClick={() => setTab('history')}
        >
          History
        </button>
        <button
          className={`px-3 py-1 rounded text-sm ${tab === 'memory' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
          onClick={() => setTab('memory')}
        >
          Memory Log
        </button>
      </div>

      {tab === 'history' && (
        <div className="space-y-4">
          <h2 className="text-xl font-bold">Reflexion History</h2>
          <ConfidenceTrend scores={logs.map(l => l.confidence)} />
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
          {pendingRetry && !decision && (
            <div className="p-3 border rounded bg-yellow-50">
              <p className="text-sm">Retry attempt {pendingRetry.attempt} suggested: {pendingRetry.justification}</p>
              <div className="space-x-2 mt-2">
                <button className="px-2 py-1 bg-green-600 text-white text-xs rounded" onClick={() => setDecision('approved')}>
                  Approve Retry
                </button>
                <button className="px-2 py-1 bg-red-600 text-white text-xs rounded" onClick={() => setDecision('aborted')}>
                  Abort
                </button>
              </div>
            </div>
          )}
          {decision && (
            <div className="text-xs text-gray-600">User decision: {decision}</div>
          )}
        </div>
      )}

      {tab === 'memory' && (
        <MemoryLogViewer sessionId="demo-session" />
      )}
    </div>
  );
}
