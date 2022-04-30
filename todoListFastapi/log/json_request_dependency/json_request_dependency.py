from fastapi import Request
from ..get_json_logger.get_json_logger import get_logger
from ..formattor.json_app_logger_formatter import CustomFormatter
from log.request_log_maker.request_log_maker import request_log_maker

formatter = CustomFormatter('%(asctime)s')
logger = get_logger(__name__, formatter)
async def json_request_dependency(request: Request):
    if request.method != "GET":
        request_body = await request.json()
        return logger.info(request.method + ' ' + request.url.path, extra={'extra_info': request_log_maker(request, request_body), 'res': 'false'})
    else:
        return logger.info(request.method + ' ' + request.url.path, extra={'extra_info': request_log_maker(request, "No query as this is a GET request"), 'res': 'false'})

