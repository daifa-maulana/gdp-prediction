"""
preprocessing.py
Fungsi preprocessing yang bisa di-import dari notebook atau script lain.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import os


FEATURES = [
    'Inflation', 'Unemployment', 'Population_Growth',
    'Exports', 'Imports', 'FDI', 'Exchange_Rate'
]
TARGET = 'GDP_Growth'


def load_dataset(path: str = 'data/processed/dataset_indonesia.csv') -> pd.DataFrame:
    return pd.read_csv(path)


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Interpolasi linear untuk time series."""
    df = df.copy().set_index('Year')
    df = df.interpolate(method='linear', limit_direction='both')
    return df.reset_index().dropna()


def split_features_target(df: pd.DataFrame):
    X = df[FEATURES]
    y = df[TARGET]
    return X, y


def scale_features(X_train, X_test, save_path: str = None):
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s  = scaler.transform(X_test)
    if save_path:
        joblib.dump(scaler, save_path)
    return X_train_s, X_test_s, scaler
