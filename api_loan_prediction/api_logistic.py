from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# =========================================================================
# CONFIG
# =========================================================================
MODEL_FILE = 'logistic_regression_model.pkl'
PORT = 5001

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
    return jsonify({"message": f"Logistic Regression API Running on Port {PORT}"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        processed_data = preprocess_input(data)
        
        prediction = model.predict(processed_data)[0]
        probability = model.predict_proba(processed_data)[0]
        
        return jsonify({
            "model": "Logistic Regression",
            "prediction": "Approved" if prediction == 0 else "Rejected",
            "confidence": f"{probability[prediction]:.2%}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=PORT)
