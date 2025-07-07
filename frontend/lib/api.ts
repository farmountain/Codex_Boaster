export async function callAgent(path: string, body: any) {
  const base = process.env.NEXT_PUBLIC_API_BASE_URL || ''
  const res = await fetch(`${base}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  return res.json()
}
