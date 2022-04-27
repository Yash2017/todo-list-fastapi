import profile
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from schema.todo_schema.todo_schema import todo_schema
from schema.todo_schema.todo_schema import input_todo_schema
from .dependencies import *
from db.db import *
from schema.profile_schema.profile_schema import profile_schema
from dependencies import get_current_active_user

todoRoute = APIRouter(
    prefix="/todo",
    tags=["todo"],
    responses={404: {"description": "Not found"}},
)

@todoRoute.post("/create-todo")
async def create_todo(input_todo:todo_schema, current_user = Depends(get_current_user)):
    input_todo.completed = False
    input_todo.owner = current_user
    todo_info = jsonable_encoder(input_todo)
    await insert_todo(todo_info)
    return {"Message": "User Account Created"}

@todoRoute.get("/get-todo")
async def get_todo(current_user = Depends(get_current_user)):
    todos = await get_todo_from_db(current_user)
    if todos:
        return todos
    else:
        return {"Message": "You don't have any todo tasks"}

#@todoRoute.put("/update-todo")
#async def update_todo()
    