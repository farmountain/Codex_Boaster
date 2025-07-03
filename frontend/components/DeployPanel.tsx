import { useState, useEffect } from "react"
import axios from "axios"

export default function DeployPanel() {
  const [projectName, setProjectName] = useState("codex-booster-demo")
  const [repoUrl, setRepoUrl] = useState("https://github.com/user/codex-demo")
  const [provider, setProvider] = useState("vercel")
  const [status, setStatus] = useState("idle")
  const [result, setResult] = useState(null)
  const [buildLogs, setBuildLogs] = useState("")

  const deploy = async () => {
    setStatus("pending")
    try {
      const res = await axios.post("/api/deploy", {
        project_name: projectName,
        repo_url: repoUrl,
        provider,
        framework: "nextjs",
      })
      setResult(res.data)
      setStatus("success")
    } catch (err) {
      setStatus("error")
    }
  }

  useEffect(() => {
    let timer: NodeJS.Timeout
    async function poll() {
      const res = await axios.get("/api/deploy/status")
      setBuildLogs(res.data.logs)
      if (res.data.status !== "pending") {
        clearInterval(timer)
      }
    }
    if (status === "pending") {
      timer = setInterval(poll, 2000)
    }
    return () => clearInterval(timer)
  }, [status])

  return (
    <div className="p-4 bg-white shadow rounded space-y-4">
      <h2 className="text-lg font-bold flex items-center space-x-2">
        <span>🚀 One-Click Deployment</span>
        <span className={`text-sm ${status === 'success' ? 'text-green-600' : status === 'pending' ? 'text-yellow-600' : 'text-gray-600'}`}>{status}</span>
      </h2>

      <div className="space-y-2">
        <input
          className="w-full border p-2"
          placeholder="Project Name"
          value={projectName}
          onChange={e => setProjectName(e.target.value)}
        />
        <input
          className="w-full border p-2"
          placeholder="GitHub Repo URL"
          value={repoUrl}
          onChange={e => setRepoUrl(e.target.value)}
        />
        <select
          className="w-full border p-2"
          value={provider}
          onChange={e => setProvider(e.target.value)}
        >
          <option value="vercel">Vercel</option>
          <option value="flyio">Fly.io</option>
        </select>

        <button
          onClick={deploy}
          disabled={status === "pending"}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          {status === "pending" ? "Deploying..." : "Deploy Now"}
        </button>
      </div>

      {status === "success" && result && (
        <div className="border-t pt-4 text-sm space-y-1">
          <div>
            ✅ <strong>Deployment Triggered</strong>
          </div>
          <div>
            Preview:{" "}
            <a
              href={result.deployment_url}
              target="_blank"
              className="text-blue-600 underline"
            >
              {result.deployment_url}
            </a>
          </div>
          <div>
            Logs:{" "}
            <a
              href={result.logs_url}
              target="_blank"
              className="text-blue-600 underline"
            >
              View Logs
            </a>
          </div>
          <div className="text-gray-500">{result.message}</div>
        </div>
      )}

      {buildLogs && (
        <pre className="bg-gray-100 p-2 mt-2 overflow-x-auto text-xs">{buildLogs}</pre>
      )}

      {status === "error" && (
        <div className="text-red-500 mt-2">
          ❌ Deployment failed. Check logs or credentials.
        </div>
      )}
    </div>
  )
}

