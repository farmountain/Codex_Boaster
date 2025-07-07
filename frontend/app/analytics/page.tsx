"use client"
import { useEffect, useState } from 'react'
import { LineChart } from 'lucide-react'
import AnalyticsPanel from '../../components/ui/AnalyticsPanel'

export default function AnalyticsPage() {
  const [usage, setUsage] = useState<any>(null)
  useEffect(() => {
    fetch('/monetizer/usage')
      .then(res => res.json())
      .then(setUsage)
      .catch(() => {})
  }, [])

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-semibold flex items-center gap-2">
        <LineChart className="w-6 h-6" /> Analytics
      </h1>
      <AnalyticsPanel data={JSON.stringify(usage, null, 2)} />
    </div>
  )
}
