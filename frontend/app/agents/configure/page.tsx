

'use client'
import { RuntimeConfig, runtimeDefaults } from '../../../src/runtime.config.schema'
import RuntimeSelector from '../../../components/RuntimeSelector'


export default function ConfigAgentPage() {
  return (
    <div className="p-4">
      <RuntimeSelector />
    </div>
  )
}
