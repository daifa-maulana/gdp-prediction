import streamlit as st
st.set_page_config(page_title="Dataset", page_icon="📁", layout="wide", initial_sidebar_state="collapsed")
from utils.navigation import show_navbar
show_navbar()
import pandas as pd
import os

st.set_page_config(page_title="Dataset", page_icon="📁", layout="wide")

with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📁 Dataset")
st.markdown("Eksplorasi data GDP Growth Indonesia dari World Bank.")

DATA_PATH = "data/processed/dataset_indonesia.csv"

if not os.path.exists(DATA_PATH):
    st.warning("⚠️ Dataset belum tersedia. Jalankan notebook `01_data_collection.ipynb` terlebih dahulu.")
    st.stop()

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/dataset_indonesia.csv")

df = load_data()

# Summary metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Baris", len(df))
col2.metric("Total Kolom", len(df.columns))
col3.metric("Tahun Mulai", int(df["Year"].min()))
col4.metric("Tahun Akhir", int(df["Year"].max()))

st.markdown("---")

# Tabel data
st.markdown("### 📋 Tabel Data Lengkap")
st.dataframe(df.style.format({c: "{:.3f}" for c in df.columns if c != "Year"}),
             use_container_width=True, height=400)

st.markdown("---")

# Statistik deskriptif
st.markdown("### 📈 Statistik Deskriptif")
st.dataframe(df.describe().round(3), use_container_width=True)

st.markdown("---")

# Missing values
st.markdown("### 🔍 Pengecekan Missing Values")
missing = df.isnull().sum().reset_index()
missing.columns = ["Kolom", "Jumlah Missing"]
missing["Persen (%)"] = (missing["Jumlah Missing"] / len(df) * 100).round(2)
st.dataframe(missing, use_container_width=True, hide_index=True)

st.markdown("---")

# Kamus variabel
st.markdown("### 📖 Kamus Variabel")
dict_data = {
    "Variabel": ["GDP_Growth", "Inflation", "Unemployment", "Population_Growth",
                 "Exports", "Imports", "FDI", "Exchange_Rate"],
    "Deskripsi": [
        "Pertumbuhan GDP tahunan (target prediksi)",
        "Inflasi berdasarkan indeks harga konsumen",
        "Persentase pengangguran terhadap angkatan kerja",
        "Pertumbuhan populasi tahunan",
        "Ekspor barang dan jasa sebagai % GDP",
        "Impor barang dan jasa sebagai % GDP",
        "Investasi asing langsung bersih sebagai % GDP",
        "Nilai tukar resmi IDR terhadap USD"
    ],
    "Satuan": ["%", "%", "%", "%", "% GDP", "% GDP", "% GDP", "IDR/USD"],
    "Kode World Bank": [
        "NY.GDP.MKTP.KD.ZG", "FP.CPI.TOTL.ZG", "SL.UEM.TOTL.ZS",
        "SP.POP.GROW", "NE.EXP.GNFS.ZS", "NE.IMP.GNFS.ZS",
        "BX.KLT.DINV.WD.GD.ZS", "PA.NUS.FCRF"
    ]
}
st.dataframe(pd.DataFrame(dict_data), use_container_width=True, hide_index=True)

# Download button
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Dataset (CSV)", csv, "dataset_indonesia.csv", "text/csv")
