import streamlit as st
st.set_page_config(page_title="Forecasting", page_icon="📡", layout="wide", initial_sidebar_state="collapsed")
from utils.navigation import show_navbar
show_navbar()
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

st.set_page_config(page_title="Forecasting", page_icon="📡", layout="wide")

with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📡 Forecasting GDP Growth Indonesia")
st.markdown("Forecast otomatis — setiap indikator ekonomi di-forecast pakai ARIMA, lalu hasilnya dimasukkan ke 4 model ML untuk menghasilkan GDP forecast.")

FORECAST_PATH = "models/forecast_report.json"
if not os.path.exists(FORECAST_PATH):
    st.warning("⚠️ Forecast belum tersedia. Jalankan notebook `05_forecasting.ipynb` terlebih dahulu.")
    st.stop()

@st.cache_data
def load_forecast_report():
    with open(FORECAST_PATH) as f:
        return json.load(f)

@st.cache_data
def load_hist_data():
    path = "data/processed/dataset_indonesia.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

report  = load_forecast_report()
hist_df = load_hist_data()

forecast_years      = report['forecast_years']
gdp_forecasts       = report['gdp_forecasts']
indicator_forecasts = report['indicator_forecasts']
best_model          = report['best_model']
hist_years          = report['gdp_historical']['years']
hist_values         = report['gdp_historical']['values']

MODEL_COLORS = {
    'Linear Regression': '#3B5BA5',
    'Ridge Regression':  '#1D9E75',
    'Decision Tree':     '#E67E22',
    'Random Forest':     '#8E44AD',
}

def hex_to_rgba(hex_color, alpha=0.13):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r},{g},{b},{alpha})'

tab1, tab2, tab3 = st.tabs([
    "📈 GDP Forecast",
    "🔢 Forecast Indikator",
    "📋 Tabel & Ringkasan"
])

# ── TAB 1 ────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("### GDP Growth Historis + Forecast 2025–2030")

    col_ctrl, col_chart = st.columns([1, 3])

    with col_ctrl:
        st.markdown("**Tampilkan model:**")
        active_models = []
        for name in gdp_forecasts:
            checked = st.checkbox(
                f"{'⭐ ' if name == best_model else ''}{name}",
                value=True, key=f"fc_{name}"
            )
            if checked:
                active_models.append(name)

        st.markdown("---")
        show_hist     = st.checkbox("Tampilkan data historis", value=True)
        show_ci       = st.checkbox("Tampilkan area proyeksi", value=True)
        zoom_forecast = st.checkbox("Zoom ke area forecast", value=False)

    with col_chart:
        fig = go.Figure()

        if show_hist:
            fig.add_trace(go.Scatter(
                x=hist_years, y=hist_values,
                mode='lines+markers',
                name='GDP Aktual',
                line=dict(color='#2C3E50', width=2.5),
                marker=dict(size=5),
                hovertemplate='<b>%{x}</b><br>Aktual: %{y:.2f}%<extra></extra>'
            ))

        fig.add_vline(
            x=2024.5, line_dash='dash', line_color='gray', opacity=0.4,
            annotation_text='← Historis | Forecast →',
            annotation_position='top', annotation_font_size=11
        )

        for name in active_models:
            if name not in gdp_forecasts:
                continue
            preds   = gdp_forecasts[name]
            color   = MODEL_COLORS.get(name, '#888888')
            is_best = name == best_model

            fig.add_trace(go.Scatter(
                x=forecast_years, y=preds,
                mode='lines+markers',
                name=f"{name}{' ★' if is_best else ''}",
                line=dict(color=color, width=2.5 if is_best else 1.6,
                          dash=None if is_best else 'dash'),
                marker=dict(size=8 if is_best else 5,
                            symbol='diamond' if is_best else 'circle',
                            color=color),
                hovertemplate=f'<b>%{{x}}</b><br>{name}: %{{y:.2f}}%<extra></extra>'
            ))

            if is_best and show_ci:
                fig.add_trace(go.Scatter(
                    x=forecast_years + forecast_years[::-1],
                    y=[v + 0.5 for v in preds] + [v - 0.5 for v in preds[::-1]],
                    fill='toself',
                    fillcolor=hex_to_rgba(color, 0.13),
                    line=dict(color='rgba(0,0,0,0)'),
                    showlegend=False,
                    hoverinfo='skip',
                    name='confidence'
                ))

        fig.add_hline(y=0, line_dash='dot', line_color='red', opacity=0.25)

        # Range Y
        if zoom_forecast:
            all_vals = []
            for name in active_models:
                if name in gdp_forecasts:
                    all_vals += gdp_forecasts[name]
            y_min = min(all_vals) - 0.5 if all_vals else -5
            y_max = max(all_vals) + 0.5 if all_vals else 10
        else:
            all_vals = list(hist_values)
            for name in active_models:
                if name in gdp_forecasts:
                    all_vals += gdp_forecasts[name]
            y_min = min(all_vals) - 1
            y_max = max(all_vals) + 1

        fig.update_layout(
            xaxis_title='Tahun',
            yaxis_title='GDP Growth (%)',
            hovermode='x unified',
            template='plotly_white',
            height=420,
            yaxis=dict(range=[y_min, y_max]),
            legend=dict(orientation='h', y=-0.2)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"### Ringkasan Forecast — {best_model} ⭐")
    best_preds = gdp_forecasts[best_model]
    cols = st.columns(len(forecast_years))
    for i, (yr, val) in enumerate(zip(forecast_years, best_preds)):
        clr = "#27AE60" if val >= 0 else "#E74C3C"
        with cols[i]:
            st.markdown(f"""
            <div style='background:#f8f9fa;border-radius:8px;padding:.6rem;text-align:center'>
                <p style='margin:0;font-size:11px;color:#888'>{yr}</p>
                <p style='margin:.2rem 0;font-size:1.3rem;font-weight:600;color:{clr}'>{val:+.2f}%</p>
            </div>
            """, unsafe_allow_html=True)

