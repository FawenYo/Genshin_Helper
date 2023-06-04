from fastapi import APIRouter

from src.line import controller

url = APIRouter(prefix="/line")
url.include_router(router=controller.controller)
