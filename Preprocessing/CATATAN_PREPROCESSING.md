# Catatan Proses Preprocessing

Dokumen ini merangkum langkah-langkah preprocessing yang dilakukan dalam notebook `Preprocessing.ipynb` untuk mempersiapkan data sebelum pemodelan Machine Learning.

## 1. Persiapan & Pembersihan Data

- **Loading Data**: Memuat dataset hasil EDA (`dataset_after_EDA.csv`).
- **Pembersihan Teks**:
  - Membersihkan spasi tersembunyi (whitespace) pada nama kolom.
  - Membersihkan spasi tersembunyi pada isi data kategorikal.
- **Pengubahan Nama Kolom (Translation)**:
  - Mengubah seluruh nama kolom ke dalam Bahasa Indonesia agar lebih mudah dipahami.
  - Contoh: `income_annum` $\rightarrow$ `pendapatan_tahunan`, `loan_amount` $\rightarrow$ `jumlah_pinjaman`, dsb.
- **Penghapusan Fitur**: Menghapus kolom `id_pinjaman` karena hanya berfungsi sebagai identifier unik dan tidak relevan untuk prediksi model.

## 2. Pemisahan Fitur & Target

- **Fitur (X)**: Seluruh kolom kecuali `status_pinjaman`.
- **Target (y)**: Kolom `status_pinjaman` (`Approved` / `Rejected`).

## 3. Feature Engineering & Transformation

- **Identifikasi Tipe Data**:
  - **Kategorikal**: `pendidikan`, `wirausaha`.
  - **Numerik**: `jumlah_tanggungan`, `pendapatan_tahunan`, `jumlah_pinjaman`, `jangka_waktu_pinjaman`, `skor_kredit`, seluruh fitur aset.
- **Encoding (Kategorikal)**:
  - Menggunakan teknik **One-Hot Encoding** (`pd.get_dummies`) dengan parameter `drop_first=True`.
  - Hasilnya: Muncul kolom boolean baru seperti `pendidikan_Not Graduate` dan `wirausaha_Yes`.
- **Scaling (Numerik)**:
  - Menggunakan **StandardScaler** untuk menormalisasi fitur numerik agar memiliki mean=0 dan std=1. Langkah ini penting untuk algoritma yang sensitif terhadap skala data.

## 4. Penyimpanan Hasil (Export)

- **Dataset Siap Model**:
  - Fitur yang sudah diproses disimpan ke `X_preprocessing_ready.csv`.
  - Target disimpan ke `y_target.csv`.
- **Penyimpanan Scaler**:
  - Objek `scaler` disimpan menggunakan **Joblib** menjadi file `scaler.pkl`.
  - **Penting**: File `scaler.pkl` ini Wajib digunakan nanti pada saat deployment/API untuk mentransformasi data input pengguna agar sesuai dengan skala data training.
