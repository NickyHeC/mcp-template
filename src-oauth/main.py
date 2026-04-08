"""OAuth MCP server.

Use this template when the target platform requires browser-based OAuth
(e.g. Gmail, Google Calendar, Linear, Spotify).

How it works with DAuth:
- The Connection object declares the secret name the server expects.
- OAuth credentials (client ID, secret, authorize URL, token URL, scopes) are
  configured as environment variables baked into the server at deploy time.
- The Dedalus platform handles the full OAuth token exchange flow externally.
- Your server code uses ctx.dispatch() to make authenticated requests through
  the DAuth enclave — it never sees or manages OAuth tokens directly.

To use this template, rename this folder to src/:
    mv src-oauth src
"""

import os
import asyncio
from dotenv import load_dotenv
from dedalus_mcp import MCPServer
from dedalus_mcp.server import TransportSecuritySettings
from dedalus_mcp.auth import Connection, SecretKeys

from src.tools import tools

load_dotenv()

# --- DAuth Connection (OAuth) ---
# Even for OAuth platforms, the Connection uses SecretKeys to declare the
# token name. DAuth handles the OAuth flow and token refresh externally.
# The OAUTH_* environment variables configure the flow on the Dedalus platform.
# Docs: https://docs.dedaluslabs.ai/dmcp/connections

platform_connection = Connection(
    # A short identifier for this connection — use the plain platform name
    # (e.g. "gmail", "linear", "notion"), NOT the MCP server name ("notion-mcp").
    name="platform",
    # The token name DAuth will provide after OAuth exchange
    secrets=SecretKeys(token="ACCESS_TOKEN"),
    # The base URL of the platform's API (e.g. "https://api.linear.app")
    base_url="https://api.example.com",
    # OAuth tokens are typically passed as Bearer tokens
    auth_header_format="Bearer {api_key}",
)


def create_server() -> MCPServer:
    as_url = os.getenv("DEDALUS_AS_URL", "https://as.dedaluslabs.ai")
    return MCPServer(
        # A unique name for your MCP server (e.g. "gmail-mcp", "linear-mcp")
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
