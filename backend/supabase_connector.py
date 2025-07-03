import httpx


class SupabaseClient:
    """Minimal async Supabase REST client."""

    def __init__(self, url: str, key: str):
        self.url = url.rstrip('/')
        self.headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }
        self._client = httpx.AsyncClient()

    async def insert(self, table: str, data: dict):
        """Insert a row into a table."""
        resp = await self._client.post(
            f"{self.url}/rest/v1/{table}", headers=self.headers, json=data
        )
        resp.raise_for_status()
        return resp.json()
