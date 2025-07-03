import React from 'react'

export default function ConfidenceTrend({ scores }: { scores: number[] }) {
  if (!scores.length) return null
  const width = 200
  const height = 40
  const points = scores
    .map((s, i) => `${(i / (scores.length - 1 || 1)) * width},${height - s * height}`)
    .join(' ')
  return (
    <svg width={width} height={height}>
      <polyline points={points} fill="none" stroke="blue" strokeWidth="2" />
    </svg>
  )
}
