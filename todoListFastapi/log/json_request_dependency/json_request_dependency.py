from fastapi import Request, HTTPException
from ..get_json_logger.get_json_logger import get_logger
from ..formattor.json_app_logger_formatter import CustomFormatter
from log.request_log_maker.request_log_maker import request_log_maker
'''
This method is called when we have to log a request. If it is a not a get request, only then
 I get the request body and pass it to the logger.info method
'''
formatter = CustomFormatter('%(asctime)s')
logger = get_logger(__name__, formatter)
async def json_request_dependency(request: Request):
    try:
        if request.method != "GET":
            request_body = await request.json()
            return logger.info(request.method + ' ' + request.url.path, extra={'extra_info': request_log_maker(request, request_body), 'res': 'false'})
        else:
            return logger.info(request.method + ' ' + request.url.path, extra={'extra_info': request_log_maker(request, "No query as this is a GET request"), 'res': 'false'})
    except:
        raise HTTPException(status_code=500, detail="Logging Error Occurred")


