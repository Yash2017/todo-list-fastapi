import json
from fastapi import HTTPException
import motor.motor_tornado
from bson import ObjectId
import motor.motor_asyncio
from helper_functions.json_encoder.json_encoder import JSONEncoder
from redis.redis_helper import find_todo_in_redis
from .db_client import get_db_user_collection_client, get_db_todo_collection_client
# replace this with your MongoDB connection string

async def create_user(userInfo):
    try:
        user_collection = await get_db_user_collection_client()
        result = await user_collection.insert_one(userInfo)
        return result
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")

#Can be improved by using find one for future
async def get_user_from_db():
    try:
        user_collection = await get_db_user_collection_client()
        users = []
        users_from_db = user_collection.find({}).max_time_ms(12)
        async for user in users_from_db:
            users.append(JSONEncoder().encode(user))
        return users
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")
        
    

async def get_todo_from_db(user):
    try:
        todo_collection = await get_db_todo_collection_client()
        todos = []
        todo_from_db = todo_collection.find({"owner": user}).max_time_ms(12)
        async for todo in todo_from_db:
            todos.append(JSONEncoder().encode(todo))
        return todos
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def insert_todo(todo_info):
    try:
        todo_collection = await get_db_todo_collection_client()
        result = await todo_collection.insert_one(todo_info)
        return result
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_bson_object_id(todo_id):
    try:
        object_id = ObjectId(todo_id)
        return object_id
    except:
        raise HTTPException(status_code=400, detail="Invalid todo id")


async def find_todo(todo_id, current_user):
    try:
        todo_collection = await get_db_todo_collection_client()
        result = await find_todo_in_redis(current_user, todo_id)
        if result:
            return True
        found_todo = await todo_collection.find_one({"_id": todo_id}, {"_id": 0})
        if not found_todo:
            raise HTTPException(status_code=400, detail="The todo does not exist")
        else: 
            return True
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def update_todo_db(todo_id, updated_data, current_user):
    try:
        todo_collection = await get_db_todo_collection_client()
        todo_id = get_bson_object_id(todo_id)
        await find_todo(todo_id, current_user)
        result = await todo_collection.update_one({"_id": todo_id}, {"$set": updated_data})
        return result
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")
        

async def delete_todo_db(todo_id, current_user):
    try:
        todo_collection = await get_db_todo_collection_client()
        todo_id = get_bson_object_id(todo_id)
        await find_todo(todo_id, current_user)
        result = await todo_collection.delete_one({"_id": todo_id})
        return result
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")

 
