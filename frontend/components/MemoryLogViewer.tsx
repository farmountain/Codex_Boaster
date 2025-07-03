import { useEffect, useState } from "react";
import ConfidenceScore from "./ConfidenceScore";

export type MemoryLog = {
  step: string;
  agent: string;
  reasoning?: string;
  content?: string;
  confidence: number;
  timestamp: string;
  [key: string]: any;
};

export default function MemoryLogViewer({ sessionId }: { sessionId: string }) {
  const [logs, setLogs] = useState<MemoryLog[]>([]);
  const [raw, setRaw] = useState(false);
  const [agentFilter, setAgentFilter] = useState("");
  const [confFilter, setConfFilter] = useState(0);
  const [keyword, setKeyword] = useState("");

  useEffect(() => {
    fetch(`/api/hipcortex/memory-log?session_id=${sessionId}`)
      .then(res => res.json())
      .then(data => setLogs(data));
  }, [sessionId]);

  const filtered = logs.filter(l =>
    (!agentFilter || l.agent.includes(agentFilter)) &&
    l.confidence >= confFilter &&
    (!keyword || (l.reasoning || l.content || "").toLowerCase().includes(keyword.toLowerCase()))
  );

  const exportData = (type: "json" | "md") => {
    const data = type === "json" ? JSON.stringify(filtered, null, 2) : filtered.map(l => `- **${l.step}** (${l.agent}) - ${l.reasoning || l.content}`).join("\n");
    const blob = new Blob([data], { type: type === "json" ? "application/json" : "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `memory_log.${type}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="p-4 space-y-3">
      <div className="flex gap-2 items-center text-xs">
        <input className="border px-1 py-0.5 rounded" placeholder="Agent" value={agentFilter} onChange={e => setAgentFilter(e.target.value)} />
        <input className="border px-1 py-0.5 rounded" type="number" step="0.1" min="0" max="1" placeholder="Min conf" value={confFilter} onChange={e => setConfFilter(parseFloat(e.target.value) || 0)} />
        <input className="border px-1 py-0.5 rounded" placeholder="Keyword" value={keyword} onChange={e => setKeyword(e.target.value)} />
        <button className="px-2 py-1 bg-gray-200 rounded" onClick={() => setRaw(!raw)}>{raw ? "Formatted" : "Raw JSON"}</button>
        <button className="px-2 py-1 bg-gray-200 rounded" onClick={() => exportData("md")}>Export MD</button>
        <button className="px-2 py-1 bg-gray-200 rounded" onClick={() => exportData("json")}>Export JSON</button>
      </div>
      {filtered.map((log, idx) => (
        raw ? (
          <pre key={idx} className="bg-gray-100 p-2 text-xs overflow-auto">{JSON.stringify(log, null, 2)}</pre>
        ) : (
          <div key={idx} className="mb-2 p-3 border rounded bg-gray-100">
            <div className="font-bold">{log.step} — {log.agent}</div>
            <div className="text-xs text-gray-600">{new Date(log.timestamp).toLocaleString()}</div>
            <div className="mt-1 text-sm">{log.reasoning || log.content}</div>
            <ConfidenceScore score={log.confidence} />
          </div>
        )
      ))}
    </div>
  );
}
