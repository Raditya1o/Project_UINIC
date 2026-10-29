from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
# Import model scikit-learn & mediapipe kamu di sini nanti

app = FastAPI()

# Wajib agar frontend lokal (HTML biasa) bisa akses FastAPI tanpa terhalang CORS
app.middleware("http")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend BISINDO aktif!"}

@app.post("/predict")
async def predict_sign(file: UploadFile = File(...)):
    # 1. Baca gambar yang dikirim dari web uji coba
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # TODO: Masukkan kode OpenCV -> MediaPipe -> Model Scikit-Learn kamu di sini
    # Contoh sementara kita bikin balasan dummy huruf "A"
    detected_letter = "A" 

    return {"status": "success", "letter": detected_letter}