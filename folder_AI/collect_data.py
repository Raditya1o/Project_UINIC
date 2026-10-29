import os
import cv2

# Tentukan direktori penyimpanan dataset
DATA_DIR = "./Citra BISINDO"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Masukkan huruf yang ingin kamu ambil datanya (misal: 'N', 'C', dll.)
label_name = input("Masukkan huruf/label yang ingin direkam: ").strip().upper()

label_path = os.path.join(DATA_DIR, label_name)
if not os.path.exists(label_path):
    os.makedirs(label_path)

# Buka webcam
cap = cv2.VideoCapture(0)
print(f"\n[INFO] Bersiap merekam untuk huruf '{label_name}'")
print("[INFO] Tekan spasi (' ') untuk mengambil gambar.")
print("[INFO] Tekan 'q' untuk keluar / ganti huruf.\n")

counter = len(os.listdir(label_path)) # Melanjutkan hitungan jika sudah ada foto sebelumnya

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal membuka kamera!")
        break

    # Tampilkan teks panduan di layar webcam
    display_frame = frame.copy()
    cv2.putText(display_frame, f"Huruf: {label_name} | Total: {counter}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(display_frame, "Tekan 'SPACE' untuk foto, 'Q' untuk keluar", (30, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow("Perekam Dataset BISINDO", display_frame)

    key = cv2.waitKey(1) & 0xFF

    # Jika tombol 'q' ditekan, keluar dari program
    if key == ord('q'):
        break
    
    # Jika tombol 'Spasi' ditekan, simpan gambar
    elif key == ord(' '):
        counter += 1
        img_name = os.path.join(label_path, f"{label_name}_{counter}.jpg")
        cv2.imwrite(img_name, frame)
        print(f"Berhasil menyimpan: {img_name}")

cap.release()
cv2.destroyAllWindows()
print(f"Selesai! Total gambar untuk huruf {label_name} sekarang: {counter}")