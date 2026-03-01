# app/routers/attendance.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import pandas as pd
import os

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/attendance", tags=["Attendance"])

DATA_DIR = Path("data/Attendance")

@router.get("/", response_class=HTMLResponse)
async def attendance_home(request: Request):
    subjects = [d.name for d in DATA_DIR.glob("*") if d.is_dir()]
    return templates.TemplateResponse("attendance_home.html", {"request": request, "subjects": subjects})

@router.get("/subject", response_class=HTMLResponse)
async def subject_form(request: Request):
    return templates.TemplateResponse("subject_form.html", {"request": request, "msg": ""})

@router.post("/subject", response_class=HTMLResponse)
async def start_attendance(request: Request, subject: str = Form(...)):
    from app.services.automatic_attendance import run_recognition_session
    msg = run_recognition_session(subject)
    return templates.TemplateResponse("subject_form.html", {"request": request, "msg": msg})

@router.get("/view/{subject}", response_class=HTMLResponse)
async def view_subject_attendance(request: Request, subject: str):
    subject_dir = DATA_DIR / subject
    if not subject_dir.exists():
        return templates.TemplateResponse("view_attendance.html", {"request": request, "subject": subject, "files": []})

    csv_files = list(subject_dir.glob("*.csv"))
    return templates.TemplateResponse("view_attendance.html", {
        "request": request,
        "subject": subject,
        "files": [f.name for f in csv_files]
    })

@router.get("/download/{subject}/{filename}")
async def download_attendance(subject: str, filename: str):
    file_path = DATA_DIR / subject / filename
    if not file_path.exists():
        return {"error": "File not found"}
    return FileResponse(path=file_path, filename=filename, media_type="text/csv")

@router.get("/view/{subject}/{filename}", response_class=HTMLResponse)
async def open_attendance(request: Request, subject: str, filename: str):
    file_path = DATA_DIR / subject / filename
    if not file_path.exists():
        return templates.TemplateResponse("error.html", {"request": request, "msg": "File not found"})
    df = pd.read_csv(file_path)
    html_table = df.to_html(classes="table table-bordered", index=False)
    return templates.TemplateResponse("attendance_table.html", {
        "request": request,
        "subject": subject,
        "filename": filename,
        "table": html_table
    })