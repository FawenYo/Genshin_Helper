import json
from datetime import datetime

from linebot.models import FlexSendMessage

from genshin.helper import Award

true = True


def sign_award(award: Award) -> FlexSendMessage:
    """Sign Award Result

    Args:
        award (Award): Award Object

    Returns:
        FlexSendMessage: Flex Message
    """
    now = datetime.now()

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
