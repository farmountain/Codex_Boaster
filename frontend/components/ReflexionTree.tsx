import { useEffect, useState } from "react"
import axios from "axios"

export type TraceNode = {
  version: string
  agent: string
  step: string
  content: string
  confidence: number
  timestamp: string
  attempt?: number
  justification?: string
  children?: TraceNode[]
}

export default function ReflexionTree({
  sessionId,
  steps,
}: {
  sessionId?: string
  steps?: TraceNode[]
}) {
  const [trace, setTrace] = useState<TraceNode[]>([])
  const [selected, setSelected] = useState<TraceNode | null>(null)
  const [compare, setCompare] = useState(false)

  useEffect(() => {
    if (steps && steps.length > 0) {
      setTrace(steps)
      return
    }
    if (sessionId) {
      axios
        .get(`/api/hipcortex/logs?session_id=${sessionId}`)
        .then((res) => setTrace(res.data || []))
    }
  }, [sessionId, steps])

  const renderNode = (node: TraceNode) => (
    <div key={node.version} className="ml-4">
      <div
        className={`p-2 border rounded cursor-pointer shadow-sm ${
          node.confidence < 0.8 ? 'border-yellow-400' : 'border-gray-300'
        }`}
        onClick={() => setSelected(node)}
      >
        <div className="flex justify-between text-sm">
          <span>
            <strong>{node.version}</strong>{' '}
            {node.attempt !== undefined && (
              <span className="text-purple-700">Retry {node.attempt}</span>
            )}{' '}
            – {node.agent}: {node.step}
          </span>
          <span
            className={`px-2 rounded text-xs ${
              node.confidence < 0.8 ? 'bg-yellow-200' : 'bg-green-200'
            }`}
          >
            {Math.round(node.confidence * 100)}%
          </span>
        </div>
        <div className="text-xs text-gray-500">
          {new Date(node.timestamp).toLocaleString()}
        </div>
        <div className="text-xs text-gray-600">{node.justification}</div>
        <div className="text-sm mt-1 text-gray-800 line-clamp-2">
          {node.content}
        </div>
      </div>
      {node.children && node.children.map((c) => renderNode(c))}
    </div>
  )

  return (
    <div className="p-4">
      <h2 className="text-lg font-bold mb-2">🧠 AUREUS Reasoning Tree</h2>

      <div className="space-y-2">
        {trace.map((node) => renderNode(node))}
      </div>

      {selected && (
        <div className="mt-6 border-t pt-4">
          <h3 className="font-semibold text-sm mb-1">🧩 Full Reasoning ({selected.version})</h3>
          <p className="text-sm whitespace-pre-wrap">{selected.content}</p>
          {compare && trace.length > 1 && (
            <pre className="mt-2 p-2 bg-gray-50 text-xs whitespace-pre-wrap">
              {trace[trace.length - 2].content}
              {'\n---\n'}
              {trace[trace.length - 1].content}
            </pre>
          )}
          <button className="mt-2 text-xs underline" onClick={() => setCompare(!compare)}>
            {compare ? 'Hide Comparison' : 'Compare Last Two'}
          </button>
        </div>
      )}
    </div>
  )
}
