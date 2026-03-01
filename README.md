# mcp-template

A starter template for building MCP (Model Context Protocol) servers with the [dedalus_mcp](https://docs.dedaluslabs.ai/dmcp) framework. Authentication is handled by **DAuth** (Dedalus Auth).

## What is DAuth?

[DAuth](https://www.dedaluslabs.ai/blog/dedalus-auth-launch) is a multi-tenant authentication layer for MCP servers built by Dedalus Labs. It solves a core problem in the MCP ecosystem: most servers require API keys or tokens, but the MCP spec doesn't define how non-OAuth credentials should be handled securely. Without DAuth, developers either build their own auth infrastructure or pass raw secrets around — both are bad options.

DAuth is **zero-trust** and **host-blind** — Dedalus never sees your raw API keys. Here's how it works:

1. The SDK **encrypts credentials client-side** before they leave your device.
2. When a request reaches your MCP server, it acts as a standard **OAuth 2.1 Resource Server** — access is verified without touching the credential.
3. Authenticated requests are forwarded to **the Enclave**, a network-isolated, hardware-secured execution environment written in Rust.
4. Inside the Enclave, the credential is **decrypted for milliseconds**, used to call the external API, then **zeroed from memory**.
5. Only the API **response** is returned — the raw secret is never exposed to your server code, to Dedalus, or to the network.

This means your MCP server only holds an opaque connection handle, never a raw key. DAuth is built into the `dedalus_mcp` SDK, takes minutes to integrate, and works across all auth types (Bearer tokens, API keys, OAuth, etc.).

In this template, the `Connection` object in `main.py` is how you configure DAuth for your target platform.

## Project Structure

```
project-root/
├── src/
│   ├── main.py      # Server entry point and configuration
│   ├── tools.py     # Tool definitions and implementations
│   └── client.py    # Test client for local debugging
├── pyproject.toml   # Dependencies and build config
├── PROJECT.md       # Your platform research notes (optional)
└── README.md
```

## How to Build an MCP Server from This Template

### 1. Research the Target Platform API

Read the API docs for the platform you want to integrate. Note:

- Available endpoints and features
- Authentication method (Bearer token, API key, OAuth, etc.)
- Rate limits and restrictions
- Response formats

**Tip:** Save your notes in a `PROJECT.md` file — it serves as useful context for coding agents in later steps.

### 2. Set Up API Access

- Obtain the required API keys or tokens.
- Create an application/account on the platform if needed.
- Store credentials in environment variables (never hardcode them).

### 3. Configure the Server and DAuth (`main.py`)

Customize `main.py` with your platform's details:

1. **DAuth Connection** — Update `platform_connection` with your platform's name, credential key, base URL, and auth header format. This `Connection` object tells DAuth *which* platform to authenticate with and *how* to attach the credential (see [What is DAuth?](#what-is-dauth) above). The inline comments in `main.py` include concrete examples.
2. **Server name** — Change `"my-mcp"` to something descriptive (e.g. `"github-mcp"`).

The server registers tools via `server.collect()` and serves them over HTTP.

### 4. Implement Tools (`tools.py`)

Define the tools your server will expose:

1. **Result models** — Create Pydantic `BaseModel` subclasses for structured return values.
2. **Tool functions** — Decorate functions with `@tool(description="...")`. Use type hints for parameters and return a Pydantic model.
3. **Tool registry** — Add every tool to the `tools` list at the bottom of the file so the server can find them.

The included `example_tool` demonstrates this pattern. Replace or extend it with your own implementations.

### 5. Test Locally

Install dependencies and start the server:

```bash
pip install -e .
python -m src.main
```

The server starts on port 8080. Use the included test client to verify:

```bash
python -m src.client
```

### 6. Document Your Project

Update this README with:

- What your server does
- Available tools and their parameters
- Configuration and environment variables
- Usage examples

### 7. Deploy to Dedalus Labs

Upload your server to [dedaluslabs.ai](https://dedaluslabs.ai). DAuth handles credential security automatically in production. Make sure all environment variables are configured in the deployment environment.
