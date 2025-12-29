import joblib
import pandas as pd
import numpy as np
import os

# =========================================================================
# FUNGSI PREPROCESSING
# =========================================================================
def preprocess_input(input_data, scaler_path='scaler.pkl'):
    if not os.path.exists(scaler_path): return None
    scaler = joblib.load(scaler_path)
    df = pd.DataFrame([input_data])
    df['pendidikan_Not Graduate'] = 1 if input_data['pendidikan'] == 'Not Graduate' else 0
    df['wirausaha_Yes'] = 1 if input_data['wirausaha'] == 'Yes' else 0
    kolom_numerik = ['jumlah_tanggungan', 'pendapatan_tahunan', 'jumlah_pinjaman', 'jangka_waktu_pinjaman', 'skor_kredit', 'aset_rumah', 'aset_usaha', 'aset_mewah', 'aset_bank']
    df[kolom_numerik] = scaler.transform(df[kolom_numerik])
    final_features = kolom_numerik + ['pendidikan_Not Graduate', 'wirausaha_Yes']
    return df[final_features]

# =========================================================================
# INPUT DATA
# =========================================================================
new_data_1 = {'jumlah_tanggungan': 2, 'pendidikan': 'Graduate', 'wirausaha': 'No', 'pendapatan_tahunan': 15000000, 'jumlah_pinjaman': 30000000, 'jangka_waktu_pinjaman': 24, 'skor_kredit': 850, 'aset_rumah': 50000000, 'aset_usaha': 20000000, 'aset_mewah': 10000000, 'aset_bank': 30000000}
new_data_2 = {'jumlah_tanggungan': 4, 'pendidikan': 'Not Graduate', 'wirausaha': 'Yes', 'pendapatan_tahunan': 3000000, 'jumlah_pinjaman': 50000000, 'jangka_waktu_pinjaman': 12, 'skor_kredit': 350, 'aset_rumah': 0, 'aset_usaha': 0, 'aset_mewah': 0, 'aset_bank': 1000000}

# =========================================================================
# EKSEKUSI (LOGISTIC REGRESSION)
# =========================================================================
print("LOGISTIC REGRESSION TEST")
print("-" * 30)

model = joblib.load('logistic_regression_model.pkl')

# Tes 1
input_1 = preprocess_input(new_data_1)
pred_1 = model.predict(input_1)[0]
prob_1 = model.predict_proba(input_1)[0][pred_1] # Ambil probabilitas kelas yang diprediksi
hasil_1 = "Approved" if pred_1 == 0 else "Rejected"

print("[Data 1]")
print(f"Hasil   : {hasil_1}")
print(f"Akurasi : {prob_1:.1%}")

print("-" * 30)

# Tes 2
input_2 = preprocess_input(new_data_2)
pred_2 = model.predict(input_2)[0]
prob_2 = model.predict_proba(input_2)[0][pred_2]
hasil_2 = "Approved" if pred_2 == 0 else "Rejected"

print("[Data 2]")
print(f"Hasil   : {hasil_2}")
print(f"Akurasi : {prob_2:.1%}")
