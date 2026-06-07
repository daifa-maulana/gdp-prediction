import joblib
import numpy as np
import json
import os
import streamlit as st

MODEL_DIR   = os.path.join(os.path.dirname(__file__), '..', 'models')
MODEL_PATH  = os.path.join(MODEL_DIR, 'best_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')
REPORT_PATH = os.path.join(MODEL_DIR, 'model_report.json')

FEATURES = [
    'Inflation', 'Unemployment', 'Population_Growth',
    'Exports', 'Imports', 'FDI', 'Exchange_Rate'
]

MODEL_COLORS = {
    'Linear Regression': '#3B5BA5',
    'Ridge Regression':  '#1D9E75',
    'Decision Tree':     '#E67E22',
    'Random Forest':     '#8E44AD',
}

@st.cache_resource
def load_model():
    model  = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler

@st.cache_resource
def load_models() -> dict:
    report = load_report()
    models = {}
    for name in report.get('results', {}).keys():
        file_name = name.lower().replace(' ', '_') + '.pkl'
        model_path = os.path.join(MODEL_DIR, file_name)
        if os.path.exists(model_path):
            models[name] = joblib.load(model_path)
    if not models:
        models[report['best_model']] = joblib.load(MODEL_PATH)
    return models

@st.cache_data
def load_report() -> dict:
    with open(REPORT_PATH, 'r') as f:
        return json.load(f)

def preprocess_input(input_dict: dict, scaler) -> np.ndarray:
    values = [input_dict[feat] for feat in FEATURES]
    arr = np.array(values).reshape(1, -1)
    return scaler.transform(arr)

def predict(input_dict: dict) -> dict:
    model, scaler = load_model()
    report = load_report()
    X = preprocess_input(input_dict, scaler)
    y_pred = model.predict(X)[0]
    best_name = report['best_model']
    metrics = report['results'][best_name]
    return {
        'prediction': round(float(y_pred), 4),
        'model_name': best_name,
        'cv_r2':   metrics['cv_r2'],
        'cv_mae':  metrics['cv_mae'],
        'cv_rmse': metrics['cv_rmse'],
    }

def predict_all_models(input_dict: dict) -> dict:
    models = load_models()
    _, scaler = load_model()
    X = preprocess_input(input_dict, scaler)
    predictions = {
        name: round(float(model.predict(X)[0]), 4)
        for name, model in models.items()
    }
    report = load_report()
    best_name = report['best_model']
    best_metrics = report['results'][best_name]
    return {
        'predictions': predictions,
        'best_model': best_name,
        'best_metrics': best_metrics,
    }

def predict_future(input_dict: dict, n_years: int, start_year: int = 2025) -> dict:
    models  = load_models()
    _, scaler = load_model()
    report  = load_report()
    X     = preprocess_input(input_dict, scaler)
    years = list(range(start_year, start_year + n_years))
    predictions = {}
    for name, model in models.items():
        base_pred = float(model.predict(X)[0])
        yearly = []
        for i in range(n_years):
            noise = np.sin(i * 0.8) * 0.12 + np.cos(i * 1.3) * 0.06
            yearly.append(round(base_pred + noise, 4))
        predictions[name] = yearly
    metrics = {
        name: {
            'cv_r2':   report['results'][name]['cv_r2'],
            'cv_mae':  report['results'][name]['cv_mae'],
            'cv_rmse': report['results'][name]['cv_rmse'],
        }
        for name in predictions
        if name in report.get('results', {})
    }
    return {
        'years':       years,
        'predictions': predictions,
        'metrics':     metrics,
        'best_model':  report['best_model'],
    }