import streamlit as st

st.set_page_config(
    page_title="Prediksi GDP Growth Indonesia",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)
from utils.navigation import show_navbar
show_navbar()
# Load CSS
with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.sidebar.title("📊 GDP Indonesia")
st.sidebar.markdown("**Machine Learning Project**")
st.sidebar.markdown("---")
st.sidebar.markdown("""
**Navigasi:**
- 🏠 Home
- 📁 Dataset
- 📊 Visualisasi
- 🔮 Prediksi
- 📝 Kesimpulan
""")
st.sidebar.markdown("---")
st.sidebar.caption("Data: World Bank | 1991–2024")

st.title("📈 Prediksi GDP Growth Indonesia")
st.markdown("""
Selamat datang! Gunakan menu di sidebar untuk navigasi antar halaman.

| Halaman | Deskripsi |
|---|---|
| 🏠 Home | Informasi proyek |
| 📁 Dataset | Eksplorasi data |
| 📊 Visualisasi | Grafik interaktif |
| 🔮 Prediksi | Input & prediksi GDP |
| 📝 Kesimpulan | Evaluasi model |
""")
st.markdown("---")
st.markdown("##### 🧭 Navigasi Halaman")
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.page_link("pages/01_Home.py", label="📖 Info", use_container_width=True)
with col2:
    st.page_link("pages/02_Dataset.py", label="📁 Dataset", use_container_width=True)
with col3:
    st.page_link("pages/03_Visualisasi.py", label="📊 Visualisasi", use_container_width=True)
with col4:
    st.page_link("pages/04_Prediksi.py", label="🔮 Prediksi", use_container_width=True)
with col5:
    st.page_link("pages/05_Kesimpulan.py", label="📝 Kesimpulan", use_container_width=True)
with col6:
    st.page_link("pages/06_Forecasting.py", label="📡 Forecasting", use_container_width=True)