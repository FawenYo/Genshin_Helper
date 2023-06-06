import pickle

from linebot import LineBotApi

from src import config
from src.line.controller import handle_sign_result
from src.utils.genshin_helper import GenshinHelper
from src.utils.genshin_models import DailyReward
from src.utils.logging_util import get_logger

logger = get_logger()
line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)


async def all_daily_sign_in() -> None:
    """Daily Sign In"""
    users = pickle.loads(config.DATABASE.get("users"))
    for user_id, cookie in users.items():
        profile = line_bot_api.get_profile(user_id)
        display_name = profile.display_name
        helper = GenshinHelper(cookies=cookie)
        award: DailyReward | None = None
        try:
            award = await helper.claim_daily_reward()
        except Exception as e:
            logger.error(f"User: {display_name} ({user_id}). Exception message: {e}")
        finally:
            reply_message = handle_sign_result(
                display_name=display_name, user_id=user_id, award=award
            )
        # Push Message
        line_bot_api.push_message(user_id, reply_message)
