from pydantic import BaseModel
from typing import Any, Dict, List

class ToolRequest(BaseModel):
    name: str
    arguments: Dict[str, Any]

class ToolResponse(BaseModel):
    tool_name: str
    result: Any
    error: str = None
