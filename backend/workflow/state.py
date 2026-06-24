from typing import TypedDict, Annotated
from pydantic import BaseModel,Field
from langgraph.graph.message import add_messages
from operator import add

class ExtractID(BaseModel):
    order_id : str = Field(description="Extract the order id of the customer from the user query")

class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
    tool_names: Annotated[list[str], add]
    voice_response : str