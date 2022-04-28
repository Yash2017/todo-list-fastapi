from fastapi import HTTPException
import motor.motor_tornado
from bson import ObjectId
import motor.motor_asyncio
from .jsonEncoder import *
from redis.redis_helper import find_todo_in_redis

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

def get_bson_object_id(todo_id):
    try:
        object_id = ObjectId(todo_id)
        return object_id
    except:
        raise HTTPException(status_code=400, detail="Invalid todo id")


async def find_todo(todo_id, current_user):
    result = await find_todo_in_redis(current_user, todo_id)
    if result:
        return True
    found_todo = await todo_collection.find_one({"_id": todo_id}, {"_id": 0})
    if not found_todo:
        raise HTTPException(status_code=400, detail="The todo does not exist")
    else: 
        return True

async def update_todo_db(todo_id, updated_data, current_user):
    todo_id = get_bson_object_id(todo_id)
    await find_todo(todo_id, current_user)
    result = await todo_collection.update_one({"_id": todo_id}, {"$set": updated_data})
    return result
        

async def delete_todo_db(todo_id, current_user):
    todo_id = get_bson_object_id(todo_id)
    await find_todo(todo_id, current_user)
    result = await todo_collection.delete_one({"_id": todo_id})
    return result
 
