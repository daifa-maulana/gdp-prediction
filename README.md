# 📈 Prediksi GDP Growth Indonesia

Proyek Machine Learning untuk memprediksi pertumbuhan ekonomi (GDP Growth) Indonesia menggunakan data historis dari World Bank.

---

## 🗂️ Struktur Proyek

```
gdp-prediction/
├── app.py                        # Entry point Streamlit
├── requirements.txt              # Dependensi library
├── assets/
│   └── style.css                 # Custom styling
├── data/
│   ├── raw/                      # Data mentah per indikator
│   ├── processed/                # Dataset gabungan siap pakai
│   └── eda_outputs/              # Chart hasil EDA
├── models/
│   ├── best_model.pkl            # Model terbaik
│   ├── scaler.pkl                # StandardScaler
│   └── model_report.json         # Laporan evaluasi model
├── notebooks/
│   ├── 01_data_collection.ipynb  # Ambil data dari World Bank
│   ├── 02_eda.ipynb              # Exploratory Data Analysis
│   ├── 03_preprocessing.ipynb   # Preprocessing & scaling
│   └── 04_modeling.ipynb        # Training & evaluasi model
├── pages/
│   ├── 01_Home.py
│   ├── 02_Dataset.py
│   ├── 03_Visualisasi.py
│   ├── 04_Prediksi.py
│   └── 05_Kesimpulan.py
├── scripts/
│   ├── visualization.py          # Fungsi visualisasi Plotly
│   └── preprocessing.py         # Fungsi preprocessing
└── utils/
    └── predictor.py              # Load model & prediksi
```

---

## 🚀 Cara Menjalankan

### 1. Clone & Install
```bash
git clone https://github.com/username/gdp-prediction.git
cd gdp-prediction
pip install -r requirements.txt
```

### 2. Jalankan Notebook Secara Berurutan
```bash
# Di Jupyter Notebook / JupyterLab
1. notebooks/01_data_collection.ipynb   # Ambil data dari World Bank
2. notebooks/02_eda.ipynb              # EDA & visualisasi
3. notebooks/03_preprocessing.ipynb   # Preprocessing & simpan scaler
4. notebooks/04_modeling.ipynb        # Train model & simpan best_model.pkl
```

### 3. Jalankan Streamlit
```bash
streamlit run app.py
```

---

## 🌐 Deploy ke Streamlit Community Cloud

1. Push project ke GitHub (pastikan `requirements.txt` ada)
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Klik **New app** → pilih repo → set `app.py` sebagai main file
4. Klik **Deploy**

> ⚠️ **Penting**: File `models/best_model.pkl`, `models/scaler.pkl`, dan `models/model_report.json` **harus ikut di-push ke GitHub** agar app bisa berjalan di Streamlit Cloud.

---

## 📊 Variabel yang Digunakan

| Variabel | Kode World Bank | Satuan |
|---|---|---|
| GDP_Growth (Target) | NY.GDP.MKTP.KD.ZG | % |
| Inflation | FP.CPI.TOTL.ZG | % |
| Unemployment | SL.UEM.TOTL.ZS | % |
| Population_Growth | SP.POP.GROW | % |
| Exports | NE.EXP.GNFS.ZS | % GDP |
| Imports | NE.IMP.GNFS.ZS | % GDP |
| FDI | BX.KLT.DINV.WD.GD.ZS | % GDP |
| Exchange_Rate | PA.NUS.FCRF | IDR/USD |

---

## 🤖 Model yang Digunakan

- Linear Regression
- Ridge Regression
- Decision Tree Regressor
- Random Forest Regressor

Evaluasi menggunakan **Leave-One-Out Cross Validation (LOOCV)** — lebih andal untuk dataset kecil (~34 baris).

---

## 👥 Tim

| No | Nama | Peran |
|---|---|---|
| 1 | Daifa Maulana | Project Manager |
| 2 | Mochamad Firmansyah | Data Analyst & ML |
| 3 | Fauzi Rizky Maulana | Data Analyst & ML |
| 4 | Dini Sriastuti | Data Analyst & ML |
| 5 | Nazwa Nur Hapidah | UI/UX Designer |
| 6 | Muhammad Raufan Umarulloh | Frontend Developer |
| 7 | Fajar Muhammad Ramdhani | Backend Developer |
