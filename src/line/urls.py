from fastapi import APIRouter

from line import controller

url = APIRouter(prefix="/line")
url.include_router(router=controller.controller)
