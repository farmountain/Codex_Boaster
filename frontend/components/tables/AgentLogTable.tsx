'use client'
import React from 'react'

const logs = [
  { agent: 'architect', action: 'plan', time: '2024-01-01 10:00', result: 'ok' },
  { agent: 'builder', action: 'build', time: '2024-01-01 10:05', result: 'ok' },
  { agent: 'tester', action: 'test', time: '2024-01-01 10:10', result: 'fail' },
]

export default function AgentLogTable() {
  return (
    <table className="min-w-full text-sm border rounded">
      <thead className="bg-gray-50 dark:bg-gray-700">
        <tr>
          <th className="px-2 py-1 text-left">Agent</th>
          <th className="px-2 py-1 text-left">Action</th>
          <th className="px-2 py-1 text-left">Time</th>
          <th className="px-2 py-1 text-left">Result</th>
        </tr>
      </thead>
      <tbody>
        {logs.map((log, i) => (
          <tr key={i} className="border-t">
            <td className="px-2 py-1 capitalize">{log.agent}</td>
            <td className="px-2 py-1">{log.action}</td>
            <td className="px-2 py-1 whitespace-nowrap">{log.time}</td>
            <td className="px-2 py-1">{log.result}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
