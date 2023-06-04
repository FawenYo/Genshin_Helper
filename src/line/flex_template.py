import json
from datetime import datetime

import pytz
from linebot.models import FlexSendMessage

from src.utils.genshin_models import Award

true = True
taipei_timezone = pytz.timezone("Asia/Taipei")


def sign_award(award: Award) -> FlexSendMessage:
    """Sign Award Result

    Args:
        award (Award): Award Object

    Returns:
        FlexSendMessage: Flex Message
    """
    now = datetime.now(taipei_timezone)

    now_text = now.strftime("%Y/%m/%d %H:%M:%S")
    with open("src/line/flex_message_template/sign_award.json") as json_file:
        contents = json.load(json_file)
    contents["hero"]["url"] = award.icon
    contents["body"]["contents"][1]["contents"][1][
        "text"
    ] = f"{award.name} * {award.count}"
    contents["body"]["contents"][3]["contents"][1]["text"] = now_text
    message = FlexSendMessage(alt_text=f"簽到成功！", contents=contents)
    return message
