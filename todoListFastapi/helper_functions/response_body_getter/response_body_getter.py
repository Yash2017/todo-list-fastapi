async def response_body_getter(response):
    body = b""
    async for chunk in response.body_iterator:
        body += chunk
    return body