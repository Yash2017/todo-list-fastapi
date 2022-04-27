from dataclasses import Field
from typing import Optional
from pydantic import BaseModel

class update_todo_schema(BaseModel):
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    class Config:
        schema_extra = {
                "title": "Updated Homeword",
                "description": "Updated Description",
        }
