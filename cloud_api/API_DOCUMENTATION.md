# Dokumentasi API Prediksi Kelayakan Pinjaman (Smart Credit AI)

Dokumentasi ini menjelaskan cara menggunakan layanan API Smart Credit AI untuk memprediksi kelayakan pinjaman nasabah secara otomatis menggunakan Machine Learning.

---

## 🚀 Daftar Endpoint

Terdapat 3 model AI yang tersedia. Anda dapat memilih salah satu sesuai kebutuhan (Rekomendasi: **XGBoost**).

| Method | URL Endpoint             | Deskripsi                                                                  |
| :----- | :----------------------- | :------------------------------------------------------------------------- |
| `POST` | `/predict/xgboost`       | **(Rekomendasi)** Menggunakan model XGBoost. Akurasi tinggi & konservatif. |
| `POST` | `/predict/random-forest` | Menggunakan model Random Forest. Cenderung lebih fleksibel.                |
| `POST` | `/predict/logistic`      | Menggunakan model Logistic Regression. Cocok untuk baseline sederhana.     |

**Base URL Cloud Run:**

```
https://loan-prediction-api-1015488191395.asia-southeast2.run.app
```

_(Gunakan URL di atas sebagai awalan untuk setiap endpoint)_

---

## 📝 Format Request (Permintaan)

- **Content-Type**: `application/json`
- **Method**: `POST`

### Kamus Data Input (Input Dictionary)

Pastikan data yang dikirim sesuai dengan spesifikasi berikut agar API berjalan lancar.

| Nama Field (Key)            | Tipe Data | Wajib? | Keterangan & Aturan Isi                                                                                                                             |
| :-------------------------- | :-------- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`pendidikan`**            | `String`  | Ya     | Status pendidikan terakhir pemohon.<br>⛔ **Hanya menerima:**<br>• `"Graduate"` (Lulusan Sarjana/Diploma)<br>• `"Not Graduate"` (Belum/Tidak Lulus) |
| **`wirausaha`**             | `String`  | Ya     | Apakah pemohon bekerja sendiri?<br>⛔ **Hanya menerima:**<br>• `"Yes"` (Wirausaha)<br>• `"No"` (Karyawan/Lainnya)                                   |
| **`jumlah_tanggungan`**     | `Integer` | Ya     | Jumlah orang yang ditanggung (anak/istri).<br>Contoh: `0`, `1`, `2`, dst.                                                                           |
| **`pendapatan_tahunan`**    | `Integer` | Ya     | Total pendapatan per tahun (dalam Rupiah).<br>Contoh: `120000000` (untuk 120 Juta).                                                                 |
| **`jumlah_pinjaman`**       | `Integer` | Ya     | Besar pinjaman yang diajukan (dalam Rupiah).<br>Contoh: `300000000` (untuk 300 Juta).                                                               |
| **`jangka_waktu_pinjaman`** | `Integer` | Ya     | Lama pinjaman dalam satuan **TAHUN**.<br>Contoh: `5` (untuk 5 tahun), `15` (untuk 15 tahun).<br>⚠️ _Range training data: 2 s.d 20 tahun._           |
| **`skor_kredit`**           | `Integer` | Ya     | Skor kredit pemohon (CIBIL Score).<br>Range: `300` (Terburuk) s.d `900` (Sempurna).                                                                 |
| **`aset_rumah`**            | `Integer` | Ya     | Nilai taksiran aset rumah (Residential Assets).<br>Isi `0` jika tidak punya.                                                                        |
| **`aset_usaha`**            | `Integer` | Ya     | Nilai aset komersial/toko (Commercial Assets).<br>Isi `0` jika tidak punya.                                                                         |
| **`aset_mewah`**            | `Integer` | Ya     | Nilai aset barang mewah (Luxury Assets).<br>Isi `0` jika tidak punya.                                                                               |
| **`aset_bank`**             | `Integer` | Ya     | Nilai tabungan/deposito di bank (Bank Assets).<br>Isi `0` jika tidak punya.                                                                         |

---

## 💡 Contoh Input JSON

Berikut adalah contoh payload JSON lengkap yang bisa Anda copy-paste ke Postman:

```json
{
  "pendidikan": "Graduate",
  "wirausaha": "No",
  "jumlah_tanggungan": 2,
  "pendapatan_tahunan": 120000000,
  "jumlah_pinjaman": 300000000,
  "jangka_waktu_pinjaman": 15,
  "skor_kredit": 650,
  "aset_rumah": 500000000,
  "aset_usaha": 0,
  "aset_mewah": 50000000,
  "aset_bank": 100000000
}
```

---

## 📤 Penjelasan Output (Response)

API akan mengembalikan JSON dengan format berikut:

```json
{
  "model": "xgboost",
  "status": "Disetujui",
  "prediction_label": 0,
  "confidence": "78.50%",
  "ratio_aset_pinjaman": "2.17x"
}
```

### Arti Field Output:

1.  **`status`**: Keputusan akhir sistem.
    - `"Disetujui"`: Aman untuk diberikan pinjaman.
    - `"Ditolak"`: Berisiko tinggi.
    - `"Disetujui Bersyarat"`: Ditolak oleh AI, tapi disetujui karena jaminan aset nasabah sangat besar (>5x pinjaman).
2.  **`prediction_label`**: Hasil murni dari otak AI.
    - `0`: AI bilang Approve.
    - `1`: AI bilang Reject.
3.  **`confidence`**: Tingkat keyakinan AI terhadap prediksinya (0% - 100%).
4.  **`ratio_aset_pinjaman`**: Perbandingan total kekayaan nasabah dibanding utangnya. Semakin besar semakin aman.
