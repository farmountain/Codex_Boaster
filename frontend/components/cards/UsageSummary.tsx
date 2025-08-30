'use client'
import { useEffect, useState } from 'react'
import { api } from '../../lib/api' // Corrected: Import the 'api' object instead of individual functions

type Usage = {
  daily: number
  by_agent: Record<string, number>
}

export default function UsageSummary() {
  const [usage, setUsage] = useState<Usage | null>(null)
  const [loading, setLoading] = useState(true) // Add loading state
  const [error, setError] = useState<string | null>(null) // Add error state

  useEffect(() => {
    async function fetchUsage() {
      try {
        setLoading(true)
        setError(null) // Clear previous errors
        // Corrected: Call getUsage as a property of the 'api' object
        const data = await api.getUsage()
        setUsage(data)
      } catch (err) {
        console.error('Failed to fetch usage data:', err)
        setError('Failed to load API usage data.') // Set a user-friendly error message
      } finally {
        setLoading(false)
      }
    }

    fetchUsage()
  }, []) // Empty dependency array ensures this runs once on mount

  return (
    <div className="p-4 border rounded bg-white dark:bg-gray-800 space-y-2">
      <h3 className="font-semibold">API Usage</h3>
      {loading ? ( // Display loading state
        <div className="text-sm text-gray-500">Loading...</div>
      ) : error ? ( // Display error state
        <div className="text-sm text-red-500">{error}</div>
      ) : usage ? (
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
        <div className="text-sm text-gray-500">No usage data available.</div> // Fallback if no usage
      )}
    </div>
  )
}