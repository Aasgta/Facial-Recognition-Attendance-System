# 🤖 AI-Based Face Recognition Attendance System (FastAPI)

An advanced **AI-powered attendance management system** built using **FastAPI**, **OpenCV**, and **Machine Learning**.  
This web application replaces the traditional attendance methods with a **modern, futuristic dashboard**, allowing subject-wise attendance marking, face recognition, and automatic Excel record generation.

---

## 🚀 Features

- 🎯 **Real-time Face Recognition** using OpenCV  
- 🧍‍♂️ **Student Registration** with automatic data saving  
- 🧠 **AI Model Training** for new faces  
- 📋 **Subject-wise Attendance Marking**  
- 📂 **Automatic CSV/Excel Attendance Reports**  
- 💻 **FastAPI Web Interface**  
- 🎨 **Futuristic UI Theme** — neon glowing, AI-style interface  
- ⚡ **Error-Free and Lightweight** — runs smoothly on local systems  

---

## 🧠 Technologies Used

| Component | Technology |
|------------|-------------|
| **Frontend** | HTML5, CSS3 (Custom AI Theme), Jinja2 Templates |
| **Backend** | FastAPI (Python) |
| **Face Detection** | OpenCV, Haar Cascade Classifier |
| **Data Handling** | Pandas, CSV, Excel |
| **Model Training** | OpenCV LBPH Face Recognizer |
| **Version Control** | Git & GitHub |

---

## 🏗️ Project Structure
fastapi_attendance/
│
├── app/
│ ├── main.py
│ ├── routers/
│ │ ├── register.py
│ │ ├── train.py
│ │ ├── recognize.py
│ │ └── attendance.py
│ ├── services/
│ │ ├── automatic_attendance.py
│ │ └── train_image.
│ │ └── train_image.py
│ ├── templates/
│ │ ├── base.html
│ │ ├── index.html
│ │ ├── register.html
│ │ ├── train.html
│ │ ├── attendance_home.html
│ │ ├── attendance_table.html
│ │ ├── subject_form.html
│ │ └── view_attendance.html
│ └── static/
│ │ └── css/
│ │     └── styles.css
│ ├──data/
│ │ ├──StudentDetails/
│ │ │   └── studentdetails.csv
│ │ │
│ │ ├── Attendance/
│ │ │   └── (Attendance reports by date)
│ │ │
│ │ ├── TrainingImageLabel/
│ │ │   └── trainer.yml
├── haarcascade_frontalface_alt.xml
├── haarcascade_frontalface_default.xml
├── requirements.txt
└── README.md

---

## ⚙️ Installation & Setup Guide

### Step 1️⃣ — Clone the Repository

git clone https://github.com/your-username/fastapi-attendance-system.git
cd fastapi-attendance-system


Step 2️⃣ — Create a Virtual Environment

python -m venv FaceAtt
FaceAtt\Scripts\Activate.ps1      # (Windows)


Step 3️⃣ — Install Dependencies

pip install -r requirements.txt


Step 4️⃣ — Run the FastAPI App

uvicorn app.main:app --reload
Then open your browser and visit:
👉 http://127.0.0.1:8000

---

🧩 How It Works

Register a Student:
Capture student face images and store enrollment details.

Train Model:
Train the face recognition model on stored images.

Mark Attendance (Subject-wise):
Automatically recognize faces through webcam and record attendance in CSV format.

View or Export Records:
Open or download Excel reports anytime.

---

🙌 Credits

Developed by Aashi Gupta 💻
Built with ❤️ using FastAPI, Python, and OpenCV

---

⭐ Show Your Support

If you like this project:
- Give it a ⭐ on GitHub
- Fork it and build your own AI-powered system!

---

📌 “Smart Attendance, Powered by AI — The Future of Education Management.”