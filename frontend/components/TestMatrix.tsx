import { useEffect, useState } from "react"
import axios from "axios"

type UATScenario = {
  title: string
  steps: string[]
  expected: string
}

export default function TestMatrix() {
  const [unitTests, setUnitTests] = useState<Record<string, string>>({})
  const [sitTests, setSitTests] = useState<Record<string, string>>({})
  const [uatScenarios, setUatScenarios] = useState<UATScenario[]>([])
  const [tab, setTab] = useState<"unit" | "sit" | "uat">("unit")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  useEffect(() => {
    fetchTests()
  }, [])

  const fetchTests = async () => {
    setLoading(true)
    setError("")
    try {
      const res = await axios.post("/api/test-suite", {
        business_description: "Users can log in and edit their profile",
        language: "python",
        framework: "pytest",
      })
      setUnitTests(res.data.unit_tests || {})
      setSitTests(res.data.sit_tests || {})
      setUatScenarios(res.data.uat_scenarios || [])
    } catch (e) {
      setError("Failed to generate tests")
    } finally {
      setLoading(false)
    }
  }

  const download = (filename: string, content: string) => {
    const blob = new Blob([content], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  }

  const downloadUATJson = () => {
    download("uat_scenarios.json", JSON.stringify(uatScenarios, null, 2))
  }

  const downloadUATMarkdown = () => {
    const md = uatScenarios
      .map((s) => {
        const steps = s.steps
          .map((step, i) => `${i + 1}. ${step}`)
          .join("\n")
        return `### ${s.title}\n${steps}\n**Expected:** ${s.expected}`
      })
      .join("\n\n")
    download("uat_scenarios.md", md)
  }

  const renderCode = (files: Record<string, string>) => (
    <div className="space-y-4">
      {Object.entries(files).map(([filename, code]) => (
        <div key={filename}>
          <div className="flex items-center mb-1">
            <h4 className="text-sm font-semibold flex-1">{filename}</h4>
            <button
              onClick={() => download(filename, code)}
              className="bg-gray-700 text-white px-2 py-0.5 rounded text-xs"
            >
              Download
            </button>
          </div>
          <pre className="bg-black text-green-300 p-2 rounded text-sm overflow-auto">
            {code}
          </pre>
        </div>
      ))}
    </div>
  )

  const renderUAT = (scenarios: UATScenario[]) => (
    <div className="space-y-4">
      {scenarios.map((s, i) => (
        <div key={i} className="border p-2 rounded bg-white text-sm">
          <h4 className="font-semibold">{s.title}</h4>
          <ul className="list-decimal pl-4 mt-1 text-gray-700">
            {s.steps.map((step, idx) => (
              <li key={idx}>{step}</li>
            ))}
          </ul>
          <p className="mt-2 text-gray-500">
            <strong>Expected:</strong> {s.expected}
          </p>
        </div>
      ))}
      {scenarios.length > 0 && (
        <div className="flex gap-2">
          <button
            onClick={downloadUATJson}
            className="bg-gray-700 text-white px-2 py-1 rounded text-xs"
          >
            Download JSON
          </button>
          <button
            onClick={downloadUATMarkdown}
            className="bg-gray-700 text-white px-2 py-1 rounded text-xs"
          >
            Download Markdown
          </button>
        </div>
      )}
    </div>
  )

  return (
    <div className="p-4 bg-white shadow rounded">
      <h2 className="text-lg font-semibold mb-4">🧪 Test Matrix</h2>
      <div className="flex gap-4 mb-4 items-center">
        <button
          className={`px-3 py-1 ${tab === "unit" ? "bg-blue-600 text-white" : "bg-gray-200"}`}
          onClick={() => setTab("unit")}
        >
          Unit Tests
        </button>
        <button
          className={`px-3 py-1 ${tab === "sit" ? "bg-blue-600 text-white" : "bg-gray-200"}`}
          onClick={() => setTab("sit")}
        >
          SIT Tests
        </button>
        <button
          className={`px-3 py-1 ${tab === "uat" ? "bg-blue-600 text-white" : "bg-gray-200"}`}
          onClick={() => setTab("uat")}
        >
          UAT Scenarios
        </button>
        <button onClick={fetchTests} className="ml-auto bg-green-600 text-white px-3 py-1 rounded">
          🔁 Regenerate
        </button>
        {loading && <span className="ml-2">⏳</span>}
        {!loading && error && <span className="ml-2 text-red-600">❌ {error}</span>}
        {!loading && !error && (Object.keys(unitTests).length || Object.keys(sitTests).length || uatScenarios.length) && (
          <span className="ml-2 text-green-600">✅</span>
        )}
      </div>

      {loading && <p className="text-sm">Generating tests...</p>}
      {!loading && tab === "unit" && renderCode(unitTests)}
      {!loading && tab === "sit" && renderCode(sitTests)}
      {!loading && tab === "uat" && renderUAT(uatScenarios)}
    </div>
  )
}

