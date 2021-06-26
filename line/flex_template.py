import json
import sys
from datetime import datetime

import pytz
from linebot.models import FlexSendMessage

sys.path.append(".")
from helper import Award

true = True


def sign_award(award: Award) -> FlexSendMessage:
    """Sign Award Result

    Args:
        award (Award): Award Object

    Returns:
        FlexSendMessage: Flex Message
    """
    tz = pytz.timezone("Asia/Taipei")
    now = datetime.now(tz=tz)

    now_text = now.strftime("%Y/%m/%d %H:%M:%S")
    with open("line/flex_message_template/sign_award.json") as json_file:
        contents = json.load(json_file)
    contents["hero"]["url"] = award.icon
    contents["body"]["contents"][1]["contents"][1][
        "text"
    ] = f"{award.name} * {award.count}"
    contents["body"]["contents"][3]["contents"][1]["text"] = now_text
    message = FlexSendMessage(alt_text=f"簽到成功！", contents=contents)
    return message
