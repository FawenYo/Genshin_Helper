from fastapi import APIRouter

from . import views

url = APIRouter()
url.include_router(router=views.view)
