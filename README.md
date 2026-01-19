# 🏦 Smart Credit AI: Sistem Klasifikasi Kelayakan Kredit

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)

> **Proyek Capstone** untuk syarat kelulusan program **Dicoding Data Science**. Membangun sistem cerdas yang dapat memprediksi kelayakan pengajuan pinjaman kredit nasabah berdasarkan data profil finansial mereka.

---

## 📋 Daftar Isi

1. [Tentang Proyek](#-tentang-proyek)
2. [Alur Kerja (Pipeline)](#-alur-kerja)
3. [Dataset & Struktur Folder](#-dataset--struktur-folder)
4. [Tim Pengembang](#-tim-pengembang)
5. [Exploratory Data Analysis (EDA)](#-1-exploratory-data-analysis-eda)
6. [Data Preprocessing](#-2-data-preprocessing)
7. [Pengembangan Model](#-3-pengembangan-model)
8. [Deployment & Cloud](#-4-deployment--cloud)
9. [Dokumentasi API](#-5-dokumentasi-api)
10. [Cara Menjalankan Lokal](#-6-cara-menjalankan-lokal)

---

## 📖 Tentang Proyek

Lembaga keuangan sering menghadapi tantangan dalam menentukan apakah seorang pemohon pinjaman layak diberikan kredit atau tidak. Keputusan yang salah dapat berakibat pada kredit macet (NPL) atau hilangnya potensi nasabah baik.

**Smart Credit AI** hadir sebagai solusi berbasis Machine Learning untuk mengotomatisasi proses persetujuan pinjaman dengan menganalisis berbagai faktor seperti:

- Skor Kredit (CIBIL Score)
- Pendapatan & Aset
- Jumlah & Jangka Waktu Pinjaman
- Status Pendidikan & Pekerjaan

---

## 🔄 Alur Kerja

Proyek ini mengikuti siklus _end-to-end Machine Learning_:

```mermaid
graph LR
    A[Dataset] --> B(EDA & Cleaning)
    B --> C(Preprocessing)
    C --> D{Model Training}
    D --> E[Evaluasi Model]
    E --> F[API Backend]
    F --> G[Cloud Deployment]
```

1.  **Data Collection**: Mengumpulkan data historis pinjaman.
2.  **EDA**: Menganalisis pola dan korelasi data.
3.  **Preprocessing**: Membersihkan dan transformasi data agar siap untuk mesin.
4.  **Modeling**: Melatih algoritma Logistic Regression, Random Forest, dan XGBoost.
5.  **Deployment**: Mengemas model menjadi API menggunakan Flask dan deploy ke Google Cloud Run.

---

## 📂 Dataset & Struktur Folder

### Sumber Data

Dataset yang digunakan dalam proyek ini bersumber dari Kaggle:
🔗 [Loan Approval Prediction Dataset](https://www.kaggle.com/datasets/architsharma01/loan-approval-prediction-dataset/data)

### Struktur Direktori

Berikut adalah susunan folder proyek ini beserta penjelasannya:

```text
├── cloud_api/               # Source code utama API (Flask) untuk deployment
│   ├── main.py              # File utama aplikasi Flask
│   ├── Dockerfile           # Konfigurasi container Docker
│   └── requirements.txt     # Daftar library python yang dibutuhkan
├── EDA/                     # Notebook Exploratory Data Analysis
│   └── EDA Procces.ipynb    # Proses analisis awal data
├── Preprocessing/           # Tahapan pembersihan data
│   ├── Preprocessing.ipynb  # Notebook cleaning, encoding, scaling
│   └── scaler.pkl           # File scaler tersimpan (Joblib)
├── model/                   # Eksperimen pelatihan model (Jupyter Notebooks)
│   └── model.ipynb          # Training Logistic Reg, RF, XGBoost
├── model_jadi/              # File binary model yang sudah dilatih (.pkl)
│   ├── logistic_regression_model.pkl
│   ├── random_forest_model.pkl
│   └── xgboost_model.pkl
└── README.md                # Dokumentasi proyek ini
```

---

## 👥 Tim Pengembang

Proyek ini dikerjakan oleh **Team ID: C24-G002** (Smart Credit AI) dari program Dicoding Data Science:

| ID            | Nama Anggota               | Role         |
| :------------ | :------------------------- | :----------- |
| **B25B9D009** | Handika                    | Data Science |
| **B25B9D008** | Reza Gunawan Ridlo Setiadi | Data Science |
| **B25B9D007** | Abdillah Husein Sanjani    | Data Science |
| **B25B9D003** | Umar Faruq Manek           | Data Science |

---

## 🔍 1. Exploratory Data Analysis (EDA)

Kami melakukan analisis mendalam untuk memahami karakteristik data.

**Temuan Utama:**

- **Keseimbangan Data**: Dataset cukup seimbang dengan proporsi **62% Disetujui** dan **38% Ditolak**.
- **Faktor Penentu Utama**: `cibil_score` (Skor Kredit) memiliki korelasi terkuat dengan status persetujuan. Skor yang rendah hampir pasti ditolak.
- **Hubungan Pendapatan & Aset**: Terdapat korelasi linear yang sangat kuat antara pendapatan tahunan dengan nilai aset (rumah, komersial, mewah, bank). Semakin tinggi pendapatan, semakin banyak aset yang dimiliki.

---

## ⚙️ 2. Data Preprocessing

Sebelum masuk ke tahap modeling, data mentah diproses terlebih dahulu:

1.  **Pembersihan Data**: Menghapus spasi berlebih pada kolom dan nilai kategorikal.
2.  **Feature Selection**: Membuang kolom `loan_id` karena tidak relevan untuk prediksi.
3.  **Encoding**: Mengubah data teks menjadi angka.
    - `education` (Graduate/Not Graduate) $\rightarrow$ 0/1
    - `self_employed` (Yes/No) $\rightarrow$ 0/1
4.  **Scaling**: Menggunakan **StandardScaler** untuk menyetarakan rentang nilai pada fitur numerik (seperti pendapatan dan jumlah pinjaman) agar model lebih optimal.

---

## 🧠 3. Pengembangan Model

Kami bereksperimen dengan tiga algoritma berbeda untuk mencari performa terbaik:

| Model                   | Akurasi     | Keterangan                                                                     |
| :---------------------- | :---------- | :----------------------------------------------------------------------------- |
| **Logistic Regression** | ~92.27%     | Baseline model, baik namun kurang menangkap pola kompleks.                     |
| **XGBoost Classifier**  | ~97.89%     | Performa sangat tinggi dengan boosting.                                        |
| **Random Forest**       | **~98.36%** | **Model Terbaik (Champion)**. Dipilih karena akurasi dan stabilitas tertinggi. |

Model **Random Forest** akhirnya dipilih dan disimpan (`random_forest_model.pkl`) untuk digunakan di sistem produksi.

---

## ☁️ 4. Deployment & Cloud

Sistem ini dideploy menggunakan arsitektur **Serverless** modern untuk skalabilitas dan kemudahan maintenance.

- **Platform**: [Google Cloud Run](https://cloud.google.com/run)
- **Container**: Docker
- **CI/CD**: GitHub Actions

**Otomatisasi**:
Setiap kali ada perubahan kode (push) ke branch `main`, GitHub Actions akan otomatis:

1.  Membangun (Build) Docker Image baru.
2.  Mengirim (Push) image ke Google Artifact Registry.
3.  Mendeploy revisi terbaru ke Cloud Run secara live.

---

## 🔌 5. Dokumentasi API

Anda dapat mengakses layanan prediksi melalui REST API berikut:

### Endpoint Prediksi

- **URL**: `[URL_CLOUD_RUN_ANDA]/predict/random-forest`
- **Method**: `POST`
- **Content-Type**: `application/json`

### Contoh Request Body

Kirim data parameter pemohon dalam format JSON:

```json
{
  "jumlah_tanggungan": 2,
  "pendidikan": "Graduate",
  "wirausaha": "No",
  "pendapatan_tahunan": 9600000,
  "jumlah_pinjaman": 29900000,
  "jangka_waktu_pinjaman": 12,
  "skor_kredit": 778,
  "aset_rumah": 2400000,
  "aset_komersial": 17600000,
  "aset_mewah": 22700000,
  "aset_bank": 8000000
}
```

### Contoh Response

API akan mengembalikan keputusan apakah pinjaman disetujui atau ditolak, beserta tingkat keyakinannya.

```json
{
  "model": "random-forest",
  "status": "Disetujui",
  "prediction_label": 0,
  "confidence": "98.50%",
  "ratio_aset_pinjaman": "1.69x"
}
```

> **Catatan**: Jika status ditolak namun rasio aset terhadap pinjaman sangat besar (>5x), sistem memiliki aturan hibrida untuk memberikan status "Disetujui Bersyarat".

---

## 💻 6. Cara Menjalankan Lokal

Jika Anda ingin menjalankan proyek ini di komputer Anda sendiri secara lokal (Localhost):

1.  **Clone Repository**

    ```bash
    git clone https://github.com/username/project-repo.git
    cd project-repo
    ```

2.  **Install Dependencies**
    Pastikan Python sudah terinstall, lalu jalankan instalasi library dari folder `api_loan_prediction`:

    ```bash
    pip install -r api_loan_prediction/requirements.txt
    ```

3.  **Jalankan Aplikasi API**
    Kita akan menjalankan model terbaik (**Random Forest**) sebagai server lokal:

    ```bash
    python api_loan_prediction/api_random_forest.py
    ```

    _Server akan berjalan di `http://localhost:5000` (atau port yang tertera di terminal)._

4.  **Testing dengan Postman**
    Karena ini adalah layanan API (Backend), kita memerlukan tools seperti **Postman** untuk melakukan pengujian request.

    - Buka Postman.
    - Buat Request baru dengan method **POST**.
    - Masukkan URL: `http://localhost:5000/predict` (sesuaikan port jika berbeda).
    - Pilih tab **Body** -> **raw** -> **JSON**.
    - Masukkan contoh JSON data nasabah (seperti di bagian Dokumentasi API di atas).
    - Klik **Send** dan lihat hasil prediksinya!

---

_Dibuat dengan ❤️ oleh Tim Capstone Smart Credit AI_
