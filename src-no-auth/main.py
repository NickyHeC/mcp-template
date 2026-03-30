"""No-Auth MCP server.

Use this template when the server exposes self-contained tools that do not
call any external API requiring credentials (e.g. calculators, formatters,
local utilities).

No DAuth connection or environment variables are needed.

To use this template, rename this folder to src/:
    mv src-no-auth src
"""

import asyncio
from dedalus_mcp import MCPServer

from src.tools import tools


server = MCPServer(
    # A unique name for your MCP server (e.g. "calculator-mcp", "utils-mcp")
    name="my-mcp",
)


async def main() -> None:
    for tool_func in tools:
        server.collect(tool_func)
    await server.serve(port=8080)


if __name__ == "__main__":
    asyncio.run(main())
