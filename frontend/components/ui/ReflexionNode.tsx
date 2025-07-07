import React, { useState } from 'react'

type Props = {
  step: string
  children?: React.ReactNode
}

export default function ReflexionNode({ step, children }: Props) {
  const [open, setOpen] = useState(false)
  return (
    <div className="ml-2 border-l-2 pl-2">
      <button className="text-left" onClick={() => setOpen(!open)}>
        {step}
      </button>
      {open && <div className="ml-4">{children}</div>}
    </div>
  )
}
