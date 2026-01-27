# mcp-template

A template MCP (Model Context Protocol) server for quickly starting a new project using the dedalus_mcp framework.

## Overall Process for Creating an MCP Server Using Dedalus

Follow these steps to build your MCP server from this template:

### 1. Research and Document the Target Platform API

Read the API documentation of your target platform to understand:
- Available features and endpoints
- API restrictions and rate limits
- Authentication requirements
- Data formats and response structures

**Tip**: Create a `PROJECT.md` file to document your findings. This will serve as context for coding agents in later steps.

### 2. Set Up API Access

- Identify the required API access keys and tokens
- Create an application/account according to platform requirements if necessary
- Securely store credentials (use environment variables, not hardcoded values)

### 3. Initialize Project Structure

Create a GitHub repository and set up the project structure:

```
project-root/
├── src/
│   ├── main.py             # Entry point and server configuration
│   └── tools.py            # Tool definitions and implementations
├── pyproject.toml          # Project metadata and dependencies
├── PROJECT.md              # Your platform research notes (optional)
└── README.md               # Project documentation
```

Use a coding agent to construct this structure based on the template.

### 4. Configure the Server (`main.py`)

Copy the template `main.py` and customize it:

- **Server Instance**: Update the `MCPServer` name identifier
- **Main Function**: Configure the port (default: 8080) and ensure it collects tools from `tools.py`

The server uses `server.collect()` to register tools decorated with the `@tool` decorator. Reference your `PROJECT.md` for platform-specific configuration needs.

### 5. Implement Tools (`tools.py`)

Define your tools based on desired features:

- **Result Models**: Create Pydantic models (extending `BaseModel`) that define the structure of tool return values
- **Tool Functions**: Implement functions decorated with `@tool` that:
  - Include a clear description in the decorator
  - Accept typed parameters (with optional defaults)
  - Return a Pydantic model instance
  - Include docstrings for additional documentation
- **Tools List**: Export all tools in a `tools` list for automatic collection by the server

The template includes an example tool (`example_tool`) demonstrating:
- Input parameters with type hints
- Optional parameters with default values
- Returning structured data using a Pydantic model
- Basic processing logic

You can modify or replace this example with your own implementations.
Reference your `PROJECT.md` for notes on tools and features.

### 6. Test Locally

1. Install dependencies:
   ```bash
   pip install -e .
   ```

2. Run the server:
   ```bash
   python -m src.main
   ```

3. Test with a real use case to verify functionality
4. The server will start on port 8080 and be ready to accept MCP client connections

### 7. Document Your Project

Generate or update `README.md` with:
- Project overview and purpose
- Installation and usage instructions
- Available tools and their descriptions
- Configuration requirements
- Examples and use cases

### 8. Deploy to Dedalus Labs

Upload your server to [dedaluslabs.ai](https://dedaluslabs.ai) and debug as necessary. Ensure all environment variables and credentials are properly configured in the deployment environment.

---

## Server Architecture

This template follows a clean separation between server setup and tool definitions:

### main.py

The entry point of the MCP server:
- Creates an `MCPServer` instance with a name identifier
- Collects all tools from the `tools.py` module using `server.collect()`
- Starts the server on a specified port (default: 8080)

### tools.py

Contains tool definitions and implementations:
- **Result Models**: Pydantic models defining return value structures
- **Tool Functions**: Functions decorated with `@tool` implementing functionality
- **Tools List**: Exports all available tools for automatic collection

The server automatically collects and registers all tools from the `tools` list, making them available to MCP clients.
