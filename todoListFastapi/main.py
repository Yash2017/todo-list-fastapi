from fastapi import FastAPI, Request, Response
from auth.authorization import *
from todo.main_todo import *
from helper_functions.response_body_getter.response_body_getter import response_body_getter
from starlette.background import BackgroundTask
from log.json_response_dependency.json_response_dependency import json_response_dependency
from db.db_client import connect_db, close_db
from redis.redis_client import make_redis_client, close_redis_client

todoListFastapi = FastAPI()
todoListFastapi.include_router(auth)
todoListFastapi.include_router(todo_route)

#todoListFastapi.add_event_handler("startup", connect_db, make_redis_client)
#todoListFastapi.add_event_handler("shutdown", close_db)

@todoListFastapi.on_event("startup")
async def startup_event():
    await connect_db()
    await make_redis_client()

@todoListFastapi.on_event("shutdown")
async def startup_event():
    await close_db()
    await close_redis_client()

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
