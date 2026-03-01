from dedalus_mcp import tool
from pydantic import BaseModel


# --- Result Models ---
# Define Pydantic models for structured tool responses.
# Each tool should return a model so clients receive typed, predictable data.


class ExampleResult(BaseModel):
    message: str
    value: int


# --- Tool Definitions ---
# Decorate functions with @tool to expose them to MCP clients.
# The description appears in tool listings; the docstring provides extra detail.


@tool(description="An example tool that processes text and returns a result")
def example_tool(input_text: str, multiplier: int = 1) -> ExampleResult:
    """
    Process input text and return a structured result.

    Args:
        input_text: The text to process.
        multiplier: Multiplies the computed value (default: 1).
    """
    processed_value = len(input_text) * multiplier
    return ExampleResult(
        message=f"Processed: {input_text}",
        value=processed_value,
    )


# --- Tool Registry ---
# List every tool here. main.py iterates this list to register them with the server.

tools = [example_tool]
