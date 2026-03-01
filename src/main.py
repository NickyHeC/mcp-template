import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from dedalus_mcp import MCPServer
from dedalus_mcp.auth import Connection, SecretKeys

# Load environment variables from .env file
load_dotenv()

# Define Discord connection for token secret
# Replace name in name_connection with name of platform name of the mcp server
name_connection = Connection(
    # Replace name with of platform name of the mcp server
    name="name",
    # Replace TOKEN with credential name
    secrets=SecretKeys(token="CREDENTIAL"),
    # Replace URL with platform base url
    base_url="URL",
    # Replace Format {type} with the credential type of the connection
    auth_header_format="Format {type}",
)

# Handle imports for both package and direct execution
# Set up logging first to capture import errors

# --- Server ---

server = MCPServer(
    # Replace name with of platform name of the mcp server
    name="name-mcp",
    # Replace name with of platform name of the mcp server
    connections=[name_connection],
    authorization_server=os.getenv("DEDALUS_AS_URL", "https://as.dedaluslabs.ai"),
    streamable_http_stateless=True,
)


async def main() -> None:
    for tool_func in tools:
        server.collect(tool_func)
    await server.serve(port=8080)


if __name__ == "__main__":
    asyncio.run(main())
