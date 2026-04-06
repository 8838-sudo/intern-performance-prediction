from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import joblib
import numpy as np
import pandas as pd
import uvicorn
from io import BytesIO
import warnings
import os
import traceback
import mimetypes

# Ensure correct MIME types for static files
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')

warnings.filterwarnings('ignore')

# Calculate absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'scaler.pkl')

# Create static directory if it doesn't exist
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

app = FastAPI(
    title="Intern Performance Prediction API",
    description="API to predict an intern's performance score via batch Excel/CSV uploads.",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Load model and scaler
try:
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        raise FileNotFoundError(f"Model or Scaler file not found at: {MODEL_PATH} or {SCALER_PATH}")
        
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("Model and Scaler loaded successfully.")
except Exception as e:
    print(f"Error loading model or scaler: {e}")
    traceback.print_exc()
    model = None
    scaler = None

@app.post("/predict_batch")
async def predict_batch(file: UploadFile = File(...)):
    """
    Upload an Excel (.xlsx/.xls) or CSV file.
    The file must contain the following columns:
    - intern_id
    - task_completion_rate
    - consistency_score
    - engagement_metric
    """
    if model is None or scaler is None:
        raise HTTPException(status_code=500, detail="Model or Scaler not loaded.")
        
    filename = file.filename.lower()
    if not (filename.endswith('.csv') or filename.endswith('.xlsx') or filename.endswith('.xls')):
        raise HTTPException(status_code=400, detail="Please upload a .csv or .xlsx file")

    try:
        contents = await file.read()
        if filename.endswith('.csv'):
            df = pd.read_csv(BytesIO(contents))
        else:
            df = pd.read_excel(BytesIO(contents))
            
        # Ensure required columns exist
        required_cols = ['intern_id', 'task_completion_rate', 'consistency_score', 'engagement_metric']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        # Auto-generate 'intern_id' if only that is missing
        if 'intern_id' in missing_cols:
            if len(missing_cols) == 1:
                df['intern_id'] = [f"INT-{str(i+1).zfill(3)}" for i in range(len(df))]
                missing_cols.remove('intern_id')

        # If still missing other columns, raise error
        if missing_cols:
            raise HTTPException(status_code=400, detail=f"File is missing required columns: {missing_cols}")

        # Extract numerical features for the model
        features = df[['task_completion_rate', 'consistency_score', 'engagement_metric']]
        
        # Scale and Predict
        features_scaled = scaler.transform(features)
        predictions = model.predict(features_scaled)
        predictions_clipped = np.clip(predictions, 0.0, 100.0)
        
        # Build results combining Intern ID and Predicted Score
        results = []
        for intern_id, pred in zip(df['intern_id'], predictions_clipped):
            results.append({
                "intern_id": str(intern_id),
                "predicted_performance": round(pred, 2)
            })
            
        return JSONResponse(content=results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/")
def serve_ui():
    index_path = os.path.join(STATIC_DIR, 'index.html')
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "healthy", "message": "Intern Performance Prediction API is running. Dashboard not found."}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
