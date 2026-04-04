import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

def optimize_and_evaluate():
    # Load dataset
    df = pd.read_csv('clean_intern_data.csv')
    
    # Feature Engineering (Standard Scaling)
    features = ['task_completion_rate', 'consistency_score', 'engagement_metric']
    X = df[features]
    y = df['performance_score']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save the scaler for deployment
    joblib.dump(scaler, 'scaler.pkl')
    
    # Hyperparameter Tuning for Gradient Boosting Regressor
    param_grid = {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 4, 5]
    }
    
    gb = GradientBoostingRegressor(random_state=42)
    grid_search = GridSearchCV(estimator=gb, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error', n_jobs=-1, verbose=1)
    
    print("Starting Grid Search Optimization...")
    grid_search.fit(X_train_scaled, y_train)
    
    best_model = grid_search.best_estimator_
    print(f"Best Parameters: {grid_search.best_params_}")
    
    # Evaluate best model
    predictions = best_model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)
    
    print(f"Optimized Model RMSE: {rmse:.4f}")
    print(f"Optimized Model R2: {r2:.4f}")
    
    # Save best model
    joblib.dump(best_model, 'model.pkl')
    print("Saved best model to model.pkl")
    
    # Generate Evaluation Report Markdown
    report_content = f"""# Intern Performance Model Evaluation Report

## Executive Summary
This report summarizes the performance of our final optimized Intern Performance Prediction Model.

## Feature Engineering
We applied `StandardScaler` to ensure all features are on the same distribution scale before model training. The resulting scaler object is serialized and saved as `scaler.pkl` to scale data seamlessly in production.

## Model Optimization
We applied Gradient Boosting Regressor. Hyperparameter tuning was performed using 3-fold cross-validation via `GridSearchCV` searching over permutations of `n_estimators`, `learning_rate`, and `max_depth`.

### Optimal Parameters
{grid_search.best_params_}

## Final Model Evaluation on Hold-out Test Data (20% Split)
* **Root Mean Squared Error (RMSE):** {rmse:.4f}
* **R-Squared (R2) Score:** {r2:.4f}

These solid evaluation metrics indicate the model accurately identifies and explains roughly {r2*100:.2f}% of the variance within the mock intern dataset.
"""
    with open('evaluation_report.md', 'w') as f:
        f.write(report_content)
    print("Saved evaluation report to evaluation_report.md")

if __name__ == '__main__':
    optimize_and_evaluate()
