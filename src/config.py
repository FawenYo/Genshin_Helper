import os

import redis

USER_AGENT: str = os.getenv("USER_AGENT")
LINE_CHANNEL_ACCESS_TOKEN: str = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET: str = os.getenv("LINE_CHANNEL_SECRET")

DATABASE = redis.Redis(
    host=os.getenv("REDIS_URL"),
    port=os.getenv("REDIS_PORT"),
    password=os.getenv("REDIS_PASSWORD"),
    db=0,
    ssl=True,
)

TOKEN = os.getenv("TOKEN")
