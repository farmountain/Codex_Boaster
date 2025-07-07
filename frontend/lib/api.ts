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

export const api = {
  plan: (body: any) => post('/plan', body),
  build: (body: any) => post('/build', body),
  test: (body: any) => post('/test', body),
  reflect: (body: any) => post('/reflect', body),
  deploy: (body: any) => post('/deploy', body),
  chat: (body: any) => post('/chat', body),
  exportZip: () => get('/export'),
  getHipcortexLogs: (id: string) => get(`/hipcortex/logs?session_id=${id}`),
  getUsage: () => get('/monetizer/usage'),
}

export { post as callAgent, get as getAgent }
