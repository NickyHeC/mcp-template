"""Test client for the OAuth MCP server.

Two modes:

1. Test connection only (no server needed):
       python -m src.client --test-connection

   Uses ConnectionTester to verify your Connection config and credentials
   work against the target platform. You need a valid access token in .env
   for local testing — obtain one from the platform's OAuth playground or
   developer console. When deployed, DAuth handles the OAuth flow automatically.

2. Test tools (server must be running):
       python -m src.main        # in one terminal
       python -m src.client      # in another
"""

import asyncio
import sys
from dotenv import load_dotenv

load_dotenv()


async def test_connection() -> None:
    """Verify the DAuth connection config and credentials without a running server."""
    from dedalus_mcp.testing import ConnectionTester, TestRequest
    from src.main import platform_connection

    tester = ConnectionTester.from_env(platform_connection)

    # Replace "/user" with a lightweight endpoint from your target platform:
    #   Linear:          "/viewer" (GraphQL — adjust as needed)
    #   Google (Gmail):  "/gmail/v1/users/me/profile"
    #   Spotify:         "/v1/me"
    response = await tester.request(TestRequest(path="/user"))

    if response.success:
        print(f"OK {response.status} — Connection works!")
        print(f"Response: {response.body}")
    else:
        print(f"FAIL {response.status}")
        print(f"Response: {response.body}")


async def test_tools() -> None:
    """Connect to the running server and call tools."""
    from dedalus_mcp.client import MCPClient

    client = await MCPClient.connect("http://127.0.0.1:8080/mcp")

    tools = await client.list_tools()
    print("Available tools:", [t.name for t in tools.tools])

    result = await client.call_tool("list_resources", {"limit": 5})
    print("list_resources result:", result.content[0].text)

    result = await client.call_tool("get_resource", {"resource_id": "abc-123"})
    print("get_resource result:", result.content[0].text)

    await client.close()


if __name__ == "__main__":
    if "--test-connection" in sys.argv:
        asyncio.run(test_connection())
    else:
        asyncio.run(test_tools())
