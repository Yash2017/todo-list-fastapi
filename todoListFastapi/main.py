from fastapi import FastAPI, Request, Response
from auth.authorization import *
from todo.main_todo import *
from log.formattor.json_app_logger_formatter import CustomFormatter
from log.get_json_logger.get_json_logger import get_logger
from log.response_log_maker.response_log_maker import response_log_maker
from helper_functions.response_body_getter.response_body_getter import response_body_getter
from starlette.background import BackgroundTask

formatter = CustomFormatter('%(asctime)s')
logger = get_logger(__name__, formatter)

todoListFastapi = FastAPI()

todoListFastapi.include_router(auth)
todoListFastapi.include_router(todo_route)

async def write_log_data(response, response_body):
    logger.info("This is the response", extra={'extra_info': response_log_maker(response, response_body)})

@todoListFastapi.middleware("http")
async def log_request(request: Request, call_next):
    response = await call_next(request)
    response_body = await response_body_getter(response)
    new_response = Response(content=response_body, status_code=response.status_code, 
        headers=dict(response.headers), media_type=response.media_type)
    new_response.background = BackgroundTask(write_log_data, new_response, response_body)
    return new_response

@todoListFastapi.get("/")
async def root():
    return {"message": "Hello Bigger Todo Application!"}
