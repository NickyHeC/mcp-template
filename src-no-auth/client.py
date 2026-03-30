"""Test client for the No-Auth MCP server.

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

    result = await client.call_tool("add", {"a": 3, "b": 5})
    print("add(3, 5):", result.content[0].text)

    result = await client.call_tool("reverse_text", {"text": "hello world"})
    print("reverse_text('hello world'):", result.content[0].text)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
