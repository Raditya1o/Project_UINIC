import cv2
import mediapipe as mp
import numpy as np
import pickle
import time

# Load model yang sudah dilatih
model_dict = pickle.load(open('model_bisindo.p', 'rb'))
model = model_dict

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# ==========================================
# VARIABEL UNTUK FITUR TAHAN & RANGKAI KATA
# ==========================================
current_word = ""               # Menyimpan kalimat/kata yang sedang dirangkai
last_predicted_char = ""        # Huruf yang sedang dideteksi saat ini
hold_start_time = None          # Waktu awal saat jari mulai ditahan
HOLD_DURATION = 2.0             # Durasi tahan dalam detik (bisa diubah jadi 2-5 detik)
CONFIDENCE_THRESHOLD = 0.10     # Batas minimum keyakinan model
# ==========================================

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Balik frame seperti cermin agar natural
    frame = cv2.flip(frame, 1)
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    display_status = "Tunjukkan tangan..."

    if results.multi_hand_landmarks:
        data_aux = []
        
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
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
            detected_char = prediction[0]
            
            if max_prob >= CONFIDENCE_THRESHOLD:
                # Jika huruf yang terdeteksi sama dengan frame sebelumnya
                if detected_char == last_predicted_char:
                    if hold_start_time is None:
                        hold_start_time = time.time() # Mulai hitung waktu tahan
                    else:
                        elapsed_time = time.time() - hold_start_time
                        remaining_time = max(0, HOLD_DURATION - elapsed_time)
                        
                        display_status = f"Tahan [{detected_char}]: {remaining_time:.1f}s"
                        
                        # Jika waktu tahan sudah melewati durasi yang ditentukan (misal 2 detik)
                        if elapsed_time >= HOLD_DURATION:
                            current_word += detected_char # Simpan/tambahkan ke kata
                            print(f"Huruf disimpan: {detected_char}")
                            # Reset timer agar tidak langsung menyimpan huruf yang sama berulang-ulang
                            hold_start_time = None 
                else:
                    # Jika hurufnya berubah, reset timer untuk huruf baru
                    last_predicted_char = detected_char
                    hold_start_time = time.time()
                    display_status = f"Terdeteksi: {detected_char}"
            else:
                display_status = "Keyakinan rendah..."
                hold_start_time = None
    else:
        # Jika tangan tidak ada di frame, reset
        last_predicted_char = ""
        hold_start_time = None
        display_status = "Tunjukkan tangan..."

    # ==========================================
    # TAMPILKAN ANTARMUKA DI LAYAR
    # ==========================================
    # Kotak background untuk teks agar mudah dibaca
    cv2.rectangle(frame, (0, 0), (640, 120), (50, 50, 50), -1)
    
    # Status proses penahanan jari
    cv2.putText(frame, f"Status: {display_status}", (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
    
    # Menampilkan kata/kalimat yang sudah dirangkai
    cv2.putText(frame, f"Kata: {current_word}", (20, 90), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Petunjuk tombol bantuan di bawah
    cv2.putText(frame, "Tekan 'SPACE' untuk spasi | 'BACKSPACE' hapus | 'Q' keluar", (20, 450), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow('Perangkai Kata BISINDO', frame)
    
    key = cv2.waitKey(1) & 0xFF
    # Tekan 'q' untuk keluar
    if key == ord('q'):
        break
    # Tekan 'SPACE' untuk menambahkan spasi antar kata
    elif key == ord(' '):
        current_word += " "
    # Tekan 'BACKSPACE' (atau tombol 'b') untuk menghapus huruf terakhir
    elif key == ord('b') or key == 8:
        current_word = current_word[:-1]

cap.release()
cv2.destroyAllWindows()