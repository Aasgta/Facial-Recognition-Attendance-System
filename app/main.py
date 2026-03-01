# app/main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

# ----------------------------
# Project Directory Setup
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent  # app/
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# ----------------------------
# Initialize FastAPI App
# ----------------------------
app = FastAPI(title="Face Recognition Attendance System")

# ----------------------------
# Mount Static Files
# ----------------------------
if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# ----------------------------
# Setup Jinja2 Templates
# ----------------------------
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ----------------------------
# Import Routers
# ----------------------------
from app.routers import register, train, recognize, attendance

# ----------------------------
# Include Routers
# ----------------------------
app.include_router(register.router)
app.include_router(train.router)
app.include_router(recognize.router)
app.include_router(attendance.router)

# ----------------------------
# Root Route (Homepage)
# ----------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Renders the homepage with navigation to all main functions.
    """
    return templates.TemplateResponse("index.html", {"request": request})

# ----------------------------
# Health Check Route (optional)
# ----------------------------
@app.get("/ping")
async def ping():
    return {"status": "ok", "message": "FastAPI attendance system running successfully."}