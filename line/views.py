from fastapi import APIRouter, HTTPException, Request
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from . import message_event
from .line_config import handler

view = APIRouter()


@view.post("/callback")
async def callback(request: Request) -> str:
    """LINE Bot Webhook Callback

    Args:
        request (Request): Request Object.

    Raises:
        HTTPException: Signature Invalid

    Returns:
        str: OK
    """
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    # handle webhook body
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameter")
    return "OK"


@handler.add(MessageEvent, message=(TextMessage, LocationMessage))
def handle_message(event):
    message_event.handle_message(event=event)
