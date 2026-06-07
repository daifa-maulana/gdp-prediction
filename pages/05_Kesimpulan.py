import streamlit as st
st.set_page_config(page_title="Kesimpulan", page_icon="📝", layout="wide", initial_sidebar_state="collapsed")
from utils.navigation import show_navbar
show_navbar()
import pandas as pd
import json, os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from scripts.visualization import plot_actual_vs_predicted, plot_model_comparison, plot_all_models_vs_actual

st.set_page_config(page_title="Kesimpulan", page_icon="📝", layout="wide")

with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📝 Kesimpulan & Evaluasi Model")

REPORT_PATH = "models/model_report.json"
if not os.path.exists(REPORT_PATH):
    st.warning("⚠️ Model report belum tersedia. Jalankan notebook `04_modeling.ipynb` terlebih dahulu.")
    st.stop()

with open(REPORT_PATH, encoding="utf-8") as f:
    report = json.load(f)

best    = report["best_model"]
results = report["results"]

# ── Model terbaik ────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='result-box'>
    <h3>🏆 Model Terbaik</h3>
    <h2>{best}</h2>
    <p>CV R² = <b>{results[best]['cv_r2']}</b> &nbsp;|&nbsp;
       CV MAE = <b>{results[best]['cv_mae']}%</b> &nbsp;|&nbsp;
       CV RMSE = <b>{results[best]['cv_rmse']}%</b></p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Tabel perbandingan — pisah CV dan Test ───────────────────────────────────
st.markdown("### 📊 Perbandingan Performa Semua Model")

col_cv, col_test = st.columns(2)

rows_cv   = []
rows_test = []
for name, r in results.items():
    label = f"🏆 {name}" if name == best else name
    rows_cv.append({
        "Model":    label,
        "CV MAE":   r["cv_mae"],
        "CV RMSE":  r["cv_rmse"],
        "CV R²":    r["cv_r2"],
    })
    rows_test.append({
        "Model":     label,
        "Test MAE":  r["test_mae"],
        "Test RMSE": r["test_rmse"],
        "Test R²":   r["test_r2"],
    })

df_cv   = pd.DataFrame(rows_cv)
df_test = pd.DataFrame(rows_test)

with col_cv:
    st.markdown("**Cross-Validation (LOOCV)**")
    st.dataframe(
        df_cv.style
            .highlight_max(subset=["CV R²"], color="#1a3a2a")
            .highlight_min(subset=["CV MAE","CV RMSE"], color="#1a3a2a")
            .format({"CV MAE": "{:.4f}", "CV RMSE": "{:.4f}", "CV R²": "{:.4f}"}),
        use_container_width=True, hide_index=True
    )

with col_test:
    st.markdown("**Test Set**")
    st.dataframe(
        df_test.style
            .highlight_max(subset=["Test R²"], color="#1a3a2a")
            .highlight_min(subset=["Test MAE","Test RMSE"], color="#1a3a2a")
            .format({"Test MAE": "{:.4f}", "Test RMSE": "{:.4f}", "Test R²": "{:.4f}"}),
        use_container_width=True, hide_index=True
    )

# ── Metrik 4 kartu ───────────────────────────────────────────────────────────
st.markdown("#### Metrik Model Terbaik")
c1, c2, c3, c4 = st.columns(4)
c1.metric("CV R²",    f"{results[best]['cv_r2']:.4f}")
c2.metric("CV MAE",   f"{results[best]['cv_mae']:.4f}")
c3.metric("CV RMSE",  f"{results[best]['cv_rmse']:.4f}")
c4.metric("Test R²",  f"{results[best]['test_r2']:.4f}")

# ── Chart perbandingan ───────────────────────────────────────────────────────
st.plotly_chart(plot_model_comparison(results), use_container_width=True)

st.markdown("---")

# ── Actual vs Predicted ──────────────────────────────────────────────────────
st.markdown("### 📈 Actual vs Predicted — Model Terbaik")
y_test = report.get("y_test", [])
y_pred = report.get("y_pred_best", [])
if y_test and y_pred:
    st.plotly_chart(plot_actual_vs_predicted(y_test, y_pred), use_container_width=True)
else:
    st.info("Data prediksi belum tersedia.")

st.markdown("---")

# ── Actual vs semua model ────────────────────────────────────────────────────
st.markdown("### 📈 Actual vs Prediksi Semua Model")
if y_test and any("y_pred" in r for r in results.values()):
    st.plotly_chart(plot_all_models_vs_actual(results, y_test), use_container_width=True)
else:
    st.info("Jalankan ulang `04_modeling.ipynb` untuk menampilkan prediksi semua model.")

st.markdown("---")

# ── Ringkasan EDA ────────────────────────────────────────────────────────────
st.markdown("### 🔍 Ringkasan Temuan EDA")

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("""
    <div class='info-box'>
    <b>📉 Krisis Signifikan</b><br><br>
    • <b>1998</b> — Krisis Finansial Asia: GDP <b>−13.1%</b><br>
    • <b>2020</b> — COVID-19: GDP <b>−2.1%</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box' style='margin-top:12px'>
    <b>📈 Tren Umum</b><br><br>
    • Pasca reformasi (1999–2019): rata-rata <b>~5.2%/tahun</b><br>
    • Konsisten tumbuh di atas rata-rata negara berkembang
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class='info-box'>
    <b>🔧 Penanganan Data</b><br><br>
    • Missing values: <b>interpolasi linear</b><br>
    • Outlier 1998 & 2020 <b>dipertahankan</b> (kejadian nyata)<br>
    • Normalisasi: <b>StandardScaler</b> (fit on train only)
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box' style='margin-top:12px'>
    <b>📊 Data</b><br><br>
    • Sumber: <b>World Bank API</b><br>
    • Periode: <b>1991–2024</b> (34 tahun)<br>
    • 8 indikator ekonomi
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Metodologi ───────────────────────────────────────────────────────────────
st.markdown("### 🧪 Metodologi")
st.markdown("""
| Tahapan | Detail |
|---|---|
| **Data** | World Bank API — 8 indikator, 1991–2024 |
| **Preprocessing** | Interpolasi linear, StandardScaler (fit on train only) |
| **Outlier** | Dipertahankan (1998, 2020 = kejadian nyata) |
| **Split** | 80% training / 20% testing (no shuffle — time series) |
| **Evaluasi** | Leave-One-Out Cross Validation (LOOCV) |
| **Metrik** | MAE, RMSE, R² Score |
| **Model** | Linear Regression, Ridge, Decision Tree, Random Forest |
| **Forecasting** | ARIMA per indikator → 4 model ML → GDP forecast |
""")

st.markdown("---")
st.caption("Proyek Machine Learning — Prediksi GDP Growth Indonesia | Data: World Bank")
