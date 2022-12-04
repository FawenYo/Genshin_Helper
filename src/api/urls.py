from fastapi import APIRouter

from api import views

url = APIRouter(prefix="/api")
url.include_router(router=views.view)
