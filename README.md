# mcp-template

A starter template for building MCP (Model Context Protocol) servers with the [dedalus_mcp](https://docs.dedaluslabs.ai/dmcp) framework. Authentication is handled by **DAuth** (Dedalus Auth).

This template supports three auth frameworks — **No Auth**, **API Key**, and **OAuth**. Each has its own `src-*` folder with a complete, ready-to-run server. Pick one, rename it to `src/`, and start building.

---

## What is DAuth?

[DAuth](https://www.dedaluslabs.ai/blog/dedalus-auth-launch) is a multi-tenant authentication layer for MCP servers built by Dedalus Labs. It solves a core problem in the MCP ecosystem: most servers require API keys or tokens, but the MCP spec doesn't define how non-OAuth credentials should be handled securely. Without DAuth, developers either build their own auth infrastructure or pass raw secrets around — both are bad options.

DAuth is **zero-trust** and **host-blind** — Dedalus never sees your raw API keys. Here's how it works:

1. The SDK **encrypts credentials client-side** before they leave your device.
2. When a request reaches your MCP server, it acts as a standard **OAuth 2.1 Resource Server** — access is verified without touching the credential.
3. Authenticated requests are forwarded to **the Enclave**, a network-isolated, hardware-secured execution environment written in Rust.
4. Inside the Enclave, the credential is **decrypted for milliseconds**, used to call the external API, then **zeroed from memory**.
5. Only the API **response** is returned — the raw secret is never exposed to your server code, to Dedalus, or to the network.

This means your MCP server only holds an opaque connection handle, never a raw key. DAuth is built into the `dedalus_mcp` SDK and works across all auth types (Bearer tokens, API keys, OAuth, etc.).

---

## Project Structure

```
project-root/
├── src-no-auth/             # No Auth — self-contained tools, no credentials
│   ├── main.py
│   ├── tools.py
│   └── client.py
├── src-api-key/             # API Key — static credential via DAuth
│   ├── main.py
│   ├── tools.py
│   └── client.py
├── src-oauth/               # OAuth — browser-based auth via DAuth
│   ├── main.py
│   ├── tools.py
│   └── client.py
├── pyproject.toml           # Dependencies and build config
├── .env.example             # Environment variable reference (per auth type)
├── PROJECT.md               # Platform research notepad (for you / your AI agent)
└── README.md
```

Each `src-*` folder is a complete, self-contained server. To use one:

```bash
mv src-api-key src           # rename your chosen template to src/
```

The server code expects to live in a folder called `src/` — all internal imports use `from src.tools import ...` and `from src.main import ...`. After renaming, the server is ready to configure and run.

---

## Choose Your Auth Framework

Pick the framework that matches your target platform's authentication method.

| Framework | When to use | Folder |
|-----------|-------------|--------|
| **No Auth** | Tools that don't call external APIs — calculators, formatters, local utilities | `src-no-auth/` |
| **API Key** | Platforms that use static credentials — API keys, personal access tokens, bot tokens (e.g. GitHub, Slack, Discord) | `src-api-key/` |
| **OAuth** | Platforms that require browser-based user authorization — OAuth 2.0 flows (e.g. Gmail, Linear, Spotify, Google Calendar) | `src-oauth/` |

### No Auth

Use when your tools are self-contained and don't need to call any external API.

- No `Connection` object needed
- No DAuth configuration
- No environment variables beyond basic server settings
- Tools are simple decorated functions

```python
from dedalus_mcp import MCPServer, tool

@tool(description="Add two numbers")
def add(a: float, b: float) -> float:
    return a + b

server = MCPServer("my-mcp")
server.collect(add)
```

**To use:** `mv src-no-auth src`

### API Key

Use when the platform authenticates with a static credential that the user provides once (API key, personal access token, bot token, etc.).

- `Connection` + `SecretKeys` declares the credential name
- DAuth encrypts and manages the credential in its enclave
- Tools can use `ctx.dispatch()` for authenticated requests, or call APIs directly
- Environment variables: `DEDALUS_AS_URL`, your platform's token

```python
from dedalus_mcp.auth import Connection, SecretKeys

platform_connection = Connection(
    name="github",
    secrets=SecretKeys(token="GITHUB_TOKEN"),
    base_url="https://api.github.com",
    auth_header_format="token {api_key}",
)
```

**To use:** `mv src-api-key src`

### OAuth

Use when the platform requires a browser-based OAuth flow where users authorize your application to act on their behalf.

- `Connection` + `SecretKeys` declares the token name (same as API Key from code perspective)
- The Dedalus platform handles the full OAuth token exchange externally
- OAuth configuration (client ID, client secret, authorize/token URLs, scopes) is set via environment variables
- **Important:** OAuth environment variables must be baked into the server when deploying to ensure the connection works
- Tools use `ctx.dispatch()` for authenticated requests through the DAuth enclave

```python
from dedalus_mcp.auth import Connection, SecretKeys

platform_connection = Connection(
    name="linear-mcp",
    secrets=SecretKeys(token="LINEAR_ACCESS_TOKEN"),
    base_url="https://api.linear.app",
    auth_header_format="Bearer {api_key}",
)
```

> **Note on OAuth with DAuth:** Your Python server code looks nearly identical to the API Key template. The difference is that the Dedalus platform reads the `OAUTH_*` environment variables to orchestrate the browser-based OAuth flow and token refresh. Your server code never manages OAuth tokens directly — it just calls `ctx.dispatch()` and DAuth applies the token inside the enclave.

**To use:** `mv src-oauth src`

---

## How to Build an MCP Server from This Template

### 1. Research the Target Platform API

Read the API docs for the platform you want to integrate. Note:

- Available endpoints and features
- Authentication method (Bearer token, API key, OAuth, etc.)
- Rate limits and restrictions
- Response formats

Save your notes in `PROJECT.md` — it serves as context for you and for AI coding agents in later steps. The file is pre-formatted with sections for all the information you'll need.

**Tip:** Once your `PROJECT.md` is filled in, you can hand the project off to an AI coding agent with a prompt like: *"Build my MCP server based on this template and the notes in PROJECT.md."* The agent can read the template files, your research notes, and this README to implement the full server with minimal back-and-forth.

### 2. Choose an Auth Framework and Rename the Folder

Based on your research, pick the right auth framework from the table above. Rename the chosen folder to `src/` and remove the others:

```bash
# Example: using the OAuth template
mv src-oauth src
rm -rf src-no-auth src-api-key
```

### 3. Set Up Environment Variables

```bash
cp .env.example .env
```

Fill in only the variables for your chosen auth framework. See `.env.example` for which variables belong to which framework.

- **No Auth:** No environment variables needed.
- **API Key:** Set `DEDALUS_AS_URL` and your platform's token (e.g. `GITHUB_TOKEN`).
- **OAuth:** Set `DEDALUS_AS_URL`, `DEDALUS_API_KEY`, and all `OAUTH_*` variables. These must also be configured in the deployment environment.

### 4. Configure the Server (`src/main.py`)

Customize `main.py` with your platform's details:

1. **Connection name** — Change `"platform"` to your platform's identifier (e.g. `"github"`, `"linear"`, `"spotify"`).
2. **Secret key** — Update `SecretKeys(token="API_TOKEN")` to match your credential name.
3. **Base URL** — Set to the platform's API root (e.g. `"https://api.github.com"`).
4. **Auth header format** — Set how the credential is attached. Common formats: `"Bearer {api_key}"`, `"token {api_key}"`, `"Bot {api_key}"`.
5. **Server name** — Change `"my-mcp"` to something descriptive (e.g. `"github-mcp"`).

### 5. Implement Tools (`src/tools.py`)

Define the tools your server will expose:

1. **Result models** — Create Pydantic `BaseModel` subclasses for structured return values.
2. **Request helper** — For API Key and OAuth templates, use the `api_request()` helper (which wraps `ctx.dispatch()`) to make authenticated calls through DAuth.
3. **Tool functions** — Decorate functions with `@tool(description="...")`. Use type hints for parameters and return a Pydantic model.
4. **Tool registry** — Add every tool to the `tools` list at the bottom of the file.

The template files include example tools demonstrating each pattern.

### 6. Test Locally

Install dependencies and start the server:

```bash
pip install -e .
python -m src.main
```

The server starts on port 8080. Use the included test client to verify:

```bash
python -m src.client
```

Update `src/client.py` to call your tools by name with the correct arguments.

### 7. Document Your Project

Update this README with:

- What your server does
- Available tools and their parameters
- Configuration and environment variables
- Usage examples

### 8. Deploy to Dedalus Labs

Upload your server to [dedaluslabs.ai](https://dedaluslabs.ai). DAuth handles credential security automatically in production.

**Important for OAuth servers:** Make sure all `OAUTH_*` environment variables are configured in the deployment environment. These variables are consumed by the Dedalus platform to handle the OAuth flow — they must be baked into the server at deploy time.

---

## Making Authenticated API Calls with `ctx.dispatch()`

For API Key and OAuth servers, use `ctx.dispatch()` to make authenticated requests through DAuth. The framework applies the credential inside the enclave so your code never touches raw secrets.

```python
from dedalus_mcp import tool, get_context, HttpMethod, HttpRequest
from src.main import platform_connection

@tool(description="Fetch user profile")
async def get_profile() -> dict:
    ctx = get_context()
    req = HttpRequest(method=HttpMethod.GET, path="/user/profile")
    resp = await ctx.dispatch(platform_connection, req)
    if resp.success and resp.response is not None:
        return {"success": True, "data": resp.response.body}
    error = resp.error.message if resp.error else "Request failed"
    return {"success": False, "error": error}
```

The `path` is appended to the `base_url` configured in your `Connection` object. DAuth attaches the credential to the request using the `auth_header_format` you specified.

---

## Environment Variables Reference

| Variable | Auth Framework | Description |
|----------|----------------|-------------|
| `DEDALUS_AS_URL` | API Key, OAuth | Dedalus authorization server URL (default: `https://as.dedaluslabs.ai`) |
| `DEDALUS_API_KEY` | API Key, OAuth | Your Dedalus platform API key |
| `DEDALUS_API_URL` | API Key, OAuth | Dedalus API URL (default: `https://api.dedaluslabs.ai`) |
| `API_TOKEN` | API Key | The platform credential (rename to match your platform, e.g. `GITHUB_TOKEN`) |
| `OAUTH_ENABLED` | OAuth | Set to `true` to enable OAuth flow |
| `OAUTH_AUTHORIZE_URL` | OAuth | Platform's OAuth authorization endpoint |
| `OAUTH_TOKEN_URL` | OAuth | Platform's OAuth token exchange endpoint |
| `OAUTH_CLIENT_ID` | OAuth | Your OAuth app's client ID |
| `OAUTH_CLIENT_SECRET` | OAuth | Your OAuth app's client secret |
| `OAUTH_SCOPES_AVAILABLE` | OAuth | Comma-separated list of OAuth scopes |
| `OAUTH_BASE_URL` | OAuth | Platform's API base URL for OAuth requests |

See `.env.example` for a copy-paste-ready version with sections marked by framework.

---

## Links

- [Dedalus MCP docs](https://docs.dedaluslabs.ai/dmcp)
- [DAuth launch blog post](https://www.dedaluslabs.ai/blog/dedalus-auth-launch)
- [Dashboard & deployment](https://dedaluslabs.ai/dashboard)
