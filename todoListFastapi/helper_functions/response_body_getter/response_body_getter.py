from fastapi import HTTPException
async def response_body_getter(response):
    try:
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        return body
    except:
        raise HTTPException(status_code=500, detail="Could not get the body of the response")
