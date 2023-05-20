import pickle

from linebot.models import *

import config
from genshin.helper import Helper
from genshin.models import Account
from line import flex_template
from line.line_config import handler, line_bot_api
from utils.logging_util import get_logger

logger = get_logger()


@handler.add(MessageEvent, message=(TextMessage, LocationMessage))
def handle_message(event) -> None:
    """Event - Message

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#message-event
    """
    user_id = event.source.user_id
    reply_token = event.reply_token

    # 文字訊息
    if isinstance(event.message, TextMessage):
        user_message = event.message.text

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
                    reply_message = TextSendMessage(text="登入失敗，請重新登入！")
                else:
                    try:
                        users = pickle.loads(config.DATABASE.get("users"))
                        logger.info("Get users from database")
                    except:
                        users = {}
                        logger.info("Create new users")
                    users[user_id] = cookie
                    config.DATABASE.set("users", pickle.dumps(users))
                    logger.info("Set user to database")

                    reply_message = TextSendMessage(text="登入成功！ 每天半夜 01:00 自動幫您簽到！")
            except:
                reply_message = TextSendMessage(text="cookies 格式錯誤！ 請重新輸入")

        elif user_message == "簽到":
            cookie = find_user_cookie(user_id=user_id)

            if cookie == "":
                reply_message = TextSendMessage("尚未綁定帳號！")
            else:
                account = Account(cookies=cookie)

                helper = Helper(account=account)
                result = helper.run()

                if result["retcode"] != 0:
                    reply_message = TextSendMessage(text="登入失敗，請重新登入！")
                elif not result["data"]["is_sign"]:
                    reply_message = TextSendMessage(text="簽到失敗！請通知作者！")
                else:
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
