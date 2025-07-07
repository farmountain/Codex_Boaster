import React from 'react'

type Props = {
  name: string
  status?: string
  onClick?: () => void
}

export default function AgentCard({ name, status, onClick }: Props) {
  return (
    <div onClick={onClick} className="p-4 border rounded cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700">
      <h3 className="font-semibold">{name}</h3>
      {status && <p className="text-sm text-gray-500 dark:text-gray-400">{status}</p>}
    </div>
  )
}
