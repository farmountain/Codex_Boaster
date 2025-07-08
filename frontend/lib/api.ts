const base = process.env.NEXT_PUBLIC_API_BASE_URL || ''

async function post(path: string, body: any) {
  const res = await fetch(`${base}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  return res.json()
}

async function get(path: string) {
  const res = await fetch(`${base}${path}`)
  return res.json()
}

export async function callAgent(path: string, body: any) {
  return post(path, body)
}

async function recordSnapshot(data: any) {
  await fetch(`${base}/hipcortex/record`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
}

export const api = { recordSnapshot, exportZip }

export async function plan(body: any) {
  return post('/plan', body)
}
export async function build(body: any) {
  return post('/build', body)
}
export async function test(body: any) {
  return post('/test', body)
}
export async function reflect(body: any) {
  return post('/reflect', body)
}
export async function deploy(body: any) {
  return post('/deploy', body)
}
export async function chat(body: any) {
  return post('/chat', body)
}
export async function exportZip() {
  const res = await fetch(`${base}/export/frontend`)
  if (!res.ok) throw new Error('Export failed')
  return res.blob()
}
export async function getHipcortexLogs(id: string) {
  return get(`/hipcortex/logs?session_id=${id}`)
}
export async function getUsage() {
  return get('/monetizer/usage')
}
