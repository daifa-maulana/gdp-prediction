"""
visualization.py
Fungsi visualisasi siap pakai untuk Streamlit.
Semua fungsi return fig Plotly agar interaktif di browser.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


BLUE = "#3B5BA5"
RED  = "#E74C3C"
GREEN = "#27AE60"
GRAY = "#95A5A6"


def plot_gdp_trend(df: pd.DataFrame) -> go.Figure:
    """Line chart tren GDP Growth Indonesia."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Year"], y=df["GDP_Growth"],
        mode="lines+markers",
        line=dict(color=BLUE, width=2.5),
        marker=dict(size=6),
        name="GDP Growth",
        hovertemplate="<b>%{x}</b><br>GDP Growth: %{y:.2f}%<extra></extra>"
    ))
    fig.add_hrect(y0=0, y1=df["GDP_Growth"].max() + 1,
                  fillcolor="rgba(39,174,96,0.08)", line_width=0)
    fig.add_hrect(y0=df["GDP_Growth"].min() - 1, y1=0,
                  fillcolor="rgba(231,76,60,0.08)", line_width=0)
    fig.add_hline(y=0, line_dash="dash", line_color=RED, opacity=0.5)
    for year, label in [(1998, "Krisis 1998"), (2020, "COVID-19")]:
        val = df.loc[df["Year"] == year, "GDP_Growth"]
        if not val.empty:
            fig.add_annotation(x=year, y=val.values[0],
                                text=label, showarrow=True,
                                arrowhead=2, arrowcolor=RED,
                                font=dict(color=RED, size=11),
                                ax=40, ay=-40)
    fig.update_layout(
        title="Tren GDP Growth Indonesia (1991–2024)",
        xaxis_title="Tahun", yaxis_title="GDP Growth (%)",
        hovermode="x unified", template="plotly_white",
        height=420
    )
    return fig


def plot_correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    """Heatmap korelasi antar variabel."""
    corr = df.drop("Year", axis=1).corr().round(2)
    fig = px.imshow(
        corr, text_auto=True, color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1, aspect="auto",
        title="Heatmap Korelasi Antar Variabel"
    )
    fig.update_layout(template="plotly_white", height=500)
    return fig


def plot_scatter(df: pd.DataFrame, feature: str) -> go.Figure:
    """Scatter plot satu fitur vs GDP Growth."""
    d = df[["Year", feature, "GDP_Growth"]].dropna()
    fig = px.scatter(
        d, x=feature, y="GDP_Growth", hover_data=["Year"],
        trendline="ols", color_discrete_sequence=[BLUE],
        title=f"{feature} vs GDP Growth",
        labels={"GDP_Growth": "GDP Growth (%)"}
    )
    fig.update_layout(template="plotly_white", height=380)
    return fig


def plot_all_scatter(df: pd.DataFrame) -> go.Figure:
    """Grid scatter plot semua fitur vs GDP Growth."""
    features = ["Inflation", "Unemployment", "Population_Growth",
                "Exports", "Imports", "FDI", "Exchange_Rate"]
    fig = make_subplots(rows=2, cols=4,
                        subplot_titles=features,
                        vertical_spacing=0.15)
    for i, feat in enumerate(features):
        row, col = divmod(i, 4)
        d = df[[feat, "GDP_Growth"]].dropna()
        fig.add_trace(
            go.Scatter(x=d[feat], y=d["GDP_Growth"],
                       mode="markers",
                       marker=dict(color=BLUE, size=7, opacity=0.7),
                       showlegend=False),
            row=row + 1, col=col + 1
        )
    fig.update_layout(height=550, title_text="Scatter Plot: Semua Fitur vs GDP Growth",
                      template="plotly_white")
    return fig


def plot_distribution(df: pd.DataFrame, column: str) -> go.Figure:
    """Histogram distribusi satu kolom."""
    d = df[column].dropna()
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=d, nbinsx=15,
        marker_color=BLUE, opacity=0.85,
        name=column
    ))
    fig.add_vline(x=d.mean(), line_dash="dash", line_color=RED,
                  annotation_text=f"Mean: {d.mean():.2f}",
                  annotation_position="top right")
    fig.update_layout(
        title=f"Distribusi {column}",
        xaxis_title=column, yaxis_title="Frekuensi",
        template="plotly_white", height=360
    )
    return fig


