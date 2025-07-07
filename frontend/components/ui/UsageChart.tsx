'use client'
import { useEffect, useState } from 'react'

export default function UsageChart() {
  const [data, setData] = useState<string>('')
  useEffect(() => {
    fetch('/monetizer/usage').then(res=>res.json()).then(d=>{
      setData(JSON.stringify(d))
    }).catch(()=>{})
  }, [])
  return (
    <div className="border p-4 rounded">
      <h2 className="font-semibold mb-2">Usage</h2>
      <pre className="text-sm">{data}</pre>
    </div>
  )
}
