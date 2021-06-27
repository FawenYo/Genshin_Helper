import sys

from linebot import LineBotApi, WebhookHandler

sys.path.append(".")
import config

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)
