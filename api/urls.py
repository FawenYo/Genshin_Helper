from fastapi import APIRouter

from . import views

url = APIRouter(prefix="/api")
url.include_router(router=views.view)
