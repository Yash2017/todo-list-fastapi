from dataclasses import Field
from typing import Optional
from pydantic import BaseModel

class delete_todo_schema(BaseModel):
    id: str
    class Config:
        schema_extra = {
                "id": "Todo Id",
        }
