export default async function handler(req, res) {
  const {
    query: { plugin_id },
    method
  } = req;

  if (method !== 'POST') {
    res.status(405).end();
    return;
  }

  const resp = await fetch(`http://localhost:8000/api/marketplace/toggle/${plugin_id}`, {
    method: 'POST'
  });
  const data = await resp.json();
  res.status(resp.status).json(data);
}
