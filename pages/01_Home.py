import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide", initial_sidebar_state="collapsed")
from utils.navigation import show_navbar
show_navbar()

with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🏠 Prediksi GDP Growth Indonesia")
st.markdown("### Proyek Machine Learning — Analisis & Prediksi Pertumbuhan Ekonomi")

st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class='info-box'>
    <h4>📅 Periode Data</h4>
    <p><b>1991 – 2024</b><br>34 tahun data historis</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class='info-box'>
    <h4>🔢 Jumlah Fitur</h4>
    <p><b>7 variabel ekonomi</b><br>dari World Bank</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class='info-box'>
    <h4>🤖 Jumlah Model</h4>
    <p><b>4 model ML</b><br>dievaluasi dengan LOOCV</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("## 📖 Tentang Proyek")
st.markdown("""
Proyek ini bertujuan memprediksi **GDP Growth (Pertumbuhan Ekonomi) Indonesia** 
menggunakan pendekatan Machine Learning berbasis data historis dari **World Bank**.

Kami menggunakan 7 indikator makroekonomi sebagai fitur untuk memprediksi 
pertumbuhan GDP tahunan Indonesia, dengan membandingkan performa 4 model ML.
""")

st.markdown("## 📊 Variabel yang Digunakan")

data_dict = {
    "Variabel": ["GDP_Growth", "Inflation", "Unemployment", "Population_Growth",
                 "Exports", "Imports", "FDI", "Exchange_Rate"],
    "Deskripsi": [
        "Pertumbuhan GDP (Target)",
        "Tingkat inflasi tahunan",
        "Tingkat pengangguran",
        "Pertumbuhan populasi",
        "Ekspor sebagai % GDP",
        "Impor sebagai % GDP",
        "Foreign Direct Investment % GDP",
        "Nilai tukar Rupiah terhadap USD"
    ],
    "Satuan": ["%", "%", "%", "%", "% GDP", "% GDP", "% GDP", "IDR/USD"],
    "Kode World Bank": [
        "NY.GDP.MKTP.KD.ZG", "FP.CPI.TOTL.ZG", "SL.UEM.TOTL.ZS",
        "SP.POP.GROW", "NE.EXP.GNFS.ZS", "NE.IMP.GNFS.ZS",
        "BX.KLT.DINV.WD.GD.ZS", "PA.NUS.FCRF"
    ]
}
import pandas as pd
st.dataframe(pd.DataFrame(data_dict), use_container_width=True, hide_index=True)

st.markdown("## 🗺️ Panduan Penggunaan")
st.markdown("""
1. **📁 Dataset** — lihat data mentah dan statistik deskriptif
2. **📊 Visualisasi** — eksplorasi grafik interaktif antar variabel  
3. **🔮 Prediksi** — masukkan nilai variabel untuk prediksi GDP Growth
4. **📝 Kesimpulan** — lihat evaluasi & perbandingan semua model
""")

st.markdown("---")
st.caption("Data: World Bank Open Data | Model: Scikit-learn | Visualisasi: Plotly")
