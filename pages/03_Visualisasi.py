import streamlit as st
st.set_page_config(page_title="Visualisasi", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")
from utils.navigation import show_navbar
show_navbar()
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from scripts.visualization import (
    plot_gdp_trend, plot_correlation_heatmap,
    plot_scatter, plot_all_scatter, plot_distribution
)

st.set_page_config(page_title="Visualisasi", page_icon="📊", layout="wide")

with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📊 Visualisasi Data")

DATA_PATH = "data/processed/dataset_indonesia.csv"
if not os.path.exists(DATA_PATH):
    st.warning("⚠️ Dataset belum tersedia. Jalankan notebook `01_data_collection.ipynb` terlebih dahulu.")
    st.stop()

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/dataset_indonesia.csv")

df = load_data()

# Tab navigasi
tab1, tab2, tab3, tab4 = st.tabs(["📈 Tren GDP", "🌡️ Korelasi", "🔵 Scatter Plot", "📊 Distribusi"])

@st.cache_data
def get_gdp_trend(_df):
    return plot_gdp_trend(_df)

@st.cache_data
def get_heatmap(_df):
    return plot_correlation_heatmap(_df)

@st.cache_data
def get_all_scatter(_df):
    return plot_all_scatter(_df)

@st.cache_data
def get_scatter(_df, feat):
    return plot_scatter(_df, feat)

@st.cache_data
def get_distribution(_df, col):
    return plot_distribution(_df, col)

@st.cache_data
def get_corr(_df):
    return _df.drop("Year", axis=1).corr()["GDP_Growth"].drop("GDP_Growth").sort_values(ascending=False)

with tab1:
    st.markdown("### Tren GDP Growth Indonesia (1991–2024)")
    st.plotly_chart(get_gdp_trend(df), use_container_width=True)
    st.info("""
    **Catatan:**
    - **1998**: Krisis Finansial Asia → GDP turun drastis (−13.1%)
    - **2020**: Pandemi COVID-19 → GDP negatif (−2.1%)
    - Secara umum Indonesia tumbuh **4–7% per tahun** pasca reformasi
    """)

with tab2:
    st.markdown("### Heatmap Korelasi Antar Variabel")
    st.plotly_chart(get_heatmap(df), use_container_width=True)
    corr = get_corr(df)
    st.markdown("**Korelasi terhadap GDP Growth:**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("🟢 **Korelasi Positif (tertinggi)**")
        for feat, val in corr[corr > 0].items():
            st.write(f"- {feat}: `{val:.3f}`")
    with col2:
        st.markdown("🔴 **Korelasi Negatif**")
        for feat, val in corr[corr <= 0].items():
            st.write(f"- {feat}: `{val:.3f}`")

with tab3:
    st.markdown("### Scatter Plot: Fitur vs GDP Growth")
    mode = st.radio("Tampilan:", ["Semua Sekaligus", "Pilih Satu Fitur"], horizontal=True)
    if mode == "Semua Sekaligus":
        st.plotly_chart(get_all_scatter(df), use_container_width=True)
    else:
        features = ["Inflation", "Unemployment", "Population_Growth",
                    "Exports", "Imports", "FDI", "Exchange_Rate"]
        feat = st.selectbox("Pilih fitur:", features)
        st.plotly_chart(get_scatter(df, feat), use_container_width=True)

with tab4:
    st.markdown("### Distribusi Variabel")
    all_cols = ["GDP_Growth", "Inflation", "Unemployment", "Population_Growth",
                "Exports", "Imports", "FDI", "Exchange_Rate"]
    col = st.selectbox("Pilih variabel:", all_cols)
    st.plotly_chart(get_distribution(df, col), use_container_width=True)
    d = df[col].dropna()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Mean", f"{d.mean():.3f}")
    c2.metric("Median", f"{d.median():.3f}")
    c3.metric("Std Dev", f"{d.std():.3f}")
    c4.metric("Missing", d.isna().sum())
   