from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

view = APIRouter()
templates = Jinja2Templates(directory="templates")


# Home Page
@view.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("home.html", context={"request": request})


# Health check
@view.get("/healthz")
async def health() -> JSONResponse:
    """Health check

    Returns:
        JSONResponse: Status message.
    """
    return JSONResponse({"status": "Success", "message": "I'm alive!"})
