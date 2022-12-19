from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.requests import Request
from fastapi import HTTPException, Header

################################################################################
# Error Handler
################################################################################


def abort(error, msg=None):
    if error == 401:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"})

    elif error == 403:
        raise HTTPException(
            status_code=403,
            detail="Unothorized",
            headers={"WWW-Authenticate": "Basic"})

    elif not msg and error:
        raise HTTPException(
            status_code=error,
            detail="Internal Server Error",
            headers={"WWW-Authenticate": "Basic"})

    elif msg and error:
        raise HTTPException(
            status_code=error,
            detail=msg,
            headers={"WWW-Authenticate": "Basic"})
