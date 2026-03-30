"""No-Auth tools.

Tools in a No-Auth server are self-contained — they do not call external APIs.
Use Pydantic models for structured return values so clients get typed,
predictable data.
"""

from dedalus_mcp import tool
from pydantic import BaseModel


# --- Result Models ---
# Define Pydantic models for structured tool responses.
# Each tool should return a model so clients receive typed, predictable data.


class CalculationResult(BaseModel):
    expression: str
    result: float


class TextResult(BaseModel):
    original: str
    transformed: str


# --- Tool Definitions ---
# Decorate functions with @tool to expose them to MCP clients.
# The description appears in tool listings; the docstring provides extra detail.


@tool(description="Add two numbers")
def add(a: float, b: float) -> CalculationResult:
    """Add two numbers and return the result."""
    return CalculationResult(expression=f"{a} + {b}", result=a + b)


@tool(description="Multiply two numbers")
def multiply(a: float, b: float) -> CalculationResult:
    """Multiply two numbers and return the result."""
    return CalculationResult(expression=f"{a} * {b}", result=a * b)


@tool(description="Reverse a string")
def reverse_text(text: str) -> TextResult:
    """Reverse the characters in a string."""
    return TextResult(original=text, transformed=text[::-1])


# --- Tool Registry ---
# List every tool here. main.py iterates this list to register them with the server.

tools = [add, multiply, reverse_text]
