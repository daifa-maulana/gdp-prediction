# Data Dictionary

## Dataset: `dataset_indonesia.csv`

Sumber: [World Bank Open Data](https://data.worldbank.org/)  
Negara: Indonesia (IDN)  
Periode: 1991 – 2024  
Jumlah baris: ±34  

---

| Variabel | Deskripsi | Satuan | Kode World Bank | Rentang Wajar | Missing (est.) |
|---|---|---|---|---|---|
| **Year** | Tahun observasi | Tahun | — | 1991–2024 | 0 |
| **GDP_Growth** | Pertumbuhan GDP riil tahunan (Target) | % | NY.GDP.MKTP.KD.ZG | −15 s/d 10 | ~0 |
| **Inflation** | Inflasi berdasarkan CPI | % | FP.CPI.TOTL.ZG | 2 s/d 80 | ~1 |
| **Unemployment** | Pengangguran terhadap angkatan kerja | % | SL.UEM.TOTL.ZS | 3 s/d 12 | ~2 |
| **Population_Growth** | Pertumbuhan populasi tahunan | % | SP.POP.GROW | 0.5 s/d 2.5 | ~0 |
| **Exports** | Ekspor barang & jasa sebagai % GDP | % GDP | NE.EXP.GNFS.ZS | 15 s/d 45 | ~1 |
| **Imports** | Impor barang & jasa sebagai % GDP | % GDP | NE.IMP.GNFS.ZS | 15 s/d 40 | ~1 |
| **FDI** | Investasi asing langsung bersih | % GDP | BX.KLT.DINV.WD.GD.ZS | −2 s/d 5 | ~3 |
| **Exchange_Rate** | Nilai tukar resmi IDR terhadap USD | IDR/USD | PA.NUS.FCRF | 2000 s/d 16000 | ~0 |

---

## Catatan Penting

- **Outlier yang Dipertahankan:**
  - 1998: GDP Growth −13.1% (Krisis Finansial Asia)
  - 2020: GDP Growth −2.1% (Pandemi COVID-19)
  - Kedua nilai ini merupakan kejadian nyata dan dipertahankan dalam dataset

- **Penanganan Missing Values:** Interpolasi linear pada sumbu waktu

- **Normalisasi:** StandardScaler (fit hanya pada training data)
