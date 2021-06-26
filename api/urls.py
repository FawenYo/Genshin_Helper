import pickle
import sys

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from linebot import LineBotApi
from linebot.models import *

sys.path.append(".")

import config
from account import Account
from helper import Helper
from line import flex_template

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
api = APIRouter()


@api.get("/api/start")
async def start(token: str = "") -> JSONResponse:
    """Start Daily sign

    Args:
        token (str, optional): API token. Defaults to "".

    Returns:
        JSONResponse: Status message.
    """
    if token != config.TOKEN:
        return JSONResponse({"status": "Failed", "error_message": "Token invalid!"})

    users = pickle.loads(config.DATABASE.get("users"))

    for user_id, cookie in users.items():
        account = Account(cookies=cookie)

        helper = Helper(account=account)
        result = helper.run()

        # Failed to login
        if result["retcode"] != 0:
            reply_message = TextSendMessage(text="登入失敗，請重新綁定帳號！")
            line_bot_api.push_message(user_id, reply_message)

        # Failed to sign
        elif not result["data"]["is_sign"]:
            reply_message = TextSendMessage(text="簽到失敗！ 請通知作者！")
            line_bot_api.push_message(user_id, reply_message)

        # Successfully signed
        else:
            total_sign_day = result["data"]["total_sign_day"]
            award = helper.awards[total_sign_day]

            # Push result to LINE Bot
            reply_message = flex_template.sign_award(award=award)
            line_bot_api.push_message(user_id, reply_message)
    return JSONResponse({"status": "Success", "message": "Job done!"})
