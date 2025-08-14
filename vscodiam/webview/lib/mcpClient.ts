export class MCPClient {
  constructor(private baseUrl: string) {}

  async login(username: string, password: string) {
    const res = await fetch(`${this.baseUrl}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (!res.ok) {
      throw new Error('Login failed');
    }

    return res.json();
  }
}
