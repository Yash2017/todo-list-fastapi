from fastapi import FastAPI
from auth.authorization import *
from todo.mainTodo import *

todoListFastapi = FastAPI()

todoListFastapi.include_router(auth)
todoListFastapi.include_router(todoRoute)

@todoListFastapi.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
