import os
import cv2
import mediapipe as mp
import csv
import numpy as np

mp_hands = mp.solutions.hands
DATA_DIR = "./Citra BISINDO"

gagal = []
berhasil = {}

with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,  # Tetap izinkan deteksi hingga 2 tangan
    model_complexity=1,
    min_detection_confidence=0.5
) as hands:

    with open(
        "dataset_koordinat.csv",
        mode="w",
        newline=""
    ) as f:

        writer = csv.writer(f)

        # Header: 1 label + (2 tangan x 21 titik x 2 koordinat) = 85 kolom total
        header = ["label"]
        for hand_idx in range(2):
            for i in range(21):
                header += [f"h{hand_idx}_x{i}", f"h{hand_idx}_y{i}"]
        writer.writerow(header)

        for label in sorted(os.listdir(DATA_DIR)):
            label_path = os.path.join(DATA_DIR, label)

            if not os.path.isdir(label_path):
                continue

            berhasil[label] = 0

            for img_file in sorted(os.listdir(label_path)):
                if not img_file.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue

                img_path = os.path.join(label_path, img_file)
                img = cv2.imread(img_path)

                if img is None:
                    gagal.append((label, img_file, "Gagal membaca gambar"))
                    continue

                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb_img)

                if not results.multi_hand_landmarks:
                    gagal.append((label, img_file, "Tangan tidak terdeteksi"))
                    continue

                row = [label]

                # Proses setiap tangan yang terdeteksi (maksimal 2)
                detected_hands = results.multi_hand_landmarks
                
                for hand_idx in range(2):
                    if hand_idx < len(detected_hands):
                        # Ambil landmark tangan ke-i
                        landmarks = detected_hands[hand_idx].landmark
                        coords = np.array([[lm.x, lm.y] for lm in landmarks])
                        
                        # Normalisasi relatif terhadap pergelangan tangan (landmark 0)
                        wrist = coords[0]
                        coords = coords - wrist
                        
                        max_val = np.max(np.abs(coords))
                        if max_val > 0:
                            coords = coords / max_val
                            
                        row.extend(coords.flatten().tolist())
                    else:
                        # Jika hanya 1 tangan yang terdeteksi, isi slot tangan kedua 
                        # dengan 0.0 (karena sudah dinormalisasi, 0.0 artinya titik pusat / netral)
                        row.extend([0.0] * 42)

                writer.writerow(row)
                berhasil[label] += 1

# Tampilkan ringkasan
print("\n=== HASIL EKSTRAKSI 1 & 2 TANGAN ===")
for label, jumlah in sorted(berhasil.items()):
    print(f"Huruf/Kata {label}: {jumlah} berhasil")

print(f"\nTotal berhasil: {sum(berhasil.values())}")
print(f"Total gagal: {len(gagal)}")

if gagal:
    with open("gambar_gagal.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Huruf", "Nama gambar", "Penyebab"])
        writer.writerows(gagal)
    print("Daftar gambar gagal disimpan ke gambar_gagal.csv")