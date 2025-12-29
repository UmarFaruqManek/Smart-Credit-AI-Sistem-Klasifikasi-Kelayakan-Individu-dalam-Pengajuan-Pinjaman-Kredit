# Catatan Proses Pemodelan (Modeling)

Dokumen ini merangkum langkah-langkah eksperimen pembuatan model Machine Learning yang dilakukan dalam notebook `model.ipynb` untuk memprediksi kelayakan pinjaman.

## 1. Persiapan Data (Setup)

- **Loading Data**: Menggunakan data hasil preprocessing (`X_preprocessing_ready.csv` dan `y_target.csv`).
- **Encoding Target**:
  - Label target diubah menjadi numerik:
    - `Approved` $\rightarrow$ `0`
    - `Rejected` $\rightarrow$ `1`
- **Splitting Data**:
  - Data dibagi menjadi **80% Training** dan **20% Testing**.
  - Menggunakan parameter `stratify=y` untuk menjaga proporsi kelas target yang seimbang antara train dan test set.

## 2. Eksperimen Model

Tiga algoritma supervised learning diuji untuk menemukan performa terbaik:

### A. Logistic Regression

- Model linear yang sederhana dan _explainable_.
- **Akurasi**: ~92%
- **Performa**: Cukup baik, namun sedikit tertinggal dibandingkan model berbasis ensemble. Nilai precision dan recall seimbang di kedua kelas.

### B. Random Forest Classifier

- Model ensemble berbasis _bagging_ (kumpulan Decision Trees).
- **Akurasi**: ~98% (Tertinggi)
- **Performa**: Sangat baik. Mampu menangkap pola non-linear dengan akurasi sangat tinggi dan minim kesalahan pada kedua kelas.

### C. XGBoost Classifier

- Model ensemble berbasis _boosting_ (Gradient Boosting).
- **Akurasi**: ~98%
- **Performa**: Hampir setara dengan Random Forest, dengan performa yang sangat kompetitif.

## 3. Evaluasi & Perbandingan

| Model                   | Akurasi    | Keterangan                                                                    |
| :---------------------- | :--------- | :---------------------------------------------------------------------------- |
| **Logistic Regression** | 92.27%     | Baseline model yang solid, cocok jika interpretabilitas sangat diutamakan.    |
| **Random Forest**       | **98.36%** | **Performa Terbaik**. Sangat direkomendasikan untuk digunakan dalam produksi. |
| **XGBoost**             | 97.89%     | Alternatif yang sangat kuat, performa hampir identik dengan Random Forest.    |

**Kesimpulan**:
Model **Random Forest** dipilih sebagai kandidat utama karena memberikan akurasi tertinggi pada data pengujian.

## 4. Penyimpanan Model (Artifacts)

Ketiga model telah dilatih dan disimpan menggunakan `joblib` agar dapat digunakan kembali tanpa perlu _training_ ulang:

1.  `logistic_regression_model.pkl`
2.  `random_forest_model.pkl` (Rekomendasi Utama)
3.  `xgboost_model.pkl`

File `.pkl` ini siap diintegrasikan ke dalam API backend untuk melayani prediksi secara _real-time_.
