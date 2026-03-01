import os
import asyncio
from dotenv import load_dotenv
from dedalus_mcp import MCPServer
from dedalus_mcp.auth import Connection, SecretKeys

from src.tools import tools

load_dotenv()

# --- DAuth Connection ---
# A Connection configures DAuth (Dedalus Auth) for one external platform.
# It defines the platform name, credential key, base URL, and auth header format.
# DAuth keeps secrets inside a sealed enclave — your code never sees raw keys.
# For details see the README or https://docs.dedaluslabs.ai/dmcp/connections

platform_connection = Connection(
    # A short identifier for this connection (e.g. "github", "slack", "discord")
    name="platform",
    # The credential key the user will provide (e.g. "GITHUB_TOKEN")
    secrets=SecretKeys(token="API_TOKEN"),
    # The base URL of the platform's API (e.g. "https://api.github.com")
    base_url="https://api.example.com",
    # How the token is attached to the Authorization header.
    # Common formats: "Bearer {api_key}", "token {api_key}", "Bot {api_key}"
    auth_header_format="Bearer {api_key}",
)

# --- Server ---
# The MCPServer ties everything together: it registers your DAuth connections,
# points to the Dedalus authorization server, and exposes your tools over HTTP.

server = MCPServer(
    # A unique name for your MCP server (e.g. "github-mcp", "slack-mcp")
    name="my-mcp",
    connections=[platform_connection],
    authorization_server=os.getenv("DEDALUS_AS_URL", "https://as.dedaluslabs.ai"),
    streamable_http_stateless=True,
)


async def main() -> None:
    for tool_func in tools:
        server.collect(tool_func)
    await server.serve(port=8080)


if __name__ == "__main__":
    asyncio.run(main())
