import json
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
import tornado.ioloop
import tornado.web
import motor.motor_tornado
import asyncio
from bson import json_util
from bson.json_util import dumps
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

async def do_insert(userInfo):
    result = await user_collection.insert_one(userInfo)
    if not result:
        raise HTTPException(status_code=500, error="Internal Server Error")
    print('result %s' % repr(result.inserted_id))
#Can be improved by using find one for future
async def get_user_from_collection():
    users = []
    async for user in user_collection.find({}):
        users.append(JSONEncoder().encode(user))
    return users

async def get_todo_from_db(user):
    todos = []
    async for todo in todo_collection.find({"owner": user}):
        todos.append(JSONEncoder().encode(todo))
    return todos

async def insert_todo(todo_info):
    result = await todo_collection.insert_one(todo_info)
    if not result:
        raise HTTPException(status_code=500, error="Internal Server Error")
    print('result %s' % repr(result.inserted_id))
