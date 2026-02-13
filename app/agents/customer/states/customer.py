from pydantic import BaseModel
from typing import Annotated, List
from langgraph.graph.message import add_messages
from langchain.messages import AnyMessage


class CustomerState(BaseModel):
    messages: Annotated[List[AnyMessage], add_messages]
    error: bool = False
    error_message: str = ''
