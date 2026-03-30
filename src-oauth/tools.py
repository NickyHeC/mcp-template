"""OAuth tools.

Tools in an OAuth server make authenticated requests via ctx.dispatch().
This is identical to the API Key pattern — DAuth abstracts the credential
type away. The only difference is how the user's credential is obtained
(browser-based OAuth flow vs. pasting an API key).

This pattern is used in production servers like linear-mcp.
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


# --- Request Helper ---
# Centralise all API calls through a helper for consistent error handling.


async def api_request(
    method: HttpMethod,
    path: str,
    body: dict | None = None,
    headers: dict[str, str] | None = None,
) -> dict:
    """Dispatch an authenticated request through DAuth.

    DAuth applies the OAuth access token inside the enclave. Your code
    never sees the raw token.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE, PATCH).
        path: API path appended to the connection's base_url.
        body: Optional JSON body for POST/PUT/PATCH requests.
        headers: Optional extra headers.

    """
    ctx = get_context()
    req = HttpRequest(method=method, path=path, body=body, headers=headers)
    resp = await ctx.dispatch(platform_connection, req)
    if resp.success and resp.response is not None:
        resp_body = resp.response.body
        if isinstance(resp_body, dict):
            errors = resp_body.get("errors")
            if errors and isinstance(errors, list):
                msg = (
                    errors[0].get("message", "API error")
                    if isinstance(errors[0], dict)
                    else "API error"
                )
                return {"success": False, "error": str(msg)}
        return {"success": True, "data": resp_body}
    error = resp.error.message if resp.error else "Request failed"
    return {"success": False, "error": error}


# --- Tool Definitions ---
# Decorate functions with @tool to expose them to MCP clients.
# The description appears in tool listings; the docstring provides extra detail.


@tool(description="List resources from the connected platform")
async def list_resources(limit: int = 10) -> ApiResult:
    """Fetch a list of resources from the platform API.

    Replace the path and response handling with your platform's endpoints.

    Args:
        limit: Maximum number of resources to return.

    """
    result = await api_request(HttpMethod.GET, f"/resources?limit={limit}")
    return ApiResult(**result)


@tool(description="Get a single resource by ID")
async def get_resource(resource_id: str) -> ApiResult:
    """Fetch a single resource by its ID.

    Args:
        resource_id: The ID of the resource to fetch.

    """
    result = await api_request(HttpMethod.GET, f"/resources/{resource_id}")
    return ApiResult(**result)


# --- Tool Registry ---
# List every tool here. main.py iterates this list to register them with the server.

tools = [list_resources, get_resource]
