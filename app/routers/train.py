from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.train_image import train_model

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/train", tags=["train"])

@router.get("/", response_class=HTMLResponse)
async def get_train(request: Request):
    msg = train_model()
    return templates.TemplateResponse("train.html", {"request": request, "msg": msg})