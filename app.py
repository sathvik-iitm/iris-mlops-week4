
"""
IRIS Classifier API
Week 6 - Docker & Kubernetes Deployment
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from typing import List
import os

# Initialize FastAPI app
app = FastAPI(
    title="IRIS Classifier API",
    description="Predict iris species using trained ML model",
    version="1.0.0"
)

# Load model
MODEL_PATH = os.getenv("MODEL_PATH", "models/iris_model.joblib")

try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ Model loaded from {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# Request model
class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        }

class BatchIrisFeatures(BaseModel):
    samples: List[IrisFeatures]

# Response model
class PredictionResponse(BaseModel):
    species: str
    confidence: float

class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]

# Health check endpoint
@app.get("/")
def root():
    return {
        "message": "IRIS Classifier API",
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.get("/health")
def health():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy"}

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
def predict(features: IrisFeatures):
    """
    Predict iris species from flower measurements
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Prepare features
        X = np.array([[
            features.sepal_length,
            features.sepal_width,
            features.petal_length,
            features.petal_width
        ]])
        
        # Make prediction
        prediction = model.predict(X)[0]
        
        # Get probability (confidence)
        probabilities = model.predict_proba(X)[0]
        confidence = float(max(probabilities))
        
        return PredictionResponse(
            species=prediction,
            confidence=confidence
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Batch prediction endpoint
@app.post("/predict/batch", response_model=BatchPredictionResponse)
def predict_batch(features: BatchIrisFeatures):
    """
    Predict multiple iris samples at once
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        predictions = []
        
        for sample in features.samples:
            X = np.array([[
                sample.sepal_length,
                sample.sepal_width,
                sample.petal_length,
                sample.petal_width
            ]])
            
            prediction = model.predict(X)[0]
            probabilities = model.predict_proba(X)[0]
            confidence = float(max(probabilities))
            
            predictions.append(
                PredictionResponse(
                    species=prediction,
                    confidence=confidence
                )
            )
        
        return BatchPredictionResponse(predictions=predictions)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Model info endpoint
@app.get("/model/info")
def model_info():
    """
    Get information about the loaded model
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": type(model).__name__,
        "n_features": model.n_features_in_,
        "classes": model.classes_.tolist()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
