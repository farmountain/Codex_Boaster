export default async function handler(req, res) {
  if (req.method !== 'GET' && req.method !== 'POST') {
    res.status(405).end()
    return
  }
  const url = 'http://localhost:8000/api/config/env'
  const options: RequestInit = {
    method: req.method,
    headers: { 'Content-Type': 'application/json' },
  }
  if (req.method === 'POST') {
    options.body = JSON.stringify(req.body)
  }
  const resp = await fetch(url, options)
  const data = await resp.json()
  res.status(resp.status).json(data)
}
