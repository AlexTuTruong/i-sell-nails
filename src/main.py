"""Main module which holds FastAPI app"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api import routes

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    """Loads index.html"""
    context = {'request': request}
    return templates.TemplateResponse("index.html", context)

app.include_router(routes.router)
