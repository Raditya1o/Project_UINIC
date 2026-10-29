import os
import cv2
import mediapipe as mp
import csv

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2)

# Path ke folder dataset gambar kamu
DATA_DIR = './Citra BISINDO'

# Buat file CSV untuk menyimpan data koordinat
with open('dataset_koordinat.csv', mode='w', newline='') as f:
    writer = csv.writer(f)
    
    # Header kolom: label (huruf) + 42 koordinat (x dan y untuk 21 titik)
    header = ['label']
    for hand_idx in range(2):
        for i in range(21):
            header += [f'h{hand_idx}_x{i}', f'h{hand_idx}_y{i}']
    writer.writerow(header)

    # Loop setiap folder huruf (A, B, C, dst)
    for label in os.listdir(DATA_DIR):
        label_path = os.path.join(DATA_DIR, label)
        if not os.path.isdir(label_path):
            continue
            
        for img_file in os.listdir(label_path):
            img_path = os.path.join(label_path, img_file)
            img = cv2.imread(img_path)
            if img is None:
                continue
                
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_img)
            
           # Jika minimal 1 tangan terdeteksi dalam gambar
            if results.multi_hand_landmarks:
                row = [label]
                
                # Masukkan koordinat tangan yang terdeteksi
                for hand_landmarks in results.multi_hand_landmarks:
                    for lm in hand_landmarks.landmark:
                        row.append(lm.x)
                        row.append(lm.y)
                
                # 3. Jika di gambar tersebut HANYA ada 1 tangan, 
                # tambahkan padding angka 0.0 sebanyak 42 kali untuk slot tangan kedua
                if len(results.multi_hand_landmarks) == 1:
                    row.extend([0.0] * 42)
                
                writer.writerow(row)

print("Ekstraksi fitur selesai dan disimpan ke dataset_koordinat.csv!")