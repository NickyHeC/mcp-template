"""
Test client for the MCP server.

Start the server first:
    python -m src.main

Then run this script to verify your tools work:
    python -m src.client
"""

import asyncio
from dedalus_mcp.client import MCPClient


async def main() -> None:
    client = await MCPClient.connect("http://127.0.0.1:8080/mcp")

    # List all registered tools
    tools = await client.list_tools()
    print("Available tools:", [t.name for t in tools.tools])

    # Call a tool by name, passing its expected arguments
    result = await client.call_tool("example_tool", {"input_text": "hello", "multiplier": 3})
    print("Result:", result.content[0].text)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
