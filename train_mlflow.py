
"""
IRIS Classifier Training with MLflow Integration
Week 5 - MLOps Assignment
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
import mlflow
import mlflow.sklearn
import os
from datetime import datetime

# Set MLflow tracking URI (local for now)
mlflow.set_tracking_uri("file:./mlruns")

def load_data(data_path='data/data.csv'):
    """Load IRIS dataset"""
    data = pd.read_csv(data_path)
    return data

def prepare_features(data):
    """Prepare features and labels"""
    X = data[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
    y = data['species']
    return X, y

def train_model_with_mlflow(X_train, y_train, X_test, y_test, 
                            max_depth=3, min_samples_split=2, 
                            min_samples_leaf=1, random_state=42):
    """Train Decision Tree with MLflow logging"""
    
    # Start MLflow run
    with mlflow.start_run(run_name=f"dt_depth{max_depth}"):
        
        # Log parameters
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("min_samples_split", min_samples_split)
        mlflow.log_param("min_samples_leaf", min_samples_leaf)
        mlflow.log_param("random_state", random_state)
        mlflow.log_param("model_type", "DecisionTree")
        mlflow.log_param("train_samples", len(X_train))
        mlflow.log_param("test_samples", len(X_test))
        
        # Train model
        model = DecisionTreeClassifier(
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=random_state
        )
        model.fit(X_train, y_train)
        
        # Evaluate on training set
        train_predictions = model.predict(X_train)
        train_accuracy = metrics.accuracy_score(y_train, train_predictions)
        
        # Evaluate on test set
        test_predictions = model.predict(X_test)
        test_accuracy = metrics.accuracy_score(y_test, test_predictions)
        test_precision = metrics.precision_score(y_test, test_predictions, average='weighted')
        test_recall = metrics.recall_score(y_test, test_predictions, average='weighted')
        test_f1 = metrics.f1_score(y_test, test_predictions, average='weighted')
        
        # Log metrics
        mlflow.log_metric("train_accuracy", train_accuracy)
        mlflow.log_metric("test_accuracy", test_accuracy)
        mlflow.log_metric("test_precision", test_precision)
        mlflow.log_metric("test_recall", test_recall)
        mlflow.log_metric("test_f1_score", test_f1)
        
        # Log model
        mlflow.sklearn.log_model(
            model, 
            "model",
            registered_model_name="iris_decision_tree"
        )
        
        # Log feature names
        mlflow.log_param("features", ",".join(X_train.columns.tolist()))
        
        print(f"✅ Run logged - Test Accuracy: {test_accuracy:.3f}")
        
        return model, test_accuracy

def hyperparameter_tuning_with_mlflow(X_train, y_train, X_test, y_test):
    """Run multiple experiments with different hyperparameters"""
    
    # Set experiment name
    mlflow.set_experiment("iris_hyperparameter_tuning")
    
    print("🔬 Starting hyperparameter tuning experiments...")
    print("="*60)
    
    # Define hyperparameter combinations to try
    param_combinations = [
        {"max_depth": 3, "min_samples_split": 2, "min_samples_leaf": 1},
        {"max_depth": 5, "min_samples_split": 2, "min_samples_leaf": 1},
        {"max_depth": 7, "min_samples_split": 2, "min_samples_leaf": 1},
        {"max_depth": 3, "min_samples_split": 5, "min_samples_leaf": 2},
        {"max_depth": 5, "min_samples_split": 5, "min_samples_leaf": 2},
        {"max_depth": 10, "min_samples_split": 10, "min_samples_leaf": 4},
    ]
    
    results = []
    
    for i, params in enumerate(param_combinations, 1):
        print(f"\n🧪 Experiment {i}/{len(param_combinations)}")
        print(f"   Parameters: {params}")
        
        model, accuracy = train_model_with_mlflow(
            X_train, y_train, X_test, y_test,
            max_depth=params["max_depth"],
            min_samples_split=params["min_samples_split"],
            min_samples_leaf=params["min_samples_leaf"]
        )
        
        results.append({
            "params": params,
            "accuracy": accuracy
        })
    
    print("\n" + "="*60)
    print("🎯 All experiments completed!")
    
    # Find best parameters
    best_result = max(results, key=lambda x: x["accuracy"])
    print(f"\n🏆 Best Parameters: {best_result['params']}")
    print(f"🏆 Best Accuracy: {best_result['accuracy']:.3f}")
    
    return results

def main():
    """Main training pipeline with MLflow"""
    print("🚀 IRIS Classifier Training with MLflow")
    print("="*60)
    
    print("\n📊 Loading data...")
    data = load_data()
    
    print("🔧 Preparing features...")
    X, y = prepare_features(data)
    
    print("✂️ Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    
    print(f"   Training samples: {len(X_train)}")
    print(f"   Test samples: {len(X_test)}")
    
    # Run hyperparameter tuning experiments
    results = hyperparameter_tuning_with_mlflow(X_train, y_train, X_test, y_test)
    
    print("\n✅ Training complete! Check MLflow UI for results.")
    print("\n💡 To view experiments, run: mlflow ui")
    
    return results

if __name__ == "__main__":
    results = main()
