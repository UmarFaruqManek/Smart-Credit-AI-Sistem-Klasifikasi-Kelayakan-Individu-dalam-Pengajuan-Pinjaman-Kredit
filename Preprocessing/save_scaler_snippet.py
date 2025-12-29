# Tambahkan cell ini di bagian paling bawah notebook Preprocessing.ipynb
import joblib

# Simpan scaler yang sudah di-fit sebelumnya
# Pastikan variabel 'scaler' masih ada di memori (sudah di-run di cell sebelumnya)
joblib.dump(scaler, 'scaler.pkl')

print("✅ Scaler berhasil disimpan sebagai 'scaler.pkl'")
print("Sekarang file ini bisa digunakan untuk preprocessing data input baru di API.")
