# Catatan Proses Exploratory Data Analysis (EDA)

Dokumen ini merangkum proses dan temuan utama dari analisis data yang dilakukan dalam notebook `EDA Procces.ipynb`.

## 1. Persiapan Data (Data Preparation)

- **Loading Data**: Dataset dimuat dari file `dataset_capstone.csv`.
- **Pembersihan Kolom**: Nama kolom dibersihkan dari spasi berlebih (whitespace) untuk memudahkan pemrosesan.
- **Pemeriksaan Awal**:
  - **Ukuran Data**: Dataset terdiri dari **4.269 baris** dan **13 kolom**.
  - **Tipe Data**: Sebagian besar fitur bernilai numerik (`int64`), dengan beberapa fitur kategorikal (`education`, `self_employed`, `loan_status`).
  - **Duplikasi**: Tidak ditemukan data duplikat (`0 duplicates`).
  - **Missing Values**: Tidak ditemukan nilai yang hilang (`0 null values`) pada seluruh kolom.

## 2. Analisis Statistik Deskriptif

- Dilakukan pengecekan statistik dasar (mean, std, min, max, kuartil) untuk fitur numerik.
- **Target Variable (`loan_status`)**:
  - `Approved`: 2.656 data (~62%)
  - `Rejected`: 1.613 data (~38%)
  - Proporsi kelas target cukup seimbang, tidak terjadi _extreme imbalance_.

## 3. Analisis Univariat (Distribusi Fitur)

- **CIBIL Score**: Rentang nilai antara 300 hingga 900. Distribusi menunjukkan pola yang merata namun ada kecenderungan pengelompokan tertentu.
- **Loan Term**: Jangka waktu pinjaman bervariasi dari 2 hingga 20 tahun.
- **Income & Assets**: Distribusi pendapatan dan nilai aset cenderung _right-skewed_ (miring ke kanan), wajar untuk data keuangan di mana sebagian kecil populasi memiliki kekayaan sangat tinggi.

## 4. Analisis Bivariat & Multivariat (Hubungan Antar Fitur)

- **Korelasi Fitur (Heatmap)**:
  - Terdapat korelasi positif yang **sangat kuat** antara `income_annum` (pendapatan tahunan) dengan:
    - `loan_amount` (Jumlah pinjaman)
    - `residential_assets_value`
    - `commercial_assets_value`
    - `luxury_assets_value`
    - `bank_asset_value`
  - Hal ini mengindikasikan bahwa pemohon dengan pendapatan tinggi cenderung memiliki aset lebih banyak dan mengajukan pinjaman lebih besar.
- **Hubungan dengan `loan_status`**:
  - `cibil_score` terlihat menjadi faktor pembeda yang paling signifikan antara status `Approved` dan `Rejected`. Skor CIBIL yang lebih tinggi berkorelasi kuat dengan persetujuan pinjaman.

## 5. Temuan Utama (Key Insights)

1.  **Kualitas Data Baik**: Dataset bersih dari missing values dan duplikat, sehingga siap untuk pemodelan tanpa _imputation_ yang berat.
2.  **Multikolinieritas**: Karena korelasi yang sangat tinggi antara Income dan berbagai jenis Asset, model linier (seperti Logistic Regression) mungkin memerlukan _feature selection_ atau regularisasi untuk menghindari multikolinieritas. Model berbasis _tree_ (Random Forest, XGBoost) mungkin lebih tahan terhadap hal ini.
3.  **Faktor Penentu**: `cibil_score` diprediksi akan menjadi fitur terpenting (most important feature) dalam model klasifikasi nanti.

## 6. Rekomendasi Selanjutnya

- Lakukan _encoding_ untuk fitur kategorikal (`education`, `self_employed`, `loan_status`).
- Pertimbangkan untuk membuang atau menggabungkan fitur aset yang sangat berkorelasi jika menggunakan model linier, atau gunakan teknik _dimensionality reduction_ jika diperlukan.
- Lakukan _scaling_ data (Normalization/Standardization) sebelum masuk ke algoritma pemodelan yang sensitif terhadap skala (seperti KNN atau SVM).
