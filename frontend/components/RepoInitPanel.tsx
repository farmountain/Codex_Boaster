import { useState } from "react"
import axios from "axios"

export default function RepoInitPanel() {
  const [projectName, setProjectName] = useState("")
  const [description, setDescription] = useState("")
  const [language, setLanguage] = useState("python")
  const [isPrivate, setIsPrivate] = useState(true)
  const [ci, setCi] = useState("github-actions")
  const [loading, setLoading] = useState(false)
  const [response, setResponse] = useState(null)
  const [error, setError] = useState("")

  const createRepo = async () => {
    setLoading(true)
    setError("")
    try {
      const res = await axios.post("/api/repo-init", {
        project_name: projectName,
        description,
        language,
        private: isPrivate,
        ci,
      })
      setResponse(res.data)
    } catch (err) {
      setError(err?.response?.data?.detail || "Repo init failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white p-4 rounded shadow-md space-y-4">
      <h2 className="text-lg font-semibold">🧱 Initialize GitHub Project</h2>

      <input
        className="w-full border p-2"
        placeholder="Project Name"
        value={projectName}
        onChange={e => setProjectName(e.target.value)}
      />
      <textarea
        className="w-full border p-2"
        placeholder="Project Description"
        value={description}
        onChange={e => setDescription(e.target.value)}
      />

      <div className="flex gap-4">
        <div>
          <label className="block text-sm mb-1">Language</label>
          <select
            className="border p-2"
            value={language}
            onChange={e => setLanguage(e.target.value)}
          >
            <option value="python">Python</option>
            <option value="node">Node</option>
            <option value="rust">Rust</option>
          </select>
        </div>
        <div>
          <label className="block text-sm mb-1">CI Tool</label>
          <select
            className="border p-2"
            value={ci}
            onChange={e => setCi(e.target.value)}
          >
            <option value="github-actions">GitHub Actions</option>
            <option value="none">None</option>
          </select>
        </div>
        <div className="flex items-center gap-2 mt-6">
          <input
            type="checkbox"
            checked={isPrivate}
            onChange={e => setIsPrivate(e.target.checked)}
          />
          <span className="text-sm">Private</span>
        </div>
      </div>

      <button
        className="bg-blue-600 text-white px-4 py-2 rounded"
        onClick={createRepo}
        disabled={loading}
      >
        {loading ? "Creating..." : "Create Repository"}
      </button>

      {error && <p className="text-red-500 text-sm">{error}</p>}

      {response && (
        <div className="border-t pt-4 text-sm">
          ✅ Repo created:{" "}
          <a href={response.repo_url} className="text-blue-600 underline" target="_blank">
            {response.repo_url}
          </a>
          <br />
          CI Setup: {response.ci_setup}
        </div>
      )}
    </div>
  );
}
