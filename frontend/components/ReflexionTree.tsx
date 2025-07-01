import { useEffect, useState } from "react"
import axios from "axios"

export type TraceNode = {
  version: string
  agent: string
  step: string
  content: string
  confidence: number
  timestamp: string
}

export default function ReflexionTree({ sessionId }: { sessionId: string }) {
  const [trace, setTrace] = useState<TraceNode[]>([])
  const [selected, setSelected] = useState<TraceNode | null>(null)

  useEffect(() => {
    axios.get(`/api/hipcortex/logs?session_id=${sessionId}`)
      .then(res => setTrace(res.data || []))
  }, [sessionId])

  return (
    <div className="p-4">
      <h2 className="text-lg font-bold mb-2">🧠 AUREUS Reasoning Tree</h2>

      <div className="space-y-2">
        {trace.map((node) => (
          <div
            key={node.version}
            className={`p-2 border rounded cursor-pointer shadow-sm ${
              node.confidence < 0.8 ? "border-yellow-400" : "border-gray-300"
            }`}
            onClick={() => setSelected(node)}
          >
            <div className="flex justify-between text-sm">
              <span><strong>{node.version}</strong> – {node.agent}: {node.step}</span>
              <span className={`px-2 rounded text-xs ${node.confidence < 0.8 ? "bg-yellow-200" : "bg-green-200"}`}>
                {Math.round(node.confidence * 100)}%
              </span>
            </div>
            <div className="text-xs text-gray-500">{new Date(node.timestamp).toLocaleString()}</div>
            <div className="text-sm mt-1 text-gray-800 line-clamp-2">{node.content}</div>
          </div>
        ))}
      </div>

      {selected && (
        <div className="mt-6 border-t pt-4">
          <h3 className="font-semibold text-sm mb-1">🧩 Full Reasoning ({selected.version})</h3>
          <p className="text-sm whitespace-pre-wrap">{selected.content}</p>
        </div>
      )}
    </div>
  )
}
