# Intern Performance Model Evaluation Report

## Executive Summary
This report summarizes the performance of our final optimized Intern Performance Prediction Model.

## Feature Engineering
We applied `StandardScaler` to ensure all features are on the same distribution scale before model training. The resulting scaler object is serialized and saved as `scaler.pkl` to scale data seamlessly in production.

## Model Optimization
We applied Gradient Boosting Regressor. Hyperparameter tuning was performed using 3-fold cross-validation via `GridSearchCV` searching over permutations of `n_estimators`, `learning_rate`, and `max_depth`.

### Optimal Parameters
{'learning_rate': 0.1, 'max_depth': 3, 'n_estimators': 100}

## Final Model Evaluation on Hold-out Test Data (20% Split)
* **Root Mean Squared Error (RMSE):** 5.6930
* **R-Squared (R2) Score:** 0.9232

These solid evaluation metrics indicate the model accurately identifies and explains roughly 92.32% of the variance within the mock intern dataset.
