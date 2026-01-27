import asyncio

from dedalus_mcp import MCPServer

from .tools import tools


# --- Server ---

server = MCPServer(name="example-dedalus-mcp")


async def main() -> None:
    for tool_func in tools:
        server.collect(tool_func)
    await server.serve(port=8080)


if __name__ == "__main__":
    asyncio.run(main())