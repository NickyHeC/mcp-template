"""API Key tools.

Tools in an API Key server can make authenticated requests to the target
platform using ctx.dispatch(). DAuth applies the credential inside the
enclave — your tool code never handles raw secrets.
"""

from typing import Any

from dedalus_mcp import tool, get_context, HttpMethod, HttpRequest
from pydantic import BaseModel

# Import your connection object from main so ctx.dispatch knows which
# platform credentials to use. Update this import to match your connection.
from src.main import platform_connection


# --- Result Models ---
# Define Pydantic models for structured tool responses.
# Each tool should return a model so clients receive typed, predictable data.


class ApiResult(BaseModel):
    success: bool
    data: Any = None
    error: str | None = None


class ExampleResult(BaseModel):
    message: str
    value: int


# --- Request Helper ---
# Centralise API calls through a helper so error handling is consistent.


async def api_request(
    method: HttpMethod,
    path: str,
    body: dict | None = None,
) -> dict:
    """Dispatch an authenticated request through DAuth.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE, PATCH).
        path: API path appended to the connection's base_url (e.g. "/repos").
        body: Optional JSON body for POST/PUT/PATCH requests.

    """
    ctx = get_context()
    req = HttpRequest(method=method, path=path, body=body)
    resp = await ctx.dispatch(platform_connection, req)
    if resp.success and resp.response is not None:
        return {"success": True, "data": resp.response.body}
    error = resp.error.message if resp.error else "Request failed"
    return {"success": False, "error": error}


# --- Tool Definitions ---
# Decorate functions with @tool to expose them to MCP clients.
# The description appears in tool listings; the docstring provides extra detail.


@tool(description="An example tool that processes text and returns a result")
def example_tool(input_text: str, multiplier: int = 1) -> ExampleResult:
    """Process input text and return a structured result.

    Args:
        input_text: The text to process.
        multiplier: Multiplies the computed value (default: 1).

    """
    processed_value = len(input_text) * multiplier
    return ExampleResult(
        message=f"Processed: {input_text}",
        value=processed_value,
    )


@tool(description="Example: fetch a resource from the platform API")
async def fetch_resource(resource_id: str) -> ApiResult:
    """Fetch a resource by ID from the connected platform.

    Replace the path and response handling with your platform's API.

    Args:
        resource_id: The ID of the resource to fetch.

    """
    result = await api_request(HttpMethod.GET, f"/resources/{resource_id}")
    return ApiResult(**result)


# --- Tool Registry ---
# List every tool here. main.py iterates this list to register them with the server.

tools = [example_tool, fetch_resource]
