"""
Week 8: MLflow Training with Data Poisoning
Train models on clean and poisoned data, track everything
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import mlflow
import mlflow.sklearn
import joblib
import os

def train_model_with_poisoning(data_path: str, poison_level: str, experiment_name: str = "iris_data_poisoning"):
    """
    Train model on potentially poisoned data and log to MLflow
    
    Args:
        data_path: Path to dataset CSV
        poison_level: Description of poisoning (e.g., "clean", "5%", "10%", "50%")
        experiment_name: MLflow experiment name
    """
    # Set MLflow experiment
    mlflow.set_experiment(experiment_name)
    
    # Load data
    data = pd.read_csv(data_path)
    print(f"\n{'='*70}")
    print(f"📊 Training on: {poison_level} poisoned data")
    print(f"   Data: {data_path}")
    print(f"   Samples: {len(data)}")
    print(f"{'='*70}\n")
    
    # Prepare features and target
    X = data[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']]
    y = data['species']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    # Start MLflow run
    with mlflow.start_run(run_name=f"poison_{poison_level}"):
        # Log parameters
        mlflow.log_param("poison_level", poison_level)
        mlflow.log_param("data_path", data_path)
        mlflow.log_param("n_samples", len(data))
        mlflow.log_param("n_train", len(X_train))
        mlflow.log_param("n_test", len(X_test))
        mlflow.log_param("model_type", "DecisionTreeClassifier")
        mlflow.log_param("max_depth", 10)
        mlflow.log_param("random_state", 42)
        
        # Log data statistics
        for col in X.columns:
            mlflow.log_metric(f"data_mean_{col}", X[col].mean())
            mlflow.log_metric(f"data_std_{col}", X[col].std())
        
        # Train model
        print("🔨 Training model...")
        model = DecisionTreeClassifier(max_depth=10, random_state=42)
        model.fit(X_train, y_train)
        
        # Predictions
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        
        # Calculate metrics
        train_acc = accuracy_score(y_train, y_train_pred)
        test_acc = accuracy_score(y_test, y_test_pred)
        test_f1 = f1_score(y_test, y_test_pred, average='weighted')
        test_precision = precision_score(y_test, y_test_pred, average='weighted')
        test_recall = recall_score(y_test, y_test_pred, average='weighted')
        
        # Log metrics
        mlflow.log_metric("train_accuracy", train_acc)
        mlflow.log_metric("test_accuracy", test_acc)
        mlflow.log_metric("test_f1_score", test_f1)
        mlflow.log_metric("test_precision", test_precision)
        mlflow.log_metric("test_recall", test_recall)
        
        # Calculate overfitting indicator
        overfit_gap = train_acc - test_acc
        mlflow.log_metric("overfit_gap", overfit_gap)
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        # Save model locally
        model_dir = f"models/poisoned"
        os.makedirs(model_dir, exist_ok=True)
        model_path = f"{model_dir}/model_poison_{poison_level.replace('%', 'pct')}.joblib"
        joblib.dump(model, model_path)
        mlflow.log_artifact(model_path)
        
        print(f"\n📊 Results for {poison_level} poisoning:")
        print(f"   Train Accuracy: {train_acc:.4f}")
        print(f"   Test Accuracy:  {test_acc:.4f}")
        print(f"   Test F1 Score:  {test_f1:.4f}")
        print(f"   Overfit Gap:    {overfit_gap:.4f}")
        print(f"   Model saved:    {model_path}")
        
        return {
            'poison_level': poison_level,
            'train_acc': train_acc,
            'test_acc': test_acc,
            'test_f1': test_f1,
            'overfit_gap': overfit_gap
        }


def run_all_experiments():
    """Run complete data poisoning experiment"""
    print("="*70)
    print("🛡️ WEEK 8: DATA POISONING EXPERIMENTS")
    print("="*70)
    
    # Dataset configurations
    datasets = [
        ("data/raw/iris.csv", "clean"),
        ("data/poisoned/iris_poisoned_5pct.csv", "5%"),
        ("data/poisoned/iris_poisoned_10pct.csv", "10%"),
        ("data/poisoned/iris_poisoned_50pct.csv", "50%")
    ]
    
    results = []
    
    # Train on each dataset
    for data_path, poison_level in datasets:
        result = train_model_with_poisoning(data_path, poison_level)
        results.append(result)
    
    # Print comparison table
    print("\n" + "="*70)
    print("📊 RESULTS COMPARISON")
    print("="*70)
    print(f"{'Poison Level':<15} {'Train Acc':<12} {'Test Acc':<12} {'F1 Score':<12} {'Overfit Gap':<12}")
    print("-"*70)
    
    for r in results:
        print(f"{r['poison_level']:<15} {r['train_acc']:<12.4f} {r['test_acc']:<12.4f} "
              f"{r['test_f1']:<12.4f} {r['overfit_gap']:<12.4f}")
    
    print("="*70)
    print("\n✅ All experiments complete!")
    print("📁 Check MLflow UI: mlflow ui --port 5000")
    
    return results


if __name__ == "__main__":
    results = run_all_experiments()
