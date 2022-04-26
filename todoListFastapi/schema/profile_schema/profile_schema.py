from typing import Optional
from pydantic import BaseModel

class profile_schema(BaseModel):
    username: str
    password: str
    class Config:
        schema_extra = {
            "example": {
                "username": "yashkakade",
                "password": "yashkakade",
            }
        }