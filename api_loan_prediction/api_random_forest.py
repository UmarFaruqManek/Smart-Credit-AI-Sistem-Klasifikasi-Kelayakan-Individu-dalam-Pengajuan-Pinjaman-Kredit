from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# =========================================================================
# CONFIG
# =========================================================================
MODEL_FILE = 'random_forest_model.pkl'
PORT = 5002

# =========================================================================
# LOAD ASSETS
# =========================================================================
print(f"Loading {MODEL_FILE} & scaler...")
try:
    scaler = joblib.load('scaler.pkl')
    model = joblib.load(MODEL_FILE)
    print("✅ Model & Scaler berhasil dimuat!")
except Exception as e:
    print(f"❌ Error: {e}")
    scaler = None
    model = None

# =========================================================================
# PREPROCESSING
# =========================================================================
def preprocess_input(input_data):
    if scaler is None: raise ValueError("Scaler belum termuat!")

    df = pd.DataFrame([input_data])
    
    # Encoding
    df['pendidikan_Not Graduate'] = 1 if input_data.get('pendidikan') == 'Not Graduate' else 0
    df['wirausaha_Yes'] = 1 if input_data.get('wirausaha') == 'Yes' else 0
    
    # Scaling
    kolom_numerik = [
        'jumlah_tanggungan', 'pendapatan_tahunan', 'jumlah_pinjaman', 
        'jangka_waktu_pinjaman', 'skor_kredit', 'aset_rumah', 
        'aset_usaha', 'aset_mewah', 'aset_bank'
    ]
    
    for col in kolom_numerik:
        if col not in df.columns: df[col] = 0 
            
    df[kolom_numerik] = scaler.transform(df[kolom_numerik])
    
    return df[kolom_numerik + ['pendidikan_Not Graduate', 'wirausaha_Yes']]

# =========================================================================
# ENDPOINTS
# =========================================================================
@app.route('/')
def home():
    return jsonify({"message": f"Random Forest API Running on Port {PORT}"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        processed_data = preprocess_input(data)
        
        # 1. Prediksi AI (Model)
        prediction = model.predict(processed_data)[0]
        probability = model.predict_proba(processed_data)[0]
        confidence_val = probability[prediction]
        
        # 2. Business Logic (Hybrid Check)
        # Hitung Total Aset & Rasio
        total_aset = (data.get('aset_rumah', 0) + 
                      data.get('aset_usaha', 0) + 
                      data.get('aset_mewah', 0) + 
                      data.get('aset_bank', 0))
        
        pinjaman = data.get('jumlah_pinjaman', 1)  # Hindari bagi nol
        ratio = total_aset / pinjaman
        
        status = "Rejected"
        final_prediction = prediction
        logic_note = "Decision by AI Model"

        if prediction == 0:
            status = "Approved"
        else:
            # Jika REJECTED by Model, Cek Rasio Aset
            # Rule: Jika Aset 5x lipat lebih besar dari pinjaman -> Approve Manual
            if ratio >= 5.0:
                status = "Conditional Approved"
                logic_note = f"Override by Asset Rule (Asset {ratio:.1f}x Loan)"
                final_prediction = 0  # Force Approve (tapi kita kasih label khusus)
            else:
                status = "Rejected"

        return jsonify({
            "model": "Random Forest (Hybrid)",
            "prediction": status,
            "ai_confidence": f"{confidence_val:.2%}",
            "notes": logic_note,
            "asset_to_loan_ratio": f"{ratio:.2f}x"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
