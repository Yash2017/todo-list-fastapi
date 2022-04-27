from fastapi import FastAPI
from auth.authorization import *
from todo.main_todo import *

todoListFastapi = FastAPI()

todoListFastapi.include_router(auth)
todoListFastapi.include_router(todo_route)

@todoListFastapi.get("/")
async def root():
    return {"message": "Hello Bigger Todo Application!"}
