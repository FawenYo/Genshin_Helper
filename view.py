from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

view = APIRouter()
templates = Jinja2Templates(directory="templates")

# Home Page
@view.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return JSONResponse({"server-status": "Online"})
