import { useEffect, useState } from "react"
import axios from "axios"

type EnvVar = { key: string; value: string; show?: boolean }

export default function EnvVarForm() {
  const [envVars, setEnvVars] = useState<EnvVar[]>([])
  const [original, setOriginal] = useState<EnvVar[]>([])
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState("")

  useEffect(() => {
    axios.get("/api/config/env").then(res => {
      const vars = res.data.map((v: EnvVar) => ({ ...v, show: false }))
      setEnvVars(vars)
      setOriginal(vars)
    })
  }, [])

  const handleChange = (index: number, field: keyof EnvVar, value: string) => {
    const updated = [...envVars]
    ;(updated[index] as any)[field] = value
    setEnvVars(updated)
  }

  const toggleShow = (index: number) => {
    const updated = [...envVars]
    updated[index].show = !updated[index].show
    setEnvVars(updated)
  }

  const addRow = () => {
    setEnvVars([...envVars, { key: "", value: "", show: false }])
  }

  const deleteRow = (index: number) => {
    setEnvVars(envVars.filter((_, i) => i !== index))
  }

  const save = async () => {
    setLoading(true)
    try {
      await axios.post("/api/config/env", {
        env: envVars.map(({ key, value }) => ({ key, value })),
      })
      setOriginal(envVars)
      setMessage("✅ Environment updated")
    } catch {
      setMessage("❌ Failed to save")
    } finally {
      setLoading(false)
    }
  }

  const changed = (idx: number) => {
    const o = original[idx]
    const n = envVars[idx]
    return !o || o.key !== n.key || o.value !== n.value
  }

  return (
    <div className="p-4 bg-white shadow rounded">
      <h2 className="text-lg font-semibold mb-2">Environment Variables</h2>

      {envVars.map((pair, idx) => (
        <div key={idx} className="flex gap-2 mb-2 items-center">
          <input
            className={`flex-1 border px-2 py-1 ${changed(idx) ? "border-blue-500" : ""}`}
            value={pair.key}
            onChange={e => handleChange(idx, "key", e.target.value)}
            placeholder="KEY"
          />
          <input
            className={`flex-1 border px-2 py-1 ${changed(idx) ? "border-blue-500" : ""}`}
            type={pair.show ? "text" : "password"}
            value={pair.value}
            onChange={e => handleChange(idx, "value", e.target.value)}
            placeholder="VALUE"
          />
          <button onClick={() => toggleShow(idx)} className="text-sm">{pair.show ? "🙈" : "👁"}</button>
          <button onClick={() => deleteRow(idx)} className="text-red-500">🗑</button>
        </div>
      ))}

      <div className="flex gap-4 mt-4">
        <button onClick={addRow} className="bg-gray-600 text-white px-3 py-1 rounded">+ Add</button>
        <button onClick={save} className="bg-blue-600 text-white px-4 py-1 rounded" disabled={loading}>
          {loading ? "Saving..." : "Save"}
        </button>
      </div>

      {message && <p className="text-sm mt-2 text-gray-700">{message}</p>}
    </div>
  )
}
