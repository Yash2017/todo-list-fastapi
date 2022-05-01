import os
from dotenv import load_dotenv
import json
from .redis_client import get_redis_client
from fastapi import HTTPException

load_dotenv()
TIME_TO_LIVE_SECOND = int(os.environ.get("TIME_TO_LIVE_SECOND"))

#This function gets the todo information for the current user
async def get_redis_value(current_user):
    try:
        redis = await get_redis_client()
        redis_todo_value = await redis.get(current_user)
        if redis_todo_value:
            value = json.loads(redis_todo_value)
            return value
        else:
            return False
    except:
        raise HTTPException(status_code=500, detail="Redis Server Error. Could not connect to the server")

#This function sets the todo information for the current user
async def set_redis_value(current_user, todo_data):
    redis = await get_redis_client()
    try:
        await redis.set(current_user, json.dumps(todo_data))
        await redis.expire(current_user, TIME_TO_LIVE_SECOND)
    except:
        raise HTTPException(status_code=500, detail="Could Not Save Data To Redis Server")

#This function finds a todo in the redis using the current user key value
async def find_todo_in_redis(current_user, todo_id):
    try:
        redis_todo_value = await get_redis_value(current_user)
        if redis_todo_value:
            for todo in redis_todo_value:
                if str(todo_id) == todo["_id"]:
                    return True
            return False
        else:
            return False
    except:
        raise HTTPException(status_code=500, detail="Redis Server Error. Could not connect to the server")

#This function is simply used to check if a user is present in the user_list key
async def get_user_from_redis():
    try:
        redis = await get_redis_client()
        redis_user_list = await redis.get("user_list")
        if redis_user_list:
            user_list = json.loads(redis_user_list)
            return user_list
        else:
            return False
    except:
        raise HTTPException(status_code=500, detail="Redis Server Error. Could not connect to the server")

#Used to set the user_list key which contains a list of all the users
async def set_user_value(user_value):
    try:
        redis = await get_redis_client()
        await redis.set("user_list", json.dumps(user_value))
        await redis.expire("user_list", TIME_TO_LIVE_SECOND)
    except:
        raise HTTPException(status_code=500, detail="Could Not Save Data To Redis Server")



