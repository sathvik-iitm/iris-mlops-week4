
"""
IRIS Classifier Training Pipeline
Week 4 - MLOps Assignment
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
import joblib
import os

def load_data(data_path='data/data.csv'):
    """Load IRIS dataset"""
    data = pd.read_csv(data_path)
    return data

def prepare_features(data):
    """Prepare features and labels"""
    X = data[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
    y = data['species']
    return X, y

def train_model(X_train, y_train, max_depth=3, random_state=42):
    """Train Decision Tree classifier"""
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    predictions = model.predict(X_test)
    accuracy = metrics.accuracy_score(y_test, predictions)
    return accuracy, predictions

def save_model(model, model_path='models/iris_model.joblib'):
    """Save trained model"""
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

def main():
    """Main training pipeline"""
    print("Loading data...")
    data = load_data()
    
    print("Preparing features...")
    X, y = prepare_features(data)
    
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    print("Training model...")
    model = train_model(X_train, y_train)
    
    print("Evaluating model...")
    accuracy, predictions = evaluate_model(model, X_test, y_test)
    print(f"Model Accuracy: {accuracy:.3f}")
    
    print("Saving model...")
    save_model(model)
    
    return model, accuracy

if __name__ == "__main__":
    model, accuracy = main()
