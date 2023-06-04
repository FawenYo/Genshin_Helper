from fastapi import APIRouter
from fastapi.responses import JSONResponse

import config
from api import models
from utils.logging_util import get_logger

logger = get_logger()

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
        logger.error(f"Token invalid! Token: {token}")
        return JSONResponse({"status": "Failed", "error_message": "Token invalid!"})

    logger.info("Start sign in job")
    await models.daily_sign_in()
    return JSONResponse({"status": "Success", "message": "Job done!"})
