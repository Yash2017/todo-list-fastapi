from fastapi import FastAPI, Request, Response
from auth.authorization import *
from todo.main_todo import *
from helper_functions.response_body_getter.response_body_getter import response_body_getter
from log.json_request_dependency.json_request_dependency import json_request_dependency
from starlette.background import BackgroundTask
from log.json_response_dependency.json_response_dependency import json_response_dependency

todoListFastapi = FastAPI(dependencies=[Depends(json_request_dependency)])

todoListFastapi.include_router(auth)
todoListFastapi.include_router(todo_route)

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
