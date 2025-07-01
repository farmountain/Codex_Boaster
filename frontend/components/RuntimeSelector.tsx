import { useState } from "react"
import axios from "axios"

const runtimeOptions = {
  Python: ["3.8", "3.10", "3.11"],
  Node: ["16", "18", "20"],
  Rust: ["1.70", "1.71", "1.72"],
}

export default function RuntimeSelector() {
  const [language, setLanguage] = useState("Python")
  const [version, setVersion] = useState(runtimeOptions["Python"][0])
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState("")

  const handleSubmit = async () => {
    setLoading(true)
    try {
      const res = await axios.post("/api/config/runtime", { language, version })
      setMessage(`Runtime set to ${language} ${version}`)
    } catch (e) {
      setMessage("Failed to update runtime")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-4 rounded border bg-white shadow-md">
      <h2 className="text-lg font-semibold mb-2">Runtime Selector</h2>

      <div className="mb-4">
        <label className="block mb-1">Language:</label>
        <select
          value={language}
          onChange={(e) => {
            const lang = e.target.value
            setLanguage(lang)
            setVersion(runtimeOptions[lang][0])
          }}
          className="border p-2 w-full"
        >
          {Object.keys(runtimeOptions).map((lang) => (
            <option key={lang}>{lang}</option>
          ))}
        </select>
      </div>

      <div className="mb-4">
        <label className="block mb-1">Version:</label>
        <select
          value={version}
          onChange={(e) => setVersion(e.target.value)}
          className="border p-2 w-full"
        >
          {runtimeOptions[language].map((v) => (
            <option key={v}>{v}</option>
          ))}
        </select>
      </div>

      <button
        onClick={handleSubmit}
        className="bg-blue-600 text-white px-4 py-2 rounded"
        disabled={loading}
      >
        {loading ? "Saving..." : "Set Runtime"}
      </button>

      {message && <p className="mt-2 text-sm text-gray-700">{message}</p>}
    </div>
  )
}
