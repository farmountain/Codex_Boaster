import { useState, useEffect } from "react"
import TerminalPanel from "./TerminalPanel"

export default function RuntimeSelector() {
  const [config, setConfig] = useState({
    python: "3.10",
    node: "18",
    go: "1.19"
  })

  useEffect(() => {
    fetch("/api/runtime-config")
      .then(res => res.json())
      .then(setConfig)
  }, [])

  const saveConfig = async () => {
    const res = await fetch("/api/runtime-config", {
      method: "POST",
      body: JSON.stringify(config),
      headers: { "Content-Type": "application/json" }
    })
    const data = await res.json()
    alert(data.message)
  }

  return (
    <div className="p-6 border rounded shadow">
      <h2 className="text-xl font-bold mb-4">Runtime Environment Setup</h2>
      <div className="space-y-4">
        {["python", "node", "go"].map((lang) => (
          <div key={lang} className="flex items-center space-x-4">
            <label className="w-24 capitalize">{lang}</label>
            <input
              type="text"
              value={config[lang]}
              onChange={(e) => setConfig({ ...config, [lang]: e.target.value })}
              className="border px-2 py-1 rounded w-32"
            />
          </div>
        ))}
      </div>
      <button
        onClick={saveConfig}
        className="mt-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Save Configuration
      </button>
      <div className="mt-6">
        <TerminalPanel />
      </div>
    </div>
  )
}
