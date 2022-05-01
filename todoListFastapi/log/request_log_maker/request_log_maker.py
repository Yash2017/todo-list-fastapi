'''
Function to return the log in the right format
'''
def request_log_maker(request, request_body):
        return {
            'req': {
                    'url': request.url.path,
                    'headers': {
                                'host': request.headers['host'],
                                'user-agent': request.headers['user-agent'],
                                'accept': request.headers['accept']
                                },
                    'method': request.method,
                    'httpVersion': request.scope['http_version'],
                    'originalUrl': request.url.path,
                    'query': request_body
                    }
            }
                    