# app/routers/recognize.py
from fastapi import APIRouter
from app.services.automatic_attendance import run_recognition_session

router = APIRouter(prefix="/recognize", tags=["Recognize"])

@router.get("/")
async def recognize():
    """
    Start the face recognition process for general attendance.
    Saves results in 'data/Attendance/General'.
    """
    msg = run_recognition_session(subject="General", duration_seconds=20, confidence_threshold=70)
    return {"message": msg}