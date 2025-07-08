'use client'
import React from 'react'

type Point = { day: string; count: number }

export default function AgentUsageLineChart({ data }: { data?: Point[] }) {
  const points = (data || sample).map((d, i, arr) => {
    const max = Math.max(...(data || sample).map(p => p.count)) || 1
    const x = i * 40
    const y = 100 - (d.count / max) * 100
    return `${x},${y}`
  })
  const width = ((data || sample).length - 1) * 40 + 40
  const path = points.join(' ')
  return (
    <svg width={width} height={100} className="stroke-blue-600 fill-none">
      <polyline points={path} />
    </svg>
  )
}

const sample: Point[] = [
  { day: 'Mon', count: 2 },
  { day: 'Tue', count: 4 },
  { day: 'Wed', count: 3 },
  { day: 'Thu', count: 5 },
  { day: 'Fri', count: 6 },
]
