
"""
Unit tests for IRIS inference
"""

import pytest
import pandas as pd
import joblib
from inference import load_model, predict, predict_single
from train import train_model
import os

@pytest.fixture
def sample_model():
    """Create a sample model for testing"""
    X_train = pd.DataFrame({
        'sepal_length': [5.1, 4.9, 6.7, 6.3],
        'sepal_width': [3.5, 3.0, 3.1, 3.3],
        'petal_length': [1.4, 1.4, 4.4, 6.0],
        'petal_width': [0.2, 0.2, 1.4, 2.5]
    })
    y_train = pd.Series(['setosa', 'setosa', 'versicolor', 'virginica'])
    
    model = train_model(X_train, y_train)
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/iris_model.joblib')
    
    return model

def test_load_model(sample_model):
    """Test model loading"""
    model = load_model('models/iris_model.joblib')
    assert model is not None
    assert hasattr(model, 'predict')

def test_predict_with_dict(sample_model):
    """Test prediction with dictionary input"""
    features = {
        'sepal_length': 5.1,
        'sepal_width': 3.5,
        'petal_length': 1.4,
        'petal_width': 0.2
    }
    
    predictions = predict(sample_model, features)
    assert len(predictions) == 1
    assert predictions[0] in ['setosa', 'versicolor', 'virginica']

def test_predict_with_dataframe(sample_model):
    """Test prediction with DataFrame input"""
    features = pd.DataFrame({
        'sepal_length': [5.1, 6.7],
        'sepal_width': [3.5, 3.1],
        'petal_length': [1.4, 4.4],
        'petal_width': [0.2, 1.4]
    })
    
    predictions = predict(sample_model, features)
    assert len(predictions) == 2
    assert all(p in ['setosa', 'versicolor', 'virginica'] for p in predictions)

def test_predict_single(sample_model):
    """Test single prediction function"""
    prediction = predict_single(5.1, 3.5, 1.4, 0.2)
    assert prediction in ['setosa', 'versicolor', 'virginica']

def test_predictions_are_valid_species(sample_model):
    """Test that all predictions are valid species"""
    test_samples = [
        {'sepal_length': 5.1, 'sepal_width': 3.5, 'petal_length': 1.4, 'petal_width': 0.2},
        {'sepal_length': 6.7, 'sepal_width': 3.1, 'petal_length': 4.4, 'petal_width': 1.4},
        {'sepal_length': 6.3, 'sepal_width': 3.3, 'petal_length': 6.0, 'petal_width': 2.5},
    ]
    
    valid_species = ['setosa', 'versicolor', 'virginica']
    
    for sample in test_samples:
        prediction = predict(sample_model, sample)[0]
        assert prediction in valid_species
