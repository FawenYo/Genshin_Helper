from fastapi import APIRouter

from . import views

url = APIRouter(prefix="/line")
url.include_router(router=views.view)
