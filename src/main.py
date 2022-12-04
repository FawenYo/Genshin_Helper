import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.urls import url as api_url
from line.urls import url as line_url
from pages.urls import url as page_url

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
# View
app.include_router(page_url)
# LINE Bot
app.include_router(line_url)
# REST API
app.include_router(api_url)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        log_level="info",
        access_log=True,
        use_colors=True,
        reload=True,
    )
