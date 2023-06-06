from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import JSONResponse

from src import config
from src.api import models
from src.utils.genshin_helper import GenshinHelper
from src.utils.genshin_models import DailyReward
from src.utils.logging_util import get_logger

logger = get_logger()

view = APIRouter()


@view.get("/start")
async def api_genshin_sign_in_all(
    background_tasks: BackgroundTasks, token: str
) -> JSONResponse:
    """Start Sign-in job for all users

    Args:
        background_tasks (BackgroundTasks): Background task.
        token (str): API Token.

    Returns:
        JSONResponse: Status message.
    """
    if token != config.TOKEN:
        logger.error(f"Token invalid! Token: {token}")
        return JSONResponse({"status": "Failed", "error_message": "Token invalid!"})

    logger.info("Start sign in job")
    background_tasks.add_task(models.all_daily_sign_in)
    return JSONResponse({"status": "Success", "message": "Job done!"})


@view.post("/genshin/sign_in")
async def api_genshin_sign_in(request: Request) -> JSONResponse:
    """Start Sign-in job

    Args:
        request (Request): User Info.

    Returns:
        JSONResponse: Status message.
    """
    logger.info("Awaiting request body")
    data = await request.json()
    display_name = data.get("display_name")
    user_id = data.get("user_id")
    cookie = data.get("cookie")

    logger.info(f"Start sign in job for {display_name}")
    helper = GenshinHelper(cookies=cookie)
    award: DailyReward | None = None
    try:
        award: DailyReward = await helper.claim_daily_reward()
    except Exception as e:
        logger.error(f"User: {display_name} ({user_id}). Exception message: {e}")
    finally:
        if award:
            message = {
                "status": "Success",
                "reward": {
                    "icon": award.icon,
                    "name": award.name,
                    "amount": award.amount,
                },
            }
        else:
            message = {"status": "Fail", "reward": None}
        return JSONResponse(message)
