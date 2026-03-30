"""API Key MCP server.

Use this template when the target platform authenticates with a static
credential — API key, personal access token, bot token, etc.

DAuth encrypts the credential client-side and executes API calls inside a
sealed enclave. Your server code never sees the raw key.

To use this template, rename this folder to src/:
    mv src-api-key src
"""

import os
import asyncio
from dotenv import load_dotenv
from dedalus_mcp import MCPServer
from dedalus_mcp.server import TransportSecuritySettings
from dedalus_mcp.auth import Connection, SecretKeys

from src.tools import tools

load_dotenv()

# --- DAuth Connection (API Key) ---
# A Connection configures DAuth (Dedalus Auth) for one external platform.
# DAuth keeps secrets inside a sealed enclave — your code never sees raw keys.
# See README.md > "Choose Your Auth Framework" for guidance.
# Docs: https://docs.dedaluslabs.ai/dmcp/connections

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


def create_server() -> MCPServer:
    as_url = os.getenv("DEDALUS_AS_URL", "https://as.dedaluslabs.ai")
    return MCPServer(
        # A unique name for your MCP server (e.g. "github-mcp", "slack-mcp")
        name="my-mcp",
        connections=[platform_connection],
        http_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
        streamable_http_stateless=True,
        authorization_server=as_url,
    )


async def main() -> None:
    server = create_server()
    for tool_func in tools:
        server.collect(tool_func)
    await server.serve(port=8080)


if __name__ == "__main__":
    asyncio.run(main())
