import streamlit as st
st.set_page_config(page_title="Prediksi", page_icon="🔮", layout="wide", initial_sidebar_state="collapsed")
from utils.navigation import show_navbar
show_navbar()
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.predictor import predict_all_models, load_report
from scripts.visualization import (
    plot_feature_importance, plot_prediction_comparison
)

st.set_page_config(page_title="Prediksi", page_icon="🔮", layout="wide")

with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🔮 Prediksi GDP Growth")
st.markdown("Masukkan nilai indikator ekonomi untuk memprediksi GDP Growth Indonesia.")

# Cek model tersedia
MODEL_PATH = "models/best_model.pkl"
if not os.path.exists(MODEL_PATH):
    st.warning("⚠️ Model belum tersedia. Jalankan notebook `03_preprocessing.ipynb` dan `04_modeling.ipynb` terlebih dahulu.")
    st.stop()

# Penjelasan variabel
with st.expander("📖 Penjelasan Variabel Input"):
    st.markdown("""
    | Variabel | Deskripsi | Satuan | Rentang Wajar |
    |---|---|---|---|
    | **Inflation** | Inflasi berdasarkan CPI | % | 2 – 80 |
    | **Unemployment** | Pengangguran terhadap angkatan kerja | % | 3 – 12 |
    | **Population Growth** | Pertumbuhan populasi tahunan | % | 0.5 – 2.5 |
    | **Exports** | Ekspor sebagai % GDP | % GDP | 15 – 45 |
    | **Imports** | Impor sebagai % GDP | % GDP | 15 – 40 |
    | **FDI** | Investasi asing langsung bersih | % GDP | -2 – 5 |
    | **Exchange Rate** | Nilai tukar IDR/USD | IDR/USD | 2000 – 16000 |
    """)

st.markdown("---")
st.markdown("### ✏️ Masukkan Nilai Indikator")

col1, col2 = st.columns(2)

with col1:
    inflation     = st.number_input("💹 Inflation (%)", min_value=0.0, max_value=100.0, value=3.5, step=0.1, format="%.2f")
    unemployment  = st.number_input("👥 Unemployment (%)", min_value=0.0, max_value=30.0, value=5.5, step=0.1, format="%.2f")
    pop_growth    = st.number_input("👶 Population Growth (%)", min_value=-1.0, max_value=5.0, value=1.2, step=0.1, format="%.2f")
    exports       = st.number_input("📤 Exports (% GDP)", min_value=0.0, max_value=100.0, value=22.0, step=0.5, format="%.2f")

with col2:
    imports       = st.number_input("📥 Imports (% GDP)", min_value=0.0, max_value=100.0, value=20.0, step=0.5, format="%.2f")
    fdi           = st.number_input("💰 FDI (% GDP)", min_value=-10.0, max_value=20.0, value=2.0, step=0.1, format="%.2f")
    exchange_rate = st.number_input("💱 Exchange Rate (IDR/USD)", min_value=500.0, max_value=30000.0, value=15000.0, step=100.0, format="%.0f")

st.markdown("---")

# Tombol prediksi
if st.button("🔮 Prediksi GDP Growth", type="primary"):
    input_dict = {
        "Inflation": inflation,
        "Unemployment": unemployment,
        "Population_Growth": pop_growth,
        "Exports": exports,
        "Imports": imports,
        "FDI": fdi,
        "Exchange_Rate": exchange_rate
    }

    with st.spinner("Menghitung prediksi..."):
        result = predict_all_models(input_dict)

    predictions  = result["predictions"]
    best_model   = result["best_model"]
    best_metrics = result["best_metrics"]
    best_pred    = predictions[best_model]

    color = "#27AE60" if best_pred >= 0 else "#E74C3C"
    icon  = "📈" if best_pred >= 5 else ("📊" if best_pred >= 0 else "📉")

    st.markdown(f"""
    <div class='result-box'>
        <h2>{icon} Prediksi GDP Growth</h2>
        <h1 style='font-size:3rem; color:{color};'>{best_pred:+.2f}%</h1>
        <p>Model Terbaik: <b>{best_model}</b></p>
    </div>
    """, unsafe_allow_html=True)

    # Interpretasi
    if best_pred >= 6:
        st.success("✅ **Pertumbuhan Tinggi** — Ekonomi tumbuh sangat baik (di atas rata-rata).")
    elif best_pred >= 4:
        st.info("ℹ️ **Pertumbuhan Normal** — Ekonomi tumbuh stabil sesuai rata-rata historis Indonesia.")
    elif best_pred >= 0:
        st.warning("⚠️ **Pertumbuhan Rendah** — Ekonomi tumbuh namun di bawah rata-rata historis.")
    else:
        st.error("🚨 **Resesi** — Prediksi menunjukkan kontraksi ekonomi (GDP negatif).")

    # Prediksi semua model
    st.markdown("### 📊 Prediksi GDP Growth per Model")
    df_pred = pd.DataFrame.from_dict(predictions, orient='index', columns=['Prediksi GDP Growth']).reset_index()
    df_pred.columns = ['Model', 'Prediksi GDP Growth']
    st.dataframe(df_pred.style.format({'Prediksi GDP Growth': '{:+.2f}%'}), use_container_width=True)
    st.plotly_chart(plot_prediction_comparison(predictions), use_container_width=True)

    # Metrik best model
    st.markdown("### 📈 Performa Model Terbaik")
    m1, m2, m3 = st.columns(3)
    m1.metric("CV R² Score", f"{best_metrics['cv_r2']:.4f}")
    m2.metric("CV MAE", f"{best_metrics['cv_mae']:.4f}%")
    m3.metric("CV RMSE", f"{best_metrics['cv_rmse']:.4f}%")

    # Feature importance
    st.markdown("### 🎯 Feature Importance")
    report = load_report()
    if report.get("feature_importance"):
        fig = plot_feature_importance(report["feature_importance"], best_model)
        st.plotly_chart(fig, use_container_width=True)

    # Tombol ke halaman Forecasting
    st.markdown("---")
    st.markdown("""
    <div class='info-box'>
        💡 <b>Ingin melihat proyeksi GDP otomatis ke depan?</b><br>
        Halaman <b>Forecasting</b> menampilkan prediksi GDP 2025–2030 berdasarkan tren historis 
        menggunakan ARIMA + 4 model ML secara otomatis — tanpa perlu input manual.
    </div>
    """, unsafe_allow_html=True)

    st.page_link("pages/06_Forecasting.py", label="📡 Lihat Forecast Otomatis 2025–2030 →", icon="📡")
   