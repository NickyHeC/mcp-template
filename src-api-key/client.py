"""Test client for the API Key MCP server.

Start the server first:
    python -m src.main

Then run this script to verify your tools work:
    python -m src.client
"""

import asyncio
from dedalus_mcp.client import MCPClient


async def main() -> None:
    client = await MCPClient.connect("http://127.0.0.1:8080/mcp")

    tools = await client.list_tools()
    print("Available tools:", [t.name for t in tools.tools])

    result = await client.call_tool("example_tool", {"input_text": "hello", "multiplier": 3})
    print("example_tool result:", result.content[0].text)

    result = await client.call_tool("fetch_resource", {"resource_id": "abc-123"})
    print("fetch_resource result:", result.content[0].text)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
