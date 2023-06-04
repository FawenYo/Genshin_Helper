from fastapi import APIRouter

from src.api import views

url = APIRouter(prefix="/api")
url.include_router(router=views.view)
