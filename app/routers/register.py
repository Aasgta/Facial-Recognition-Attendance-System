from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.take_image import capture_faces

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/register", tags=["register"])

@router.get("/", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "msg": ""})

@router.post("/", response_class=HTMLResponse)
async def post_register(request: Request, enrollment: str = Form(...), name: str = Form(...)):
    # This blocks while capturing images from webcam (works if server has camera)
    msg = capture_faces(enrollment.strip(), name.strip())
    return templates.TemplateResponse("register.html", {"request": request, "msg": msg})