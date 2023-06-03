import pickle

from fastapi import APIRouter, HTTPException, Request
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import config
from line import flex_template
from line.line_config import handler, line_bot_api
from utils.genshin_models import Account
from utils.helper import Helper
from utils.logging_util import get_logger

controller = APIRouter()
logger = get_logger()


@controller.post("/callback")
async def callback(request: Request) -> str:
    """LINE Bot Webhook Callback

    Args:
        request (Request): Request Object.

    Raises:
        HTTPException: Signature Invalid

    Returns:
        str: OK
    """
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    # handle webhook body
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameter")
    return "OK"


@handler.add(MessageEvent, message=(TextMessage,))
def handle_message(event) -> None:
    """Event - Message

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#message-event
    """
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    display_name = profile.display_name
    reply_token = event.reply_token

    # 文字訊息
    if isinstance(event.message, TextMessage):
        user_message = event.message.text

        logger.info(f"User: {display_name} ({user_id}). message: {user_message}")

        if user_message == "登入":
            reply_message = TextSendMessage(
                text="請根據教學方法綁定帳號\nhttps://hackmd.io/@FawenYo/BJJynSE3_"
            )

        elif "/登入 " in user_message:
            cookie = user_message.split("/登入 ")[1]
            try:
                account = Account(cookies=cookie)

                helper = Helper(account=account)
                result = helper.account_status()

                if result["retcode"] != 0:
                    logger.error(
                        f"User: {display_name} ({user_id}). status_code: login failed"
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
                    f"User: {display_name} ({user_id}). status_code: cookies format error"
                )
                reply_message = TextSendMessage(text="Cookies 格式錯誤！ 請重新輸入")

        elif user_message == "簽到":
            cookie = find_user_cookie(user_id=user_id)

            if cookie == "":
                logger.error(
                    f"User: {display_name} ({user_id}). status_code: not login"
                )
                reply_message = TextSendMessage("尚未綁定帳號！")
            else:
                account = Account(cookies=cookie)

                helper = Helper(account=account)
                result = helper.run()

                if result["retcode"] != 0:
                    logger.error(
                        f"User: {display_name} ({user_id}). status_code: login failed"
                    )
                    reply_message = TextSendMessage(text="登入失敗，請重新登入！")
                elif not result["data"]["is_sign"]:
                    logger.error(
                        f"User: {display_name} ({user_id}). status_code: sign failed"
                    )
                    reply_message = TextSendMessage(text="簽到失敗！請通知作者！")
                else:
                    logger.info(
                        f"User: {display_name} ({user_id}). status_code: sign success"
                    )
                    total_sign_day = result["data"]["total_sign_day"]
                    award = helper.awards[total_sign_day]

                    reply_message = flex_template.sign_award(award=award)
        else:
            reply_message = TextSendMessage("不好意思，目前我還聽不懂你在說什麼呢><")
        line_bot_api.reply_message(reply_token, reply_message)


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
