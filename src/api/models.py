import pickle

from linebot import LineBotApi
from linebot.models import *

import config
from genshin.helper import Helper
from genshin.models import Account
from line import flex_template

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)


def daily_sign_in() -> None:
    """Daily Sign In"""
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
