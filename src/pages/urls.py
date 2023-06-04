from fastapi import APIRouter

from src.pages import views

url = APIRouter()
url.include_router(router=views.view)
