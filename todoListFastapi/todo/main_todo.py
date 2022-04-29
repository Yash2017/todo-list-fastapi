import profile
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from schema.todo_schema.todo_schema import todo_schema
from schema.todo_schema.update_todo_schema import update_todo_schema
from schema.todo_schema.delete_todo_schema import delete_todo_schema
from redis.redis_helper import get_redis_value
from redis.redis_helper import set_redis_value
from empty_checker.empty_checker import empty_checker
from .dependencies import get_current_user
from db.db import *

todo_route = APIRouter(
    prefix="/todo",
    tags=["todo"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_user)],
)

@todo_route.post("/create-todo")
async def create_todo(input_todo:todo_schema, current_user = Depends(get_current_user)):
    empty_checker(input_todo.title, "Title")
    empty_checker(input_todo.description, "Description")
    input_todo.completed = False
    input_todo.owner = current_user
    todo_info = jsonable_encoder(input_todo)
    result = await insert_todo(todo_info)
    if not result:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"Message": "Todo Created"}

@todo_route.get("/get-todo")
async def get_todo(current_user = Depends(get_current_user)):
    redis_todo_data = await get_redis_value(current_user)
    if redis_todo_data:
        print(redis_todo_data)
        return redis_todo_data
    todos = await get_todo_from_db(current_user)
    await set_redis_value(current_user, todos)
    if todos:
        return todos
    else:
        return {"Message": "You don't have any todo tasks"}

@todo_route.put("/update-todo")
async def update_todo(update_todo:update_todo_schema, current_user = Depends(get_current_user)):
    empty_checker(update_todo.id, "Id")
    update_todo_id = update_todo.id
    json_update_todo = jsonable_encoder(update_todo)
    json_update_todo.pop("id")
    result = await update_todo_db(update_todo_id, json_update_todo, current_user)
    if not result:
        raise HTTPException(status_code=500, detail="Could Not Find the Document")
    return {"Message": "Todo Updated"}

@todo_route.delete("/delete-todo")
async def delete_todo(delete_todo:delete_todo_schema, current_user = Depends(get_current_user)):
    empty_checker(delete_todo.id, "Id")
    json_delete_todo = delete_todo.id
    result = await delete_todo_db(json_delete_todo, current_user)
    if not result:
        raise HTTPException(status_code=500, detail="Could Not Find the Document")
    return {"Message": "Todo Deleted"}