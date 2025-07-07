import React from 'react'

type Props = {
  title: string
  content: string
}

export default function OutputPanel({ title, content }: Props) {
  return (
    <div className="p-4 border rounded bg-white dark:bg-gray-800">
      <h3 className="font-semibold mb-2">{title}</h3>
      <pre className="whitespace-pre-wrap text-sm">{content}</pre>
    </div>
  )
}
