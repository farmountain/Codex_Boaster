import React from 'react'

type Props = {
  step: string
  children?: React.ReactNode
}

export default function ReflexionNode({ step, children }: Props) {
  return (
    <div className="ml-2 border-l-2 pl-2">
      <div>{step}</div>
      <div className="ml-4">{children}</div>
    </div>
  )
}
