"""Train all candidate models and save pickles + model report."""
import json
import joblib
import pickle
import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODEL_DIR = os.path.join(PROJECT_ROOT, 'models')

os.makedirs(MODEL_DIR, exist_ok=True)

with open(os.path.join(MODEL_DIR, 'data_split.pkl'), 'rb') as f:
    data = pickle.load(f)

X_train_s = data['X_train_scaled']
X_test_s = data['X_test_scaled']
y_train = data['y_train']
y_test = data['y_test']
FEATURES = data['features']

models = {
    'Linear Regression': LinearRegression(),
    'Ridge Regression': Ridge(alpha=1.0),
    'Decision Tree': DecisionTreeRegressor(max_depth=4, random_state=42),
    'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=4, random_state=42)
}

loo = LeaveOneOut()
results = {}

for name, model in models.items():
    print(f'Training: {name}...')
    mae_scores = -cross_val_score(model, X_train_s, y_train, cv=loo, scoring='neg_mean_absolute_error')
    rmse_scores = np.sqrt(-cross_val_score(model, X_train_s, y_train, cv=loo, scoring='neg_mean_squared_error'))
    r2_scores = cross_val_score(model, X_train_s, y_train, cv=loo, scoring='r2')

    model.fit(X_train_s, y_train)
    y_pred = model.predict(X_test_s)

    model_file = os.path.join(MODEL_DIR, f"{name.lower().replace(' ', '_')}.pkl")
    joblib.dump(model, model_file)

    results[name] = {
        'cv_mae': round(mae_scores.mean(), 4),
        'cv_rmse': round(rmse_scores.mean(), 4),
        'cv_r2': round(r2_scores.mean(), 4),
        'test_mae': round(mean_absolute_error(y_test, y_pred), 4),
        'test_rmse': round(np.sqrt(mean_squared_error(y_test, y_pred)), 4),
        'test_r2': round(r2_score(y_test, y_pred), 4),
        'y_pred': y_pred.tolist()
    }
    print(f'  CV MAE={results[name]["cv_mae"]} | CV RMSE={results[name]["cv_rmse"]} | CV R2={results[name]["cv_r2"]}')

best_name = max(results, key=lambda k: results[k]['cv_r2'])
print(f'Best model: {best_name}')

best_model = models[best_name]
best_model.fit(X_train_s, y_train)
joblib.dump(best_model, os.path.join(MODEL_DIR, 'best_model.pkl'))
print('Saved best_model.pkl')

if hasattr(best_model, 'feature_importances_'):
    fi = pd.Series(best_model.feature_importances_, index=FEATURES).sort_values(ascending=False)
elif hasattr(best_model, 'coef_'):
    fi = pd.Series(best_model.coef_, index=FEATURES).sort_values(ascending=False)
else:
    fi = pd.Series([], dtype=float)

feature_importance = fi.to_dict()

model_report = {
    'best_model': best_name,
    'features': FEATURES,
    'results': {name: {k: v for k, v in metrics.items() if k != 'y_pred'} for name, metrics in results.items()},
    'feature_importance': feature_importance,
    'y_test': y_test.tolist(),
    'y_pred_best': results[best_name]['y_pred'],
    'y_pred_all': {name: metrics['y_pred'] for name, metrics in results.items()}
}

with open(os.path.join(MODEL_DIR, 'model_report.json'), 'w') as f:
    json.dump(model_report, f, indent=2)

print('Saved model_report.json')
