import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# 1. Load dataset koordinat
df = pd.read_csv('dataset_koordinat.csv')

# Pisahkan fitur (X) dan label/target (y)
X = df.iloc[:, 1:].values  # Kolom koordinat
y = df.iloc[:, 0].values   # Kolom huruf (label)

# 2. Bagi data untuk training (80%) dan testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Latih model Random Forest
print("Sedang melatih model AI...")
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 4. Evaluasi akurasi
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Akurasi Model: {acc * 100:.2f}%")

# 5. Simpan model yang sudah dilatih ke file
with open('model_bisindo.p', 'wb') as f:
    pickle.dump(model, f)
print("Model berhasil disimpan sebagai 'model_bisindo.p'!")