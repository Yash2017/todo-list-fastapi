from typing import Optional
from pydantic import BaseModel
"""
Update todo schema
"""
class update_todo_schema(BaseModel):
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    class Config:
        schema_extra = {
                "title": "Updated Homeword",
                "description": "Updated Description",
                "completed": "false"
        }
