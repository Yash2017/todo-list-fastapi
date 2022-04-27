import json
from turtle import update
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
import tornado.ioloop
import tornado.web
import motor.motor_tornado
import asyncio
from bson import ObjectId
import motor.motor_asyncio
from .jsonEncoder import *

# replace this with your MongoDB connection string
conn_str = "mongodb+srv://yashkakade:yashkakade@bug-tracker.np7pj.mongodb.net/todo-list-fastapi?retryWrites=true&w=majority"
db_str = "todo-list-fastapi"
user_collection_str = "profile"
todo_collection_str = "todo_information"
db = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)[db_str]
user_collection = db[user_collection_str]
todo_collection = db[todo_collection_str]

async def create_user(userInfo):
    result = await user_collection.insert_one(userInfo)
    return result

#Can be improved by using find one for future
async def get_user_from_db():
    users = []
    users_from_db = user_collection.find({}).max_time_ms(12)
    async for user in users_from_db:
        users.append(JSONEncoder().encode(user))
    return users

async def get_todo_from_db(user):
    todos = []
    todo_from_db = todo_collection.find({"owner": user}).max_time_ms(12)
    async for todo in todo_from_db:
        todos.append(JSONEncoder().encode(todo))
    return todos

async def insert_todo(todo_info):
    result = await todo_collection.insert_one(todo_info)
    return result

async def find_todo(todo_id):
    found_todo = await todo_collection.find_one({"_id": ObjectId(todo_id)}, {"_id": 0})
    if not found_todo:
        raise HTTPException(status_code=400, detail="The todo does not exist")
    else: 
        return True

async def update_todo_db(todo_id, updated_data):
    await find_todo(todo_id)
    result = await todo_collection.update_one({"_id": ObjectId(todo_id)}, {"$set": updated_data})
    return result
        

async def delete_todo_db(todo_id):
    await find_todo(todo_id)
    result = await todo_collection.delete_one({"_id": ObjectId(todo_id)})
    return result
 
