import json
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
import tornado.ioloop
import tornado.web
import motor.motor_tornado
import asyncio
from bson import json_util
import motor.motor_asyncio


# replace this with your MongoDB connection string
conn_str = "mongodb+srv://yashkakade:yashkakade@bug-tracker.np7pj.mongodb.net/todo-list-fastapi?retryWrites=true&w=majority"
db_str = "todo-list-fastapi"
collection_str = "profile"
db = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)[db_str]
collection = db[collection_str]

async def do_insert(userInfo):
    result = await collection.insert_one(userInfo)
    if not result:
        raise HTTPException(status_code=500, error="Internal Server Error")
    print('result %s' % repr(result.inserted_id))

async def get_user_from_collection():
    users = []
    async for user in collection.find({}, {'_id':0}):
        users.append(jsonable_encoder(user))
    return users

