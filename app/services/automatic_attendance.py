# app/services/automatic_attendance.py
import os
import cv2
import pandas as pd
import datetime
import time
from pathlib import Path

# ----------------------------
# Paths Setup
# ----------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "data/TrainingImageLabel" / "Trainner.yml"
STUDENT_CSV = BASE_DIR / "data/StudentDetails" / "studentdetails.csv"
HAAR_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
ATT_DIR = BASE_DIR / "data/Attendance"
ATT_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Function: run_recognition_session
# ----------------------------
def run_recognition_session(subject: str, duration_seconds: int = 20, confidence_threshold: int = 70):
    """
    Runs a real-time face recognition session using LBPH algorithm.
    Saves recognized students' attendance under the given subject name.
    """
    if not os.path.exists(MODEL_PATH):
        return "❌ No trained model found. Please train the model first."
    if not os.path.exists(STUDENT_CSV):
        return "❌ No student details found. Please register students first."

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(str(MODEL_PATH))
    face_cascade = cv2.CascadeClassifier(HAAR_PATH)
    students_df = pd.read_csv(STUDENT_CSV)

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        return "❌ Unable to access the camera. Check webcam permissions."

    start = time.time()
    recognized = []

    while True:
        ret, frame = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            id_pred, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if conf < confidence_threshold:
                match = students_df.loc[students_df["Enrollment"] == id_pred, "Name"].values
                name = match[0] if len(match) else f"ID {id_pred}"
                recognized.append((id_pred, name))
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"{name}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 2)
                cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

        cv2.imshow("Face Recognition - Press ESC to stop", frame)
        if cv2.waitKey(30) & 0xFF == 27 or time.time() - start > duration_seconds:
            break

    cam.release()
    cv2.destroyAllWindows()

    if not recognized:
        return f"⚠️ No faces recognized for subject: {subject}"

    # Remove duplicates and save attendance
    df_att = pd.DataFrame(recognized, columns=["Enrollment", "Name"]).drop_duplicates(subset=["Enrollment"])
    subject_dir = ATT_DIR / subject.replace(" ", "_")
    subject_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{subject}_{timestamp}.csv"
    save_path = subject_dir / filename
    df_att.to_csv(save_path, index=False)

    return f"✅ Attendance saved successfully for subject '{subject}'\n📁 File: {save_path}"