export default async function handler(req, res) {
  if (req.method !== 'GET') {
    res.status(405).end();
    return;
  }
  const resp = await fetch('http://localhost:8000/marketplace', {
    method: 'GET'
  });
  const data = await resp.json();
  res.status(resp.status).json(data);
}
