import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def train_initial_models():
    # 1. Load data
    try:
        df = pd.read_csv('clean_intern_data.csv')
    except FileNotFoundError:
        print("Error: clean_intern_data.csv. Run preprocessing first.")
        return

    # Features and Target
    X = df[['task_completion_rate', 'consistency_score', 'engagement_metric']]
    y = df['performance_score']

    # 2. Split data: 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Data Split - Training set: {X_train.shape[0]} samples, Test set: {X_test.shape[0]} samples")

    # 3. Initialize models to compare (We will compare 3 algorithms)
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest Regressor': RandomForestRegressor(random_state=42),
        'Gradient Boosting Regressor': GradientBoostingRegressor(random_state=42)
    }

    results = []

    # 4. Train and Evaluate Each Model
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        
        # Predictions
        predictions = model.predict(X_test)
        
        # Evaluation Metrics
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, predictions)
        
        print(f"Metrics -> RMSE: {rmse:.4f} | R2 Score: {r2:.4f}")
        
        results.append({
            'Model': name,
            'RMSE': rmse,
            'R2 Score': r2
        })

    # Save initial comparison results
    results_df = pd.DataFrame(results)
    print("\n--- Initial Model Comparison ---")
    print(results_df)
    results_df.to_csv('initial_model_results.csv', index=False)
    print("\nInitial results saved to initial_model_results.csv")

if __name__ == '__main__':
    train_initial_models()
