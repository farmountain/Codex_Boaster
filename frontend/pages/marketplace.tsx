import { useState, useEffect } from "react"

export default function Marketplace() {
  const [plugins, setPlugins] = useState([])

  useEffect(() => {
    fetch("/api/marketplace")
      .then(res => res.json())
      .then(setPlugins)
  }, [])

  async function install(plugin) {
    const res = await fetch("/api/marketplace/install", {
      method: "POST",
      body: JSON.stringify(plugin),
      headers: { "Content-Type": "application/json" }
    })
    const data = await res.json()
    alert(data.message)
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Agent & Plugin Marketplace</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {plugins.map((plugin, i) => (
          <div key={i} className="border p-4 rounded shadow bg-white">
            <div className="flex items-center space-x-4">
              <img src={plugin.icon_url} className="w-10 h-10" />
              <div>
                <h3 className="font-bold text-lg">{plugin.name}</h3>
                <p className="text-gray-600 text-sm">{plugin.type}</p>
              </div>
            </div>
            <p className="mt-3 text-gray-800 text-sm">{plugin.description}</p>
            <p className="mt-2 text-sm text-gray-500">
              Endpoint: <code>{plugin.endpoint}</code>
            </p>
            <button
              onClick={() => install(plugin)}
              className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              {plugin.is_installed ? "Installed" : "Install"}
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