# ── TAB 2 ────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("### Forecast Indikator Ekonomi (ARIMA)")
    st.caption("Setiap indikator di-forecast secara independen menggunakan ARIMA dengan order terbaik (grid search AIC).")

    INDICATORS = list(indicator_forecasts.keys())
    selected = st.selectbox("Pilih indikator:", INDICATORS)

    if selected and not hist_df.empty:
        hist_vals_ind = hist_df[selected].tolist()
        hist_yrs_ind  = hist_df['Year'].tolist()
        fc_vals       = indicator_forecasts[selected]

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=hist_yrs_ind, y=hist_vals_ind,
            mode='lines+markers', name='Historis',
            line=dict(color='#2C3E50', width=2),
            marker=dict(size=5),
            hovertemplate='<b>%{x}</b><br>' + selected + ': %{y:.3f}<extra></extra>'
        ))
        fig2.add_trace(go.Scatter(
            x=forecast_years, y=fc_vals,
            mode='lines+markers', name='Forecast ARIMA',
            line=dict(color='#E74C3C', width=2, dash='dash'),
            marker=dict(size=7, symbol='diamond'),
            hovertemplate='<b>%{x}</b><br>Forecast: %{y:.3f}<extra></extra>'
        ))
        fig2.add_vline(x=2024.5, line_dash='dash', line_color='gray', opacity=0.4)
        fig2.update_layout(
            title=f'Forecast {selected} — ARIMA',
            xaxis_title='Tahun', yaxis_title=selected,
            template='plotly_white', height=380,
            hovermode='x unified',
            legend=dict(orientation='h', y=-0.2)
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### Nilai Forecast Semua Indikator")
    tbl = {'Tahun': forecast_years}
    for ind in INDICATORS:
        tbl[ind] = [round(v, 3) for v in indicator_forecasts[ind]]
    st.dataframe(pd.DataFrame(tbl).set_index('Tahun'), use_container_width=True)

# ── TAB 3 ────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("### Tabel GDP Forecast Per Tahun — Semua Model")
    tbl2 = {'Tahun': forecast_years}
    for name, preds in gdp_forecasts.items():
        label = f"{'⭐ ' if name == best_model else ''}{name}"
        tbl2[label] = [f"{v:+.2f}%" for v in preds]
    st.dataframe(pd.DataFrame(tbl2).set_index('Tahun'), use_container_width=True)

    st.markdown("### Rata-rata GDP Forecast (2025–2030)")
    cols2 = st.columns(len(gdp_forecasts))
    for i, (name, preds) in enumerate(gdp_forecasts.items()):
        avg = sum(preds) / len(preds)
        clr = "#27AE60" if avg >= 0 else "#E74C3C"
        with cols2[i]:
            st.markdown(f"""
            <div style='background:#f8f9fa;border-radius:8px;padding:.75rem;text-align:center'>
                <p style='margin:0;font-size:11px;color:#888'>{'⭐ ' if name == best_model else ''}{name}</p>
                <p style='margin:.2rem 0;font-size:1.4rem;font-weight:600;color:{clr}'>{avg:+.2f}%</p>
                <p style='margin:0;font-size:10px;color:#aaa'>rata-rata {len(forecast_years)} tahun</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### Pipeline Forecasting")
    st.info("""
    **Cara kerja:**
    1. **ARIMA** mem-forecast 7 indikator ekonomi (Inflasi, Pengangguran, Ekspor, Impor, FDI, Pertumbuhan Populasi, Nilai Tukar) secara independen untuk 2025–2030
    2. Hasil forecast indikator disusun menjadi input untuk model ML
    3. **4 model ML** (Linear Regression, Ridge, Decision Tree, Random Forest) masing-masing memprediksi GDP Growth dari input tersebut
    4. Hasil semua model ditampilkan dan dibandingkan
    """)
   