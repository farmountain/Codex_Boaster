'use client'
import { useEffect, useState } from 'react'
import { getUsage } from '../../lib/api'

type Usage = {
  daily: number
  by_agent: Record<string, number>
}

export default function UsageSummary() {
  const [usage, setUsage] = useState<Usage | null>(null)
  useEffect(() => {
    getUsage().then(setUsage).catch(() => {})
  }, [])

  return (
    <div className="p-4 border rounded bg-white dark:bg-gray-800 space-y-2">
      <h3 className="font-semibold">API Usage</h3>
      {usage ? (
        <>
          <div className="text-sm">Daily Calls: {usage.daily}</div>
          <table className="text-sm w-full">
            <tbody>
              {Object.entries(usage.by_agent || {}).map(([agent, count]) => (
                <tr key={agent} className="border-t last:border-b-0">
                  <td className="py-1 pr-2 capitalize">{agent}</td>
                  <td className="py-1 text-right">{count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      ) : (
        <div className="text-sm text-gray-500">Loading...</div>
      )}
    </div>
  )
}
