import streamlit as st

st.set_page_config(
    page_title="Prediksi GDP Growth Indonesia",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
