'use client'
import { useState } from 'react'
import PromptEditor from '../../components/ui/PromptEditor'
import ParahelpCard from '../../components/cards/ParahelpCard'
import PromptFoldingToggle from '../../components/ui/PromptFoldingToggle'

const library = [
  { title: 'Feature Spec', prompt: 'Write a feature spec using Parahelp SOP.' },
  { title: 'Bug Report', prompt: 'Describe a bug with steps to reproduce.' },
]

export default function PromptsPage() {
  const [current, setCurrent] = useState(library[0].prompt)
  return (
    <div className="h-screen flex">
      <aside className="w-60 border-r p-4 space-y-2 overflow-y-auto bg-gray-50 dark:bg-gray-900">
        <h3 className="font-semibold mb-2">Prompt Library</h3>
        {library.map((p) => (
          <button
            key={p.title}
            onClick={() => setCurrent(p.prompt)}
            className="block w-full text-left p-2 border rounded hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            {p.title}
          </button>
        ))}
      </aside>
      <main className="flex-1 p-4 space-y-4 overflow-auto">
        <PromptFoldingToggle />
        <PromptEditor value={current} onChange={setCurrent} />
        <ParahelpCard role="Developer" goal="Ship feature" format="XML" constraints="100 words" />
      </main>
    </div>
  )
}
