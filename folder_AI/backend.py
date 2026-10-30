from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import cv2
import mediapipe as mp
import numpy as np
import pickle

app = FastAPI()

# Izinkan CORS agar frontend HTML/JS bisa mengakses backend Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model BISINDO
model_dict = pickle.load(open('model_bisindo.p', 'rb'))
model = model_dict

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2)

CONFIDENCE_THRESHOLD = 0.10

@app.post("/predict")
async def predict_frame(file: UploadFile = File(...)):
    # Baca file gambar yang dikirim dari web frontend
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is None:
        return {"status": "error", "message": "Frame tidak valid"}

    # Balik frame seperti cermin
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    detected_char = ""
    status_text = "Tunjukkan tangan..."

    if results.multi_hand_landmarks:
        data_aux = []
        for hand_landmarks in results.multi_hand_landmarks:
            for lm in hand_landmarks.landmark:
                data_aux.append(lm.x)
                data_aux.append(lm.y)
                
        if len(results.multi_hand_landmarks) == 1:
            data_aux.extend([0.0] * 42)
            
        if len(data_aux) == 84:
            input_data = np.asarray(data_aux).reshape(1, -1)
            probabilities = model.predict_proba(input_data)[0]
            max_prob = np.max(probabilities)
            prediction = model.predict(input_data)
            
            if max_prob >= CONFIDENCE_THRESHOLD:
                detected_char = prediction[0]
                status_text = f"Terdeteksi: {detected_char}"
            else:
                status_text = "Keyakinan rendah..."

    return {
        "status": "success",
        "letter": detected_char,
        "message": status_text
    }