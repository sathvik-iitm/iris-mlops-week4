
"""
Unit tests for IRIS training pipeline
"""

import pytest
import pandas as pd
import numpy as np
from train import load_data, prepare_features, train_model, evaluate_model
import os

def test_load_data():
    """Test data loading"""
    # Create sample data for testing
    sample_data = pd.DataFrame({
        'sepal_length': [5.1, 4.9, 6.7],
        'sepal_width': [3.5, 3.0, 3.1],
        'petal_length': [1.4, 1.4, 4.4],
        'petal_width': [0.2, 0.2, 1.4],
        'species': ['setosa', 'setosa', 'versicolor']
    })
    
    # Save test data
    os.makedirs('data', exist_ok=True)
    sample_data.to_csv('data/data.csv', index=False)
    
    # Test loading
    data = load_data('data/data.csv')
    assert isinstance(data, pd.DataFrame)
    assert len(data) > 0
    assert 'species' in data.columns

def test_prepare_features():
    """Test feature preparation"""
    data = pd.DataFrame({
        'sepal_length': [5.1, 4.9],
        'sepal_width': [3.5, 3.0],
        'petal_length': [1.4, 1.4],
        'petal_width': [0.2, 0.2],
        'species': ['setosa', 'setosa']
    })
    
    X, y = prepare_features(data)
    assert X.shape[0] == 2
    assert X.shape[1] == 4
    assert len(y) == 2

def test_train_model():
    """Test model training"""
    X_train = pd.DataFrame({
        'sepal_length': [5.1, 4.9, 6.7, 6.3],
        'sepal_width': [3.5, 3.0, 3.1, 3.3],
        'petal_length': [1.4, 1.4, 4.4, 6.0],
        'petal_width': [0.2, 0.2, 1.4, 2.5]
    })
    y_train = pd.Series(['setosa', 'setosa', 'versicolor', 'virginica'])
    
    model = train_model(X_train, y_train)
    assert model is not None
    assert hasattr(model, 'predict')

def test_evaluate_model():
    """Test model evaluation"""
    X_train = pd.DataFrame({
        'sepal_length': [5.1, 4.9, 6.7, 6.3],
        'sepal_width': [3.5, 3.0, 3.1, 3.3],
        'petal_length': [1.4, 1.4, 4.4, 6.0],
        'petal_width': [0.2, 0.2, 1.4, 2.5]
    })
    y_train = pd.Series(['setosa', 'setosa', 'versicolor', 'virginica'])
    
    model = train_model(X_train, y_train)
    accuracy, predictions = evaluate_model(model, X_train, y_train)
    
    assert 0 <= accuracy <= 1
    assert len(predictions) == len(y_train)

def test_model_accuracy_threshold():
    """Test that model meets minimum accuracy threshold"""
    # This test will use actual data when available
    # For now, just check the structure
    assert True  # Placeholder - will be replaced with actual test
