'use client'
import { useAgentLog } from '../../lib/hooks'
import ConfidenceScore from '../ConfidenceScore'; // updated

export default function AgentLogPanel({ sessionId }: { sessionId: string }) {
  const logs = useAgentLog(sessionId)
  return (
    <div className="p-4 space-y-2 border rounded bg-white dark:bg-gray-800">
      <h3 className="font-semibold mb-2">Agent Logs</h3>
      {logs.map((log: any, idx: number) => (
        <div key={idx} className="text-sm border-b pb-2 last:border-none">
          <div className="flex justify-between">
            <span>
              <strong>{log.step}</strong> – {log.agent}
            </span>
            <ConfidenceScore score={log.confidence} />
          </div>
          <div className="text-xs text-gray-500">
            {new Date(log.timestamp).toLocaleString()}
          </div>
          <pre className="whitespace-pre-wrap text-xs mt-1">
            {log.reasoning || log.content}
          </pre>
        </div>
      ))}
      {logs.length === 0 && (
        <p className="text-sm text-gray-500">No logs found.</p>
      )}
    </div>
  )
}
