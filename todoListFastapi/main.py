from fastapi import FastAPI, Request, Response
from auth.authorization import *
from todo.main_todo import *
from helper_functions.response_body_getter.response_body_getter import response_body_getter
from starlette.background import BackgroundTask
from log.json_response_dependency.json_response_dependency import json_response_dependency
from db.db_client import connect_db, close_db
from redis.redis_client import make_redis_client, close_redis_client

#Here we include the auth and the todo_route
todoListFastapi = FastAPI()
todoListFastapi.include_router(auth)
todoListFastapi.include_router(todo_route)

#We initialize both redis and the db on startup
@todoListFastapi.on_event("startup")
async def startup_event():
    await connect_db()
    await make_redis_client()

#We shutdown redis and the db on shutdown
@todoListFastapi.on_event("shutdown")
async def startup_event():
    await close_db()
    await close_redis_client()

'''We add a middleware that is used to log the response. This is essential as I wanted the resposnse body 
which is hard to get in a dependency
'''
@todoListFastapi.middleware("http")
async def log_request(request: Request, call_next):
    response = await call_next(request)
    response_body = await response_body_getter(response)
    new_response = Response(content=response_body, status_code=response.status_code, 
        headers=dict(response.headers), media_type=response.media_type)
    new_response.background = BackgroundTask(json_response_dependency, new_response, response_body)
    return new_response

@todoListFastapi.get("/")
async def root():
    return {"message": "Hello Bigger Todo Application!"}
