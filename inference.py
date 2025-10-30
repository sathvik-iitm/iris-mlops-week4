
"""
IRIS Classifier Inference Script
Week 4 - MLOps Assignment
"""

import pandas as pd
import joblib
import os

def load_model(model_path='models/iris_model.joblib'):
    """Load trained model"""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")
    return joblib.load(model_path)

def predict(model, features):
    """Make predictions on new data"""
    if isinstance(features, dict):
        features = pd.DataFrame([features])
    elif isinstance(features, list):
        features = pd.DataFrame(features)
    
    predictions = model.predict(features)
    return predictions

def predict_single(sepal_length, sepal_width, petal_length, petal_width, 
                   model_path='models/iris_model.joblib'):
    """Predict species for a single iris sample"""
    model = load_model(model_path)
    features = pd.DataFrame({
        'sepal_length': [sepal_length],
        'sepal_width': [sepal_width],
        'petal_length': [petal_length],
        'petal_width': [petal_width]
    })
    prediction = model.predict(features)[0]
    return prediction

def main():
    """Example inference"""
    print("Loading model...")
    model = load_model()
    
    # Example predictions
    test_samples = [
        {'sepal_length': 5.1, 'sepal_width': 3.5, 'petal_length': 1.4, 'petal_width': 0.2},
        {'sepal_length': 6.7, 'sepal_width': 3.1, 'petal_length': 4.4, 'petal_width': 1.4},
        {'sepal_length': 6.3, 'sepal_width': 3.3, 'petal_length': 6.0, 'petal_width': 2.5},
    ]
    
    print("Making predictions...")
    for i, sample in enumerate(test_samples, 1):
        pred = predict(model, sample)
        print(f"Sample {i}: {pred[0]}")

if __name__ == "__main__":
    main()
