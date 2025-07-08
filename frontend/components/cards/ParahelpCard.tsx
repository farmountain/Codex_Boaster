'use client'
import React from 'react'

type Props = {
  role: string
  goal: string
  format: string
  constraints: string
}

export default function ParahelpCard({ role, goal, format, constraints }: Props) {
  return (
    <div className="p-4 border rounded bg-white dark:bg-gray-800 space-y-1">
      <h3 className="font-semibold mb-2">Parahelp SOP</h3>
      <div><strong>Role:</strong> {role}</div>
      <div><strong>Goal:</strong> {goal}</div>
      <div><strong>Format:</strong> {format}</div>
      <div><strong>Constraints:</strong> {constraints}</div>
    </div>
  )
}
