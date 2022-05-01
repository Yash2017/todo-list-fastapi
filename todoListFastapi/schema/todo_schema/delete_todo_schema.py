from pydantic import BaseModel
'''
Delete todo schema
'''
class delete_todo_schema(BaseModel):
    id: str
    class Config:
        schema_extra = {
                "id": "Todo Id",
        }
