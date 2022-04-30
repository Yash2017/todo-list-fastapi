from ..get_json_logger.get_json_logger import get_logger
from ..formattor.json_app_logger_formatter import CustomFormatter
from log.response_log_maker.response_log_maker import response_log_maker

formatter = CustomFormatter('%(asctime)s')
logger = get_logger(__name__, formatter)
async def json_response_dependency(response, response_body):
    logger.info("This is the response", extra={'extra_info': response_log_maker(response, response_body), 'res':'true'})

