# RESULT -- PLAN-20260701-N8N-MCP-CHECKLIST-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-07-01 01:57:49

---

```markdown
# Deployment Checklist: czlonkowski/n8n-mcp with Existing n8n Instance

## Prerequisites
- [ ] Ensure an existing n8n instance is running and accessible (default API port 5678).
- [ ] Docker installed and configured on the deployment host.
- [ ] Network access between the MCP container and the n8n instance.
- [ ] n8n instance has workflows configured and published.
- [ ] Pull the `czlonkowski/n8n-mcp` Docker image: `docker pull czlonkowski/n8n-mcp`.

## Environment Variables
- [ ] Set `N8N_URL`: Base URL of the n8n instance (e.g., `http://n8n-host:5678`).
- [ ] Set `N8N_API_KEY`: API key for authenticating with n8n (UNCONFIRMED: required?).
- [ ] Set `MCP_PORT`: Port for the MCP server (e.g., `8080`).
- [ ] Set `MCP_TOOL_NAME`: Name to identify the tool in the AI agent's context (UNCONFIRMED: optional?).
- [ ] Set `MCP_API_KEY`: API key for the MCP server (UNCONFIRMED: required?).

## Deployment Steps
- [ ] Run the Docker container with mapped ports and environment variables:
  ```bash
  docker run -d \
    -p <MCP_PORT>:8080 \
    -e N8N_URL=<N8N_URL> \
    -e N8N_API_KEY=<N8N_API_KEY> \
    -e MCP_PORT=<MCP_PORT> \
    czlonkowski/n8n-mcp
  ```
- [ ] Verify the container is running: `docker ps`.
- [ ] Check container logs for errors: `docker logs <container_id>`.

## Verify Connection from MCP Client
- [ ] Use `curl` or a tool like Postman to query the MCP server's `/api/tools` endpoint:
  ```bash
  curl http://localhost:<MCP_PORT>/api/tools
  ```
- [ ] Ensure the response includes the expected tools from n8n.
- [ ] Test invoking a tool via the MCP server's API (UNCONFIRMED: specific endpoint?).

## Troubleshooting: Tools Not Appearing
- [ ] Confirm n8n is reachable from the MCP container (test with `curl` from the container).
- [ ] Recheck environment variables for typos or missing keys.
- [ ] Inspect n8n logs for errors related to MCP or workflow publishing.
- [ ] Ensure workflows in n8n are published and have valid triggers/actions (UNCONFIRMED: required?).
- [ ] Check if the n8n instance requires authentication and that `N8N_API_KEY` is correctly set.
- [ ] Confirm the MCP server is correctly configured to expose the workflows (UNCONFIRMED: additional setup?).
```
