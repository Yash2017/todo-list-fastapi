from fastapi import FastAPI, Request, Response
from fastapi.routing import APIRoute
from typing import Callable
from ..get_json_logger.get_json_logger import get_logger
from ..formattor.json_app_logger_formatter import CustomFormatter
from log.request_log_maker.request_log_maker import request_log_maker
formatter = CustomFormatter('%(asctime)s')
logger = get_logger(__name__, formatter)
async def log_dependency(request: Request):
    #print(await request.json())
    logger.info(request.method + ' ' + request.url.path, extra={'extra_info': request_log_maker(request), 'req': 'true'})

