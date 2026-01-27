from dedalus_mcp import tool
from pydantic import BaseModel


class ExampleResult(BaseModel):
    message: str
    value: int


@tool(description="An example tool that demonstrates the basic structure")
def example_tool(input_text: str, multiplier: int = 1) -> ExampleResult:
    """
    An example tool that processes input and returns a result.
    
    Args:
        input_text: A text input to process
        multiplier: A multiplier value (default: 1)
    
    Returns:
        ExampleResult with a message and computed value
    """
    processed_value = len(input_text) * multiplier
    return ExampleResult(
        message=f"Processed: {input_text}",
        value=processed_value,
    )


tools = [example_tool]