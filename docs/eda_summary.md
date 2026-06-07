# Ringkasan EDA — GDP Growth Indonesia

## Temuan Utama

### 1. Tren GDP Growth
- Rata-rata historis: **~5.2% per tahun** (1991–2024)
- Nilai minimum: **−13.1%** (1998, Krisis Finansial Asia)
- Nilai maksimum: **~8.2%** (tahun 1995)
- Dua periode negatif: 1998 dan 2020

### 2. Anomali Signifikan
| Tahun | GDP Growth | Peristiwa |
|---|---|---|
| 1998 | −13.1% | Krisis Finansial Asia |
| 2020 | −2.1% | Pandemi COVID-19 |

### 3. Korelasi dengan GDP Growth
*(Diisi setelah menjalankan notebook 02_eda.ipynb)*

### 4. Missing Values
- Beberapa indikator memiliki missing di tahun-tahun awal (1991–1993)
- Ditangani dengan interpolasi linear
- FDI memiliki missing terbanyak (~3 tahun)

### 5. Distribusi
- GDP Growth: distribusi mendekati normal dengan heavy tail kiri (karena 1998)
- Inflation: right-skewed (didominasi nilai rendah, outlier tinggi di 1998)
- Exchange Rate: tren naik linear seiring waktu

## Implikasi untuk Modeling
- Dataset kecil (~34 baris) → gunakan LOOCV bukan simple train-test split
- Outlier 1998 & 2020 dipertahankan karena informatif
- StandardScaler diperlukan karena Exchange Rate memiliki skala sangat berbeda
