import sys

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from . import models

sys.path.append(".")

import config

view = APIRouter()


@view.get("/start")
async def start(token: str = "") -> JSONResponse:
    """Start Sign in job

    Args:
        token (str, optional): API token. Defaults to "".

    Returns:
        JSONResponse: Status message.
    """
    if token != config.TOKEN:
        return JSONResponse({"status": "Failed", "error_message": "Token invalid!"})

    models.daily_sign_in()
    return JSONResponse({"status": "Success", "message": "Job done!"})
