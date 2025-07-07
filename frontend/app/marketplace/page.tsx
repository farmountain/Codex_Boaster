'use client'
import { useEffect, useState } from 'react'
import { callAgent } from '../../lib/api'

export default function MarketplacePage() {
  const [plugins, setPlugins] = useState<any[]>([])
  useEffect(() => {
    callAgent('/marketplace/list', {}).then(setPlugins).catch(()=>{})
  }, [])
  return (
    <div className="p-4 space-y-2">
      <h1 className="text-xl font-bold">Marketplace</h1>
      <ul className="list-disc ml-6">
        {plugins.map((p,i)=>(<li key={i}>{p.name}</li>))}
      </ul>
    </div>
  )
}
