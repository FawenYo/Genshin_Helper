import os

import redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

USER_AGENT: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
LINE_CHANNEL_ACCESS_TOKEN: str = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET: str = os.getenv("LINE_CHANNEL_SECRET")

DATABASE = redis.Redis.from_url(os.getenv("REDIS_URL"))

TOKEN = os.getenv("TOKEN")
