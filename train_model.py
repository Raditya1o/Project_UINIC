import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

# 1. Load dataset koordinat
df = pd.read_csv('dataset_koordinat.csv')

print("Total baris:", len(df))
print("Total kolom:", len(df))

print("\nJumlah data per huruf:")
print(df["label"].value_counts().sort_index())

print("\nJumlah gambar yang berhasil diekstrak:")
print(df["label"].value_counts().sum())

# Pisahkan fitur (X) dan label/target (y)
X = df.iloc[:, 1:].values  # Kolom koordinat
y = df.iloc[:, 0].values   # Kolom huruf (label)

# 2. Bagi data untuk training (80%) dan testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 3. Augmentasi koordinat training saja
rng = np.random.default_rng(42)

noise = rng.normal(
    loc=0,
    scale=0.003,
    size=X_train.shape
)

X_augmented = X_train + noise

# Gabungkan data asli dan data variasi
X_train_baru = np.concatenate(
    [X_train, X_augmented],
    axis=0
)

y_train_baru = np.concatenate(
    [y_train, y_train],
    axis=0
)

# 4. Latih model Random Forest
print("Sedang melatih model AI...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_baru, y_train_baru)

# 5. Evaluasi akurasi
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Akurasi Model: {acc * 100:.2f}%")

print("\nLaporan per kelas:")
print(classification_report(y_test, y_pred, zero_division=0))

# 6. Simpan model yang sudah dilatih ke file
with open('model_bisindo.p', 'wb') as f:
    pickle.dump(model, f)
print("Model berhasil disimpan sebagai 'model_bisindo.p'!")