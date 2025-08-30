import { useEffect, useState } from 'react'
import axios from 'axios'
import { RuntimeConfig, runtimeDefaults } from '../src/runtime.config.schema'

const options: Record<keyof RuntimeConfig, string[]> = {
  python: ['3.12'],
  nodejs: ['20'],
  ruby: ['3.4.4'],
  rust: ['1.87.0'],
  go: ['1.23.8'],
  bun: ['1.2.14'],
  java: ['21'],
  swift: ['6.1']
}

export default function RuntimeSelector() {
  const [config, setConfig] = useState<RuntimeConfig>(runtimeDefaults)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    axios.get('/runtime-config').then(res => {
      setConfig(res.data)
    })
  }, [])

  const handleChange = (lang: keyof RuntimeConfig, ver: string) => {
    setConfig(prev => ({ ...prev, [lang]: ver }))
  }

  const handleSave = async () => {
    setLoading(true)
    try {
      await axios.post('/runtime-config', config)
      setMessage('Runtime config saved')
    } catch {
      setMessage('Failed to save runtime config')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-4 rounded border bg-white shadow-md">
      <h2 className="text-lg font-semibold mb-2">Runtime Selector</h2>
      {Object.entries(options).map(([lang, versions]) => (
        <div key={lang} className="mb-4">
          <label className="block mb-1 capitalize">{lang}</label>
          <select
            className="border p-2 w-full"
            value={config[lang as keyof RuntimeConfig] || versions[0]}
            onChange={e => handleChange(lang as keyof RuntimeConfig, e.target.value)}
          >
            {versions.map(v => (
              <option key={v}>{v}</option>
            ))}
          </select>
        </div>
      ))}
      <pre className="bg-gray-100 p-2 text-sm whitespace-pre-wrap">
{JSON.stringify({ runtimes: config }, null, 2)}
      </pre>
      <button
        onClick={handleSave}
        className="bg-blue-600 text-white px-4 py-2 rounded mt-2"
        disabled={loading}
      >
        {loading ? 'Saving...' : 'Save'}
      </button>
      {message && <p className="mt-2 text-sm text-gray-700">{message}</p>}
    </div>
  )
}
