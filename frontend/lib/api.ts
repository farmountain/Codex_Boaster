// C:\Users\edwin\Codex_Boaster\frontend\lib\api.ts

const base = process.env.NEXT_PUBLIC_API_BASE_URL || '';

/**
 * Handles POST requests to the backend API.
 * @param path The API endpoint path.
 * @param body The request body.
 * @returns The JSON response from the API.
 * @throws Error if the response is not OK.
 */
async function post(path: string, body: any) {
  const res = await fetch(`${base}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  // Comprehensive error handling for non-OK responses
  if (!res.ok) {
    let errorDetail = res.statusText;
    try {
      const errorData = await res.json();
      if (errorData && typeof errorData.detail === 'string') {
        errorDetail = errorData.detail;
      } else if (errorData && typeof errorData.message === 'string') {
        errorDetail = errorData.message;
      }
    } catch (e) {
      // Ignore JSON parsing errors if response isn't JSON
    }
    throw new Error(`API POST failed with status ${res.status}: ${errorDetail}`);
  }

  return res.json();
}

/**
 * Handles GET requests to the backend API.
 * @param path The API endpoint path.
 * @returns The JSON response from the API.
 * @throws Error if the response is not OK.
 */
async function get(path: string) {
  const res = await fetch(`${base}${path}`);

  // Comprehensive error handling for non-OK responses
  if (!res.ok) {
    let errorDetail = res.statusText;
    try {
      const errorData = await res.json();
      if (errorData && typeof errorData.detail === 'string') {
        errorDetail = errorData.detail;
      } else if (errorData && typeof errorData.message === 'string') {
        errorDetail = errorData.message;
      }
    } catch (e) {
      // Ignore JSON parsing errors if response isn't JSON
    }
    throw new Error(`API GET failed with status ${res.status}: ${errorDetail}`);
  }

  return res.json();
}

/**
 * Generic function to call an agent endpoint via POST.
 * This can be used for dynamic agent calls if needed.
 * @param path The specific agent endpoint path.
 * @param body The request body for the agent.
 */
export async function callAgent(path: string, body: any) {
  // This function is a generic wrapper, so its path depends on the caller.
  // For MCP tools, this would be `'/api/mcp/tool'`.
  return post(path, body);
}

/**
 * Records a snapshot for HipCortex.
 * @param data The snapshot data to record.
 */
async function recordSnapshot(data: any) {
  const res = await fetch(`${base}/hipcortex/record`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    console.error(`Failed to record HipCortex snapshot: ${res.status} ${res.statusText}`);
    // You might want to throw an error here or handle it based on your application's needs
  }
}

/**
 * Handles the 'plan' API call.
 * @param body The request body for planning.
 */
async function plan(body: any) {
  // Path changed to '/architect/plan' based on backend FastAPI router prefix.
  return post('/architect/plan', body);
}

/**
 * Handles the 'build' API call.
 * @param body The request body for building.
 */
async function build(body: any) {
  return post('/build', body);
}

/**
 * Handles the 'test' API call.
 * @param body The request body for testing.
 */
async function test(body: any) {
  return post('/test', body);
}

/**
 * Handles the 'reflect' API call.
 * @param body The request body for reflection.
 */
async function reflect(body: any) {
  return post('/reflect', body);
}

/**
 * Handles the 'deploy' API call.
 * @param body The request body for deployment.
 */
async function deploy(body: any) {
  // Assuming the deploy_router in backend.deploy_agent has a root endpoint (e.g., @router.post("/")).
  // If not, this path would need to be updated (e.g., '/deploy/trigger').
  return post('/deploy', body);
}

/**
 * Handles the 'chat' API call.
 * @param body The request body for chat messages.
 */
async function chat(body: any) {
  // Assuming the chat_router in backend.chat_agent has a root endpoint (e.g., @router.post("/")).
  // If not, this path would need to be updated (e.g., '/chat/message').
  return post('/chat', body);
}

/**
 * Exports the frontend code as a ZIP file.
 * @returns A Blob containing the ZIP file.
 * @throws Error if the export fails.
 */
async function exportZipFunc() { // Renamed to avoid name collision with 'api.exportZip' property
  const res = await fetch(`${base}/export/frontend`);
  if (!res.ok) {
    throw new Error('Export failed');
  }
  return res.blob();
}

/**
 * Retrieves HipCortex logs for a given session ID.
 * @param id The session ID for the logs.
 */
async function getHipcortexLogs(id: string) {
  return get(`/hipcortex/logs?session_id=${id}`);
}

/**
 * Retrieves usage metrics from the monetizer service.
 */
async function getUsage() {
  return get('/monetizer/usage');
}

/**
 * Consolidates all exposed API functions into a single 'api' object for easy import.
 */
export const api = {
  recordSnapshot,
  plan,
  build,
  test,
  reflect,
  deploy,
  chat,
  exportZip: exportZipFunc, // Map the internal function to the external name
  getHipcortexLogs,
  getUsage,
  // Add other API functions here as they are developed
};