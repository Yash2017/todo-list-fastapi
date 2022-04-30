async def request_log_maker(request):
        
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
                    'query': "await request.json()"
                    }
            }
                    