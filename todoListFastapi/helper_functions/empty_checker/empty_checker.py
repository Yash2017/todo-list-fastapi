from fastapi import HTTPException
def empty_checker(input_string, message):
    if input_string == "":
        raise HTTPException(status_code=400, detail=f"{message} cannot be empty")