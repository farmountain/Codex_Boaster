'use client'
import ReflexionNode from '../../components/ui/ReflexionNode'
import { useReflexionHistory } from '../../lib/hooks'

export default function ReflexionTreePage() {
  const history = useReflexionHistory('default')
  return (
    <div className="p-4 space-y-2">
      {history.map((step, i) => (
        <ReflexionNode key={i} step={step.step}>
          {step.details}
        </ReflexionNode>
      ))}
    </div>
  )
}
