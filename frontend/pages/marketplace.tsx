import { useEffect, useState } from "react"
import axios from "axios"

type Plugin = {
  plugin_id: string
  name: string
  type: string
  entrypoint: string
  enabled: boolean
  capabilities?: string[]
  version?: string
}

export default function Marketplace() {
  const [plugins, setPlugins] = useState<Plugin[]>([])
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState<Partial<Plugin>>({})

  useEffect(() => {
    fetchPlugins()
  }, [])

  const fetchPlugins = async () => {
    const res = await axios.get("/api/marketplace")
    setPlugins(res.data)
  }

  const togglePlugin = async (id: string) => {
    await axios.post(`/api/marketplace/toggle/${id}`)
    fetchPlugins()
  }

  const registerPlugin = async () => {
    await axios.post("/api/marketplace/register", formData)
    setFormData({})
    setShowForm(false)
    fetchPlugins()
  }

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">🛒 Plugin Marketplace</h2>

      <div className="mb-4">
        <button onClick={() => setShowForm(true)} className="bg-green-600 text-white px-3 py-1 rounded">
          ➕ Register Plugin
        </button>
      </div>

      {plugins.map(plugin => (
        <div key={plugin.plugin_id} className="border p-3 rounded mb-3 shadow-sm">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-lg font-semibold">{plugin.name}</h3>
              <p className="text-sm text-gray-600">{plugin.entrypoint}</p>
              <span className="text-xs bg-gray-200 px-2 py-0.5 rounded">{plugin.type}</span>
              {plugin.capabilities?.map(cap => (
                <span key={cap} className="text-xs ml-2 bg-blue-100 px-2 py-0.5 rounded">{cap}</span>
              ))}
            </div>
            <button
              onClick={() => togglePlugin(plugin.plugin_id)}
              className={`text-xs px-3 py-1 rounded ${plugin.enabled ? "bg-red-500 text-white" : "bg-blue-500 text-white"}`}
            >
              {plugin.enabled ? "Disable" : "Enable"}
            </button>
          </div>
        </div>
      ))}

      {showForm && (
        <div className="bg-white shadow p-4 mt-4 rounded space-y-2">
          <h4 className="text-lg font-semibold">Register New Plugin</h4>
          <input className="border p-1 w-full" placeholder="Plugin ID" onChange={e => setFormData({ ...formData, plugin_id: e.target.value })} />
          <input className="border p-1 w-full" placeholder="Name" onChange={e => setFormData({ ...formData, name: e.target.value })} />
          <input className="border p-1 w-full" placeholder="Type (LLM, DB...)" onChange={e => setFormData({ ...formData, type: e.target.value })} />
          <input className="border p-1 w-full" placeholder="Entrypoint URL" onChange={e => setFormData({ ...formData, entrypoint: e.target.value })} />
          <input className="border p-1 w-full" placeholder="Capabilities (comma-separated)" onChange={e =>
            setFormData({ ...formData, capabilities: e.target.value.split(',').map(c => c.trim()) })
          } />
          <input className="border p-1 w-full" placeholder="Version" onChange={e => setFormData({ ...formData, version: e.target.value })} />
          <div className="flex gap-2 mt-2">
            <button onClick={registerPlugin} className="bg-blue-600 text-white px-3 py-1 rounded">Submit</button>
            <button onClick={() => setShowForm(false)} className="bg-gray-400 text-white px-3 py-1 rounded">Cancel</button>
          </div>
        </div>
      )}
    </div>
  )
}
