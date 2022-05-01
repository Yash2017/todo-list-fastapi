import json, logging
'''
Json formattor that adds the correct format to the logs and returns the log to the log file
'''
def get_response_log(record):
    json_obj = [{
                'todoListFastapi': {
                    'log': {
                        'level': record.levelname,
                        'type': 'access',
                        'timestamp': record.asctime,
                        'message': record.message
                        },
                'res': record.extra_info['res'],
                    }
                }]
    return json_obj

def get_request_log(record):
    json_obj = [{
                'todoListFastapi': {
                    'log': {
                        'level': record.levelname,
                        'type': 'access',
                        'timestamp': record.asctime,
                        'message': record.message
                        },
                'req': record.extra_info['req'],
                    }
                }]

    return json_obj


class CustomFormatter(logging.Formatter):
    def __init__(self, formatter):
        logging.Formatter.__init__(self, formatter)
    
    def format(self, record):
        logging.Formatter.format(self, record)
        if record.res == "true":
            return json.dumps(get_response_log(record), indent=2)
        else:
            return json.dumps(get_request_log(record), indent=2)