def plot_feature_importance(importance_dict: dict, model_name: str) -> go.Figure:
    """Bar chart feature importance."""
    fi = pd.Series(importance_dict).sort_values()
    fig = go.Figure(go.Bar(
        x=fi.values, y=fi.index,
        orientation="h",
        marker_color=BLUE
    ))
    fig.update_layout(
        title=f"Feature Importance — {model_name}",
        xaxis_title="Importance / Koefisien",
        template="plotly_white", height=380
    )
    return fig


def plot_actual_vs_predicted(y_test: list, y_pred: list) -> go.Figure:
    """Actual vs Predicted line chart."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=y_test, mode="lines+markers",
        name="Actual", line=dict(color=BLUE, width=2),
        marker=dict(size=7)
    ))
    fig.add_trace(go.Scatter(
        y=y_pred, mode="lines+markers",
        name="Predicted", line=dict(color=RED, dash="dash", width=2),
        marker=dict(size=7, symbol="square")
    ))
    fig.update_layout(
        title="Actual vs Predicted — GDP Growth",
        xaxis_title="Data Point", yaxis_title="GDP Growth (%)",
        template="plotly_white", height=380,
        legend=dict(orientation="h", y=1.1)
    )
    return fig


def plot_all_models_vs_actual(results: dict, y_test: list) -> go.Figure:
    """Line chart actual values and predicted values for all models."""
    fig = go.Figure()
    x = list(range(1, len(y_test) + 1))
    fig.add_trace(go.Scatter(
        x=x, y=y_test, mode="lines+markers",
        name="Actual", line=dict(color=BLUE, width=4),
        marker=dict(size=7)
    ))
    palette = [GREEN, RED, '#E67E22', '#8E44AD', '#2980B9', '#16A085']
    for i, (name, r) in enumerate(results.items()):
        y_pred = r.get('y_pred') or r.get('y_predicted')
        if not y_pred:
            continue
        fig.add_trace(go.Scatter(
            x=x, y=y_pred,
            mode="lines+markers",
            name=name,
            line=dict(color=palette[i % len(palette)], dash="dash", width=2),
            marker=dict(size=6)
        ))
    fig.update_layout(
        title="Actual vs Prediksi Semua Model",
        xaxis_title="Data Point", yaxis_title="GDP Growth (%)",
        template="plotly_white", height=450,
        legend=dict(orientation="h", y=1.12)
    )
    return fig


def plot_prediction_comparison(predictions: dict) -> go.Figure:
    """Bar chart perbandingan prediksi GDP Growth dari semua model."""
    models = list(predictions.keys())
    values = list(predictions.values())
    colors = [GREEN if v >= 0 else RED for v in values]
    fig = go.Figure(go.Bar(
        x=models,
        y=values,
        marker_color=colors,
        text=[f"{v:+.2f}%" for v in values],
        textposition="auto"
    ))
    fig.update_layout(
        title="Prediksi GDP Growth per Model",
        xaxis_title="Model",
        yaxis_title="Prediksi GDP Growth (%)",
        template="plotly_white", height=420,
        yaxis=dict(zeroline=True, zerolinecolor=GRAY, zerolinewidth=2)
    )
    return fig


def plot_model_comparison(results: dict) -> go.Figure:
    """Bar chart perbandingan metrik semua model."""
    models = list(results.keys())
    metrics = ["cv_mae", "cv_rmse", "cv_r2"]
    labels  = ["CV MAE", "CV RMSE", "CV R²"]
    colors  = [RED, "#E67E22", GREEN]
    fig = make_subplots(rows=1, cols=3, subplot_titles=labels)
    for i, (metric, label, color) in enumerate(zip(metrics, labels, colors)):
        vals = [results[m][metric] for m in models]
        fig.add_trace(
            go.Bar(x=models, y=vals, marker_color=color,
                   name=label, showlegend=False),
            row=1, col=i + 1
        )
    fig.update_layout(
        title="Perbandingan Performa Model (LOOCV)",
        template="plotly_white", height=400
    )
    return fig


# ── Fungsi baru untuk proyeksi multi-tahun ───────────────────────────────────

MODEL_COLORS = {
    'Linear Regression': '#3B5BA5',
    'Ridge Regression':  '#1D9E75',
    'Decision Tree':     '#E67E22',
    'Random Forest':     '#8E44AD',
}

MODEL_DASH = {
    'Linear Regression': None,
    'Ridge Regression':  'dash',
    'Decision Tree':     'dot',
    'Random Forest':     'dashdot',
}


def plot_future_projection(hist_df, future_result, active_models=None, best_model=None):
    """Grafik historis + proyeksi ke depan semua model."""
    years_future = future_result['years']
    predictions  = future_result['predictions']
    best         = best_model or future_result.get('best_model')

    if active_models is None:
        active_models = list(predictions.keys())

    fig = go.Figure()

    # Data historis
    fig.add_trace(go.Scatter(
        x=hist_df['Year'], y=hist_df['GDP_Growth'],
        mode='lines+markers',
        name='Historis (aktual)',
        line=dict(color='#2C3E50', width=2.5),
        marker=dict(size=5),
        hovertemplate='<b>%{x}</b><br>Aktual: %{y:.2f}%<extra></extra>'
    ))

    # Garis pemisah historis / proyeksi
    if not hist_df.empty:
        fig.add_vline(
            x=hist_df['Year'].max() + 0.5,
            line_dash='dash', line_color='gray', opacity=0.4,
            annotation_text='← Historis | Proyeksi →',
            annotation_position='top',
            annotation_font_size=11
        )

    # Prediksi tiap model
    for name in active_models:
        if name not in predictions:
            continue
        color   = MODEL_COLORS.get(name, '#888888')
        dash    = MODEL_DASH.get(name)
        is_best = (name == best)
        label   = f'{name} ★' if is_best else name

        fig.add_trace(go.Scatter(
            x=years_future,
            y=predictions[name],
            mode='lines+markers',
            name=label,
            line=dict(color=color, width=2.5 if is_best else 1.6, dash=dash),
            marker=dict(size=7 if is_best else 5,
                        symbol='diamond' if is_best else 'circle',
                        color=color),
            hovertemplate=f'<b>%{{x}}</b><br>{name}: %{{y:.2f}}%<extra></extra>'
        ))

    fig.add_hline(y=0, line_dash='dot', line_color='red', opacity=0.25)

    # Hitung range Y supaya grafik tidak flat
    all_vals = []
    if not hist_df.empty:
        all_vals += hist_df['GDP_Growth'].tolist()
    for name in active_models:
        if name in predictions:
            all_vals += predictions[name]

    if all_vals:
        y_min = min(all_vals) - 1
        y_max = max(all_vals) + 1
    else:
        y_min, y_max = -5, 10

    fig.update_layout(
        title=f'Proyeksi GDP Growth Indonesia — {years_future[0]}–{years_future[-1]}',
        xaxis_title='Tahun',
        yaxis_title='GDP Growth (%)',
        hovermode='x unified',
        template='plotly_white',
        height=440,
        legend=dict(orientation='h', y=-0.22),
        yaxis=dict(range=[y_min, y_max])
    )
    return fig


def plot_prediction_bars(all_preds, best_model=None):
    """Horizontal bar chart prediksi semua model untuk satu titik."""
    names  = list(all_preds.keys())
    values = [all_preds[n] for n in names]
    colors = [MODEL_COLORS.get(n, '#888') for n in names]
    labels = [f'{n} ★' if n == best_model else n for n in names]

    fig = go.Figure(go.Bar(
        x=values, y=labels,
        orientation='h',
        marker_color=colors,
        text=[f'{v:+.2f}%' for v in values],
        textposition='outside',
        hovertemplate='%{y}: %{x:.4f}%<extra></extra>'
    ))
    fig.add_vline(x=0, line_dash='dash', line_color='gray', opacity=0.5)
    fig.update_layout(
        title='Prediksi GDP Growth — Semua Model',
        xaxis_title='GDP Growth (%)',
        template='plotly_white',
        height=280,
        margin=dict(r=60)
    )
    return fig