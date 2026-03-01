import os, cv2, numpy as np
from pathlib import Path
from PIL import Image

BASE = Path(__file__).resolve().parents[2]
TRAIN_DIR = BASE / "data" / "TrainingImage"
MODEL_PATH = BASE / "data" / "TrainingImageLabel" / "Trainner.yml"
HAAR_PATH = BASE / "haarcascade_frontalface_default.xml"

def get_images_and_labels(path):
    face_samples = []
    ids = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.lower().endswith(".jpg") or file.lower().endswith(".png"):
                img_path = os.path.join(root, file)
                pil_img = Image.open(img_path).convert('L')
                img_np = np.array(pil_img, 'uint8')
                try:
                    id_ = int(os.path.basename(file).split("_")[1])
                except Exception:
                    continue
                face_samples.append(img_np)
                ids.append(id_)
    return face_samples, ids

def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, ids = get_images_and_labels(str(TRAIN_DIR))
    if len(faces) == 0:
        return "No training images found. Please register students first."
    recognizer.train(faces, np.array(ids))
    os.makedirs(MODEL_PATH.parent, exist_ok=True)
    recognizer.save(str(MODEL_PATH))
    return f"Model trained and saved to {MODEL_PATH}"
