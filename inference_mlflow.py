
"""
IRIS Classifier Inference with MLflow Integration
Week 5 - MLOps Assignment
Fetches best model from MLflow Model Registry
"""

import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np

# Set MLflow tracking URI
mlflow.set_tracking_uri("file:./mlruns")

def load_model_from_registry(model_name="iris_decision_tree", stage="latest"):
    """
    Load model from MLflow Model Registry
    
    Args:
        model_name: Name of the registered model
        stage: Model stage ("latest", "Production", "Staging", etc.)
    
    Returns:
        Loaded model
    """
    print(f"📦 Loading model from MLflow Registry...")
    print(f"   Model: {model_name}")
    print(f"   Stage: {stage}")
    
    if stage == "latest":
        # Get the latest version
        client = mlflow.MlflowClient()
        model_versions = client.search_model_versions(f"name='{model_name}'")
        
        if not model_versions:
            raise ValueError(f"No versions found for model '{model_name}'")
        
        # Get the latest version number
        latest_version = max([int(mv.version) for mv in model_versions])
        model_uri = f"models:/{model_name}/{latest_version}"
        print(f"   Version: {latest_version}")
    else:
        model_uri = f"models:/{model_name}/{stage}"
    
    model = mlflow.sklearn.load_model(model_uri)
    print(f"✅ Model loaded successfully!")
    
    return model

def get_best_model_from_experiments(experiment_name="iris_hyperparameter_tuning"):
    """
    Find and load the best model from MLflow experiments based on test_accuracy
    
    Returns:
        Best model and its metrics
    """
    print(f"🔍 Searching for best model in experiment: {experiment_name}")
    
    client = mlflow.MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)
    
    if not experiment:
        raise ValueError(f"Experiment '{experiment_name}' not found")
    
    # Search runs, ordered by test_accuracy descending
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.test_accuracy DESC"],
        max_results=1
    )
    
    if not runs:
        raise ValueError("No runs found in experiment")
    
    best_run = runs[0]
    
    print(f"\n🏆 Best Model Found:")
    print(f"   Run ID: {best_run.info.run_id}")
    print(f"   Test Accuracy: {best_run.data.metrics.get('test_accuracy', 0):.4f}")
    print(f"   Parameters:")
    for param, value in best_run.data.params.items():
        if param in ['max_depth', 'min_samples_split', 'min_samples_leaf']:
            print(f"      {param}: {value}")
    
    # Load the model from this run
    model_uri = f"runs:/{best_run.info.run_id}/model"
    model = mlflow.sklearn.load_model(model_uri)
    
    print(f"\n✅ Best model loaded!")
    
    return model, best_run

def predict(model, input_data):
    """
    Make predictions using the loaded model
    
    Args:
        model: Loaded sklearn model
        input_data: Dict or DataFrame with features
    
    Returns:
        Predictions
    """
    # Convert dict to DataFrame if needed
    if isinstance(input_data, dict):
        if 'sepal_length' in input_data:
            # Single prediction
            df = pd.DataFrame([input_data])
        else:
            df = pd.DataFrame(input_data)
    else:
        df = input_data
    
    # Make predictions
    predictions = model.predict(df)
    
    return predictions

def main():
    """Main inference pipeline"""
    print("🔮 IRIS Classifier Inference with MLflow")
    print("="*60)
    
    # Method 1: Load from Model Registry (latest version)
    print("\n📋 Method 1: Load from Model Registry")
    print("-"*60)
    model_registry = load_model_from_registry("iris_decision_tree", "latest")
    
    # Method 2: Load best model from experiments
    print("\n📋 Method 2: Load Best Model from Experiments")
    print("-"*60)
    model_best, best_run = get_best_model_from_experiments()
    
    # Test predictions
    print("\n" + "="*60)
    print("🧪 Testing Predictions")
    print("="*60)
    
    # Sample data for each species
    test_samples = [
        {
            'sepal_length': 5.1,
            'sepal_width': 3.5,
            'petal_length': 1.4,
            'petal_width': 0.2,
            'expected': 'setosa'
        },
        {
            'sepal_length': 6.7,
            'sepal_width': 3.1,
            'petal_length': 4.4,
            'petal_width': 1.4,
            'expected': 'versicolor'
        },
        {
            'sepal_length': 6.3,
            'sepal_width': 3.3,
            'petal_length': 6.0,
            'petal_width': 2.5,
            'expected': 'virginica'
        }
    ]
    
    print("\nUsing Model from Registry:")
    for i, sample in enumerate(test_samples, 1):
        features = {k: v for k, v in sample.items() if k != 'expected'}
        prediction = predict(model_registry, features)[0]
        status = "✅" if prediction == sample['expected'] else "❌"
        print(f"  Sample {i}: {prediction} (expected: {sample['expected']}) {status}")
    
    print("\nUsing Best Model from Experiments:")
    for i, sample in enumerate(test_samples, 1):
        features = {k: v for k, v in sample.items() if k != 'expected'}
        prediction = predict(model_best, features)[0]
        status = "✅" if prediction == sample['expected'] else "❌"
        print(f"  Sample {i}: {prediction} (expected: {sample['expected']}) {status}")
    
    print("\n" + "="*60)
    print("✅ Inference Complete!")
    
    return model_registry, model_best

if __name__ == "__main__":
    model_registry, model_best = main()
