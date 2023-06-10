from linebot import WebhookParser

from src import config

parser = WebhookParser(channel_secret=config.LINE_CHANNEL_SECRET)
