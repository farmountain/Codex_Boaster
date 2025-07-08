'use client'
import { useState } from 'react'
import BuildPanel from '../../../components/BuildPanel'

export default function BuilderAgentPage() {
  const [files, setFiles] = useState<any[]>([])

  return (
    <div className="p-4 space-y-4">
      <BuildPanel onFilesGenerated={setFiles} />
      {files.length > 0 && (
        <div className="space-y-4">
          {files.map((f, i) => (
            <div key={i}>
              <h4 className="font-semibold mb-1">{f.file_name}</h4>
              <pre className="bg-black text-green-300 p-2 rounded text-sm overflow-auto">
                {f.content}
              </pre>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
