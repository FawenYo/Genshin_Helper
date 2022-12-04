from fastapi import APIRouter

from pages import views

url = APIRouter()
url.include_router(router=views.view)
