# 🚀 Panduan Deploy ke Streamlit Community Cloud

## Persiapan

### 1. Pastikan semua file model sudah ada
Sebelum push ke GitHub, jalankan dulu semua notebook:
```
notebooks/01_data_collection.ipynb
notebooks/02_eda.ipynb
notebooks/03_preprocessing.ipynb
notebooks/04_modeling.ipynb
```

File yang WAJIB ada di repo sebelum deploy:
```
models/best_model.pkl
models/scaler.pkl
models/model_report.json
data/processed/dataset_indonesia.csv
```

### 2. Push ke GitHub
```bash
git init
git add .
git commit -m "feat: initial project setup"
git branch -M main
git remote add origin https://github.com/username/gdp-prediction.git
git push -u origin main
```

---

## Deploy

### 1. Buka Streamlit Community Cloud
Kunjungi: https://share.streamlit.io

### 2. Login dengan GitHub

### 3. Klik "New app"
- **Repository:** pilih `gdp-prediction`
- **Branch:** `main`
- **Main file path:** `app.py`

### 4. Klik "Deploy!"

Tunggu 2–5 menit. Jika ada error, cek log di tab "Logs".

---

## Troubleshooting Umum

| Error | Solusi |
|---|---|
| `ModuleNotFoundError` | Cek `requirements.txt`, pastikan semua library tercantum |
| `FileNotFoundError: best_model.pkl` | Pastikan file model ikut di-push ke GitHub |
| `No module named 'scripts'` | Pastikan folder `scripts/` dan `utils/` ada di root repo |
| Streamlit crash saat prediksi | Cek versi scikit-learn di `requirements.txt` harus sama dengan saat training |

---

## Versi Library Penting

Pastikan versi di `requirements.txt` **sama** dengan yang dipakai saat training model:
```
scikit-learn==1.5.0   # HARUS sama!
joblib==1.4.2         # HARUS sama!
```

Untuk cek versi yang terinstall:
```bash
pip show scikit-learn joblib
```
