import { useEffect, useState } from "react"
import TestMatrix from "../components/TestMatrix"
import TestResultPanel from "../components/TestResultPanel"

interface Results {
  success: boolean | null
  stdout?: string
  stderr?: string
  output?: string
}

export default function TestResults() {
  const [results, setResults] = useState<Results | null>(null)

  useEffect(() => {
    fetch("http://localhost:8000/test_results")
      .then((res) => res.json())
      .then((data) => setResults(data))
  }, [])

  return (
    <div className="p-4 space-y-4">
      <TestMatrix />
      {results && results.success !== null && (
        <TestResultPanel stdout={results.output || results.stdout} stderr={results.stderr} />
      )}
    </div>
  )
}
