from dataclasses import Field
from typing import Optional
from pydantic import BaseModel

class todo_schema(BaseModel):
    title: str
    description: str
    owner: Optional[str] = ""
    completed: Optional[bool] = False
    class Config:
        schema_extra = {
                "title": "Homework",
                "description": "Computer Homework",
                "owner": "yash",
                "completed": False
        }

class input_todo_schema(BaseModel):
    title: str
    description: str
    class Config:
        schema_extra = {
                "title": "Homework",
                "description": "Computer Homework",
        }
