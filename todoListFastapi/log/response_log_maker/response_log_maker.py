

import re
import json
def response_log_maker(response, response_body):
        return {
            'res': {
                    'statusCode': response.status_code, 
                    'body': json.loads(response_body.decode('utf-8'))
                    }
            }