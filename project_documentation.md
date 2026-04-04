# Project Documentation: Intern Performance Prediction & Analytics System

## 1. Project Overview
**Title:** Intern Performance Prediction & Analytics System  
**Objective:** Build a machine learning model to predict an intern's overall performance score based on three input metrics: Task Completion, Consistency, and Engagement.

---

## 2. Sprint Structure & Achievements

### Sprint 1: Data Foundation
*   **Goal:** Create a reliable dataset for training without real-world data.
*   **Method:** Developed a synthetic data generator (`data_generator.py`) that uses `numpy` and `pandas` to create 1,000 realistic intern records.
*   **Outcome:** Pristine dataset stored in `clean_intern_data.csv`.

### Sprint 2: Model Development
*   **Goal:** Compare different Machine Learning algorithms.
*   **Method:** Trained three separate regression models in `model_training.py`:
    1.  **Linear Regression** (Baseline)
    2.  **Random Forest Regressor** (Ensemble)
    3.  **Gradient Boosting Regressor** (Boosting)
*   **Outcome:** Gradient Boosting Regressor performed the best with the highest R2 score and lowest RMSE.

### Sprint 3: Optimization & Evaluation
*   **Goal:** Maximize accuracy and prepare for production.
*   **Method:** 
    *   Applied `StandardScaler` to normalize feature scales.
    *   Used `GridSearchCV` for hyperparameter tuning.
*   **Outcome:** Finalized model saved as `model.pkl`. Detailed performance report in `evaluation_report.md`.

### Sprint 4: Model Deployment
*   **Goal:** Make predictions accessible via a web interface.
*   **Method:** Built a FastAPI-based web server (`app.py`) providing a `/predict_batch` endpoint.
*   **Outcome:** Fully functional API supporting Excel and CSV file uploads.

---

## 3. Data Logic & Feature Engineering

### Feature Definitions
1.  **Task Completion Rate (0.4 - 1.0):** Percentage of assigned tasks completed.
2.  **Consistency Score (0.3 - 1.0):** Stability of output over time.
3.  **Engagement Metric (0.2 - 1.0):** Proactiveness and soft skills.

### The Scoring Formula
We used a weighted formula to calculate the "True" target score in our simulation:
*   **Task Completion:** 40% importance
*   **Consistency:** 35% importance
*   **Engagement:** 25% importance

### Why `np.random.seed(42)`?
We fixed the random seed to `42` to ensure **reproducibility**. This means any time this project is run on any computer, the resulting data and model performance will be exactly the same, allowing for fair testing and debugging.

---

## 4. Model Evaluation Results
*   **Algorithm:** Gradient Boosting Regressor
*   **RMSE (Root Mean Square Error):** ~5.88
*   **R2 Score (Variance Explained):** ~0.81 (Meaning the model explains 81% of the performance variance)

---

## 5. File Structure
*   `data_generator.py`: Generates simulation data.
*   `data_preprocessing.py`: Cleans and prepares data.
*   `model_training.py`: Compares algorithms.
*   `model_optimization.py`: Tunes and saves the final model.
*   `app.py`: The FastAPI server.
*   `requirements.txt`: Python dependencies.
*   `README.md`: Quick start guide.

---

## 6. API Documentation
**Endpoint:** `POST /predict_batch`  
**Input:** Excel (`.xlsx`) or CSV (`.csv`) file.  
**Required Columns:** `task_completion_rate`, `consistency_score`, `engagement_metric`, `intern_id` (Optional).  
**Output:** JSON list containing `intern_id` and `predicted_performance`.
