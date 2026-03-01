import os, cv2, csv
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]  # project root /fastapi_attendance
DATA_DIR = BASE / "data"
TRAIN_DIR = DATA_DIR / "TrainingImage"
STUDENT_CSV = DATA_DIR / "StudentDetails" / "studentdetails.csv"
HAAR_PATH = BASE / "haarcascade_frontalface_default.xml"

os.makedirs(TRAIN_DIR, exist_ok=True)
os.makedirs(STUDENT_CSV.parent, exist_ok=True)

def capture_faces(enrollment: str, name: str, max_samples: int = 50):
    if not enrollment or not name:
        return "Enrollment and Name are required."
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        return "Cannot open camera. Make sure webcam is available."
    detector = cv2.CascadeClassifier(str(HAAR_PATH))
    directory = TRAIN_DIR / f"{enrollment}_{name}"
    os.makedirs(directory, exist_ok=True)
    sample = 0
    try:
        while True:
            ret, img = cam.read()
            if not ret:
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                sample += 1
                face_img = gray[y:y+h, x:x+w]
                file_path = directory / f"{name}_{enrollment}_{sample}.jpg"
                cv2.imwrite(str(file_path), face_img)
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow("Capturing (press 'q' to quit)", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if sample >= max_samples:
                break
    finally:
        cam.release()
        cv2.destroyAllWindows()
    # append to studentdetails.csv
    with open(STUDENT_CSV, "a+", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([enrollment, name])
    return f"Saved {sample} images for Enrollment {enrollment}, Name {name}"