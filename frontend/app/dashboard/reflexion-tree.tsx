'use client'
import ReflexionNode from '../../components/ui/ReflexionNode'
import { useReflexionHistory } from '../../lib/hooks'

function renderTree(nodes: any[]) {
  return nodes.map((n, i) => (
    <ReflexionNode key={i} step={n.step}>
      {n.children && renderTree(n.children)}
    </ReflexionNode>
  ))
}

export default function ReflexionTreePage() {
  const history = useReflexionHistory('default')
  return (
    <div className="p-4 space-y-2">
      {renderTree(history)}
    </div>
  )
}
