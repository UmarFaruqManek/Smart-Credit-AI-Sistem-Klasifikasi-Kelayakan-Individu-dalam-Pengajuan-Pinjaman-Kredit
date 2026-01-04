import os
import joblib
import pandas as pd
import flask
from flask import Flask, request, jsonify
import xgboost as xgb

app = Flask(__name__)

# =========================================================================
# CONFIG & LOAD MODELS
# =========================================================================
# Load Scaler
try:
    scaler = joblib.load('scaler.pkl')
    print("✅ Scaler loaded.")
except Exception as e:
    print(f"❌ Error loading scaler: {e}")
    scaler = None

# Load Models
models = {}
model_files = {
    'logistic': 'logistic_regression_model.pkl',
    'random-forest': 'random_forest_model.pkl',
    'xgboost': 'xgboost_model.pkl'
}

for name, filename in model_files.items():
    try:
        # Khusus XGBoost, kadang perlu cara load berbeda jika versi beda, 
        # tapi joblib biasanya aman jika versi sama.
        # Untuk safety, kita coba joblib dulu.
        if name == 'xgboost':
            try:
                models[name] = joblib.load(filename)
            except:
                # Fallback jika joblib gagal untuk xgb
                bst = xgb.XGBClassifier()
                bst.load_model(filename)
                models[name] = bst
        else:
            models[name] = joblib.load(filename)
            
        print(f"✅ Model {name} loaded.")
    except Exception as e:
        print(f"❌ Error loading {name}: {e}")
        models[name] = None

# =========================================================================
# PREPROCESSING FUNCTION
# =========================================================================
def preprocess_input(input_data):
    if scaler is None:
        raise ValueError("Scaler is not loaded.")

    # Konversi Jangka Waktu: Tidak Diperlukan (Model dilatih dalam Tahun)
    # User input "20" artinya 20 Tahun -> Sesuai Training Data (Range 2-20 Tahun)
    pass

    df = pd.DataFrame([input_data])
    
    # 1. Encoding (Manual sesuai logic sebelumnya)
    # Pastikan key 'pendidikan' dan 'wirausaha' ada, default jika tidak
    pendidikan_val = input_data.get('pendidikan', 'Graduate') 
    wirausaha_val = input_data.get('wirausaha', 'No')

    df['pendidikan_Not Graduate'] = 1 if pendidikan_val == 'Not Graduate' else 0
    df['wirausaha_Yes'] = 1 if wirausaha_val == 'Yes' else 0
    
    # 2. Scaling
    kolom_numerik = [
        'jumlah_tanggungan', 'pendapatan_tahunan', 'jumlah_pinjaman', 
        'jangka_waktu_pinjaman', 'skor_kredit', 'aset_rumah', 
        'aset_usaha', 'aset_mewah', 'aset_bank'
    ]
    
    # Fill 0 jika kolom tidak ada di input
    for col in kolom_numerik:
        if col not in df.columns:
            df[col] = 0 
            
    df[kolom_numerik] = scaler.transform(df[kolom_numerik])
    
    # Fitur final urutannya harus sama dengan saat training!
    # Cek urutan fitur scaler atau training jika memungkinkan. 
    # Di sini kita asumsi urutan standar: Numeric + Encoded
    feature_order = kolom_numerik + ['pendidikan_Not Graduate', 'wirausaha_Yes']
    
    return df[feature_order]

# =========================================================================
# HELPER: PREDICT LOGIC
# =========================================================================
def make_prediction(model_name, data):
    model = models.get(model_name)
    if not model:
        return {"error": f"Model {model_name} not available"}, 503

    try:
        processed_data = preprocess_input(data)
        
        # Prediksi
        prediction = model.predict(processed_data)[0]
        # Probabilitas (jika support predict_proba)
        try:
            proba = model.predict_proba(processed_data)[0]
            confidence = float(proba[prediction])
        except:
            confidence = 0.0

        # Business Logic (Sama untuk semua model)
        total_aset = (data.get('aset_rumah', 0) + 
                      data.get('aset_usaha', 0) + 
                      data.get('aset_mewah', 0) + 
                      data.get('aset_bank', 0))
        
        pinjaman = data.get('jumlah_pinjaman', 1) 
        if pinjaman == 0: pinjaman = 1
        ratio = total_aset / pinjaman
        
        # Update Logic Sesuai CATATAN_MODEL.md: 0 = Approved, 1 = Rejected
        status = "Ditolak" 
        
        if prediction == 0:
            status = "Disetujui"
        else:
            status = "Ditolak"
            # Hybrid Rule: Jika Rejected (1) tapi Aset Besar -> Approve
            if ratio >= 5.0:
                status = "Disetujui Bersyarat"
                
        return {
            "model": model_name,
            "status": status,
            "prediction_label": int(prediction),
            "confidence": f"{confidence:.2%}",
            "ratio_aset_pinjaman": f"{ratio:.2f}x"
        }, 200

    except Exception as e:
        return {"error": str(e)}, 400

# =========================================================================
# ENDPOINTS
# =========================================================================
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "active",
        "models_loaded": list(models.keys())
    })

@app.route('/predict/logistic', methods=['POST'])
def predict_logistic():
    return jsonify(*make_prediction('logistic', request.get_json()))

@app.route('/predict/random-forest', methods=['POST'])
def predict_rf():
    return jsonify(*make_prediction('random-forest', request.get_json()))

@app.route('/predict/xgboost', methods=['POST'])
def predict_xgb():
    return jsonify(*make_prediction('xgboost', request.get_json()))

if __name__ == '__main__':
    # Local dev run
    app.run(debug=True, port=8080)
