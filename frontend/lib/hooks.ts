import { useEffect, useState } from 'react'

export function useAgentStatus() {
  const [status, setStatus] = useState<any>(null)
  useEffect(() => {
    async function load() {
      try {
        const res = await fetch('/test_results')
        const data = await res.json()
        setStatus(data)
      } catch (err) {
        /* empty */
      }
    }
    load()
    const id = setInterval(load, 5000)
    return () => clearInterval(id)
  }, [])
  return status
}

export function useReflexionHistory(sessionId: string) {
  const [history, setHistory] = useState<any[]>([])
  useEffect(() => {
    fetch(`/api/hipcortex/logs?session_id=${sessionId}`)
      .then(res => res.json())
      .then(data => setHistory(data.logs || []))
      .catch(() => {})
  }, [sessionId])
  return history
}

export function useAgentLog(sessionId: string) {
  const [logs, setLogs] = useState<any[]>([])
  useEffect(() => {
    fetch(`/api/hipcortex/memory-log?session_id=${sessionId}`)
      .then(res => res.json())
      .then(data => setLogs(data))
      .catch(() => {})
  }, [sessionId])
  return logs
}
