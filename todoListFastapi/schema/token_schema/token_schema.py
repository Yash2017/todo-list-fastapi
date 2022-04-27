from typing import Optional
from pydantic import BaseModel

class TokenData(BaseModel):
    username: Optional[str] = None
    class Config:
        schema_extra = {
                "username": "yashkakade",
        }
class Token(BaseModel):
    access_token: str
    token_type: str
    class Config:
        schema_extra = {
                "access_token": "access_token",
                "token_type": "bearer"
        }
