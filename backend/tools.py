from langchain.agents import tool
from pydantic import BaseModel, Field
from typing import List

class SQLQuery(BaseModel):
    query: str = Field(description="SQL query to execute")

@tool
def tool(query: str) -> List:
    """Returns string"""
    return ""