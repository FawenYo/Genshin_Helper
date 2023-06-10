import pickle

import aiohttp
from fastapi import APIRouter, HTTPException, Request
from linebot import AsyncLineBotApi
from linebot.aiohttp_async_http_client import AiohttpAsyncHttpClient
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from src import config
from src.line import flex_template
from src.line.line_config import parser
from src.utils.genshin_helper import GenshinHelper
from src.utils.genshin_models import DailyReward
from src.utils.logging_util import get_logger

controller = APIRouter()
logger = get_logger()


@controller.post("/callback")
async def callback(request: Request) -> None:
    """LINE Bot Webhook Callback

    Args:
        request (Request): Request Object.

    Raises:
        HTTPException: Signature Invalid
    """
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    # handle webhook body
    try:
        events = parser.parse(body=body.decode(), signature=signature)
        await handle_events(events=events)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameter")


async def handle_events(events) -> None:
    for event in events:
        session, line_bot_api = initialize_linebot_api()
        user_id = event.source.user_id
        profile = await line_bot_api.get_profile(user_id)
        display_name = profile.display_name
        reply_token = event.reply_token

        # 文字訊息
        if isinstance(event.message, TextMessage):
            user_message: str = event.message.text

            logger.info(f"User: {display_name} ({user_id}). Message: {user_message}")

            if user_message == "登入":
                reply_message = TextSendMessage(
                    text="請根據教學方法綁定帳號\nhttps://hackmd.io/@FawenYo/BJJynSE3_"
                )

            elif "/登入 " in user_message:
                cookie = user_message.split("/登入 ")[1]
                try:
                    helper = GenshinHelper(cookies=cookie)
                    result = helper.account_status()

                    if result["retcode"] != 0:
                        logger.error(
                            f"User: {display_name} ({user_id}). Status code: Login failed"
                        )
                        reply_message = TextSendMessage(text="登入失敗，請重新登入！")
                    else:
                        logger.error(
                            f"User: {display_name} ({user_id}). status_code: login success"
                        )
                        try:
                            users = pickle.loads(config.DATABASE.get("users"))
                            logger.debug("Get users from database")
                        except:
                            users = {}
                            logger.debug("Create new users")
                        users[user_id] = cookie
                        config.DATABASE.set("users", pickle.dumps(users))
                        logger.debug("Set user to database")

                        reply_message = TextSendMessage(text="登入成功！ 每天半夜 01:00 自動幫您簽到！")
                except:
                    logger.error(
                        f"User: {display_name} ({user_id}). Status code: Cookies format error"
                    )
                    reply_message = TextSendMessage(text="Cookies 格式錯誤！ 請重新輸入")

            elif user_message == "簽到":
                cookie = find_user_cookie(user_id=user_id)

                if cookie == "":
                    logger.error(
                        f"User: {display_name} ({user_id}). Status code: Not login"
                    )
                    reply_message = TextSendMessage("尚未綁定帳號！")
                else:
                    helper = GenshinHelper(cookies=cookie)
                    award: DailyReward | None = None
                    error_message: str = ""
                    try:
                        award = await helper.claim_daily_reward()
                    except Exception as e:
                        error_message = str(e)
                    finally:
                        reply_message = handle_sign_result(
                            display_name=display_name,
                            user_id=user_id,
                            award=award,
                            error_message=error_message,
                        )
            else:
                reply_message = TextSendMessage("不好意思，目前我還聽不懂你在說什麼呢><")
            await line_bot_api.reply_message(reply_token, reply_message)

        await session.close()


def initialize_linebot_api() -> tuple[aiohttp.ClientSession, AsyncLineBotApi]:
    """Initialize LINE Bot API

    Returns:
        tuple[aiohttp.ClientSession, AsyncLineBotApi]: aiohttp Client Session and AsyncLineBotApi
    """
    session = aiohttp.ClientSession()
    async_http_client = AiohttpAsyncHttpClient(session)
    line_bot_api = AsyncLineBotApi(
        channel_access_token=config.LINE_CHANNEL_ACCESS_TOKEN,
        async_http_client=async_http_client,
    )
    return session, line_bot_api


def find_user_cookie(user_id: str) -> str:
    """Find User Cookies in Redis Database

    Args:
        user_id (str): User's LINE ID

    Returns:
        str: User's Cookies
    """
    users = pickle.loads(config.DATABASE.get("users"))
    if user_id in users:
        cookie = users[user_id]
        return cookie
    else:
        return ""


def handle_sign_result(
    display_name: str,
    user_id: str,
    award: DailyReward | None = None,
    error_message: str = "",
) -> TextMessage | FlexSendMessage:
    """Handle Genshin Daily Sign-in Result

    Args:
        display_name (str): User's LINE Display Name
        user_id (str): User's LINE ID
        award (DailyReward, optional): Daily Sign-in Reward. Defaults to None.
        error_message (str, optional): Error Message. Defaults to "".

    Returns:
        TextMessage|FlexSendMessage: Reply Message
    """
    if award:
        logger.info(f"User: {display_name} ({user_id}). Status code: Sign-in success")
        reply_message = flex_template.sign_award(award=award)
    # Encountered Error when claiming daily sign-in reward
    else:
        logger.error(
            f"User: {display_name} ({user_id}). Exception message: {error_message}"
        )
        reply_message = TextSendMessage(text=f"簽到失敗！\n錯誤原因：{error_message}\n請通知作者")
    return reply_message
