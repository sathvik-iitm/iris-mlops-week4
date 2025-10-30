# IRIS Classifier - MLOps Weeks 4 & 5

## 🎯 Project Overview
This project demonstrates advanced MLOps practices including:
- ✅ **Week 4**: Git version control, CI/CD with GitHub Actions, automated testing
- ✅ **Week 5**: MLflow experiment tracking, hyperparameter tuning, model registry

## 📊 Dataset
IRIS dataset (150 samples) with 4 features:
- sepal_length, sepal_width, petal_length, petal_width
- Target: species (setosa, versicolor, virginica)
- Training: 105 samples, Test: 45 samples

## 🆕 Week 5: MLflow Integration

### Experiment Tracking
- **6 experiments** with different hyperparameters
- Automated parameter and metric logging
- Model versioning in MLflow Registry
- Best model selection based on metrics

### Hyperparameters Tested
```
Experiment 1: max_depth=3, min_samples_split=2, min_samples_leaf=1
Experiment 2: max_depth=5, min_samples_split=2, min_samples_leaf=1
Experiment 3: max_depth=7, min_samples_split=2, min_samples_leaf=1
Experiment 4: max_depth=3, min_samples_split=5, min_samples_leaf=2
Experiment 5: max_depth=5, min_samples_split=5, min_samples_leaf=2
Experiment 6: max_depth=10, min_samples_split=10, min_samples_leaf=4
```

### Model Registry
- **6 model versions** registered
- Models accessible via MLflow UI and API
- Automatic version tracking

## 🚀 Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Week 4: Standard Training
```bash
python train.py
python inference.py
```

### Week 5: MLflow Training
```bash
# Run experiments with hyperparameter tuning
python train_mlflow.py

# View MLflow UI
mlflow ui

# Run inference with MLflow models
python inference_mlflow.py
```

### Run Tests
```bash
pytest tests/ -v
```

## 📁 Project Structure
```
.
├── .github/workflows/
│   ├── dev-ci.yml              # CI for dev branch
│   └── main-ci.yml             # CI for main branch
├── data/
│   └── data.csv                # IRIS dataset (150 rows)
├── models/
│   └── iris_model.joblib       # Trained model (Week 4)
├── mlruns/                     # MLflow tracking (Week 5)
├── tests/
│   ├── test_train.py           # Training tests
│   └── test_inference.py       # Inference tests
├── train.py                    # Standard training (Week 4)
├── train_mlflow.py             # MLflow training (Week 5) ⭐
├── inference.py                # Standard inference (Week 4)
├── inference_mlflow.py         # MLflow inference (Week 5) ⭐
├── requirements.txt            # Dependencies (includes MLflow)
└── README.md                   # This file
```

## 🧪 Testing
Unit tests cover:
- ✅ Data loading and validation
- ✅ Feature preparation
- ✅ Model training
- ✅ Model evaluation
- ✅ Inference functionality
- ✅ Prediction validation

## 🔄 CI/CD Workflow
1. **Dev Branch**: All development work happens here
2. **Pull Request**: Create PR from dev to main
3. **Automated Tests**: GitHub Actions runs all tests
4. **Code Review**: Review changes before merging
5. **Merge to Main**: Production-ready code

## 📊 Week 5: MLflow Features

### Experiment Tracking
- Automatic parameter logging
- Metric tracking (accuracy, precision, recall, F1)
- Model artifact storage
- Run comparison in MLflow UI

### Model Registry
- Centralized model storage
- Version management
- Model staging (Production, Staging, Archived)
- Easy model deployment

### Hyperparameter Tuning
- Grid search over multiple parameters
- Automated experiment logging
- Best model selection
- Reproducible results

## 📈 Results

### Week 4 Results
- **Training Accuracy**: 95.2%
- **Test Accuracy**: 100%
- **CI/CD**: ✅ All checks passing

### Week 5 Results
- **Experiments Run**: 6
- **Best Model**: max_depth=10, test_accuracy=1.000
- **Model Versions**: 6 (all in registry)
- **All Metrics**: Logged in MLflow

## 🎯 MLflow Usage

### View Experiments
```bash
# Start MLflow UI
mlflow ui

# Access at: http://localhost:5000
```

### Load Best Model
```python
import mlflow

# From registry
model = mlflow.sklearn.load_model("models:/iris_decision_tree/latest")

# From specific run
model = mlflow.sklearn.load_model("runs:/<run_id>/model")
```

## 🔗 Important Links

- **Repository**: https://github.com/sathvik-iitm/iris-mlops-week4
- **GitHub Actions**: https://github.com/sathvik-iitm/iris-mlops-week4/actions
- **Pull Requests**: https://github.com/sathvik-iitm/iris-mlops-week4/pulls

## 📝 Week-by-Week Progress

### Week 4 ✅
- Git repository setup
- Unit testing with pytest
- GitHub Actions CI/CD
- Branch protection
- Pull Request workflow

### Week 5 ✅
- MLflow integration
- Experiment tracking
- Hyperparameter tuning
- Model registry
- MLflow-based inference
- Removed DVC dependency

## ✨ Key Takeaways

**Week 4**: Version control, automated testing, and CI/CD are essential for collaborative ML development

**Week 5**: Experiment tracking and model registry solve reproducibility and model management challenges in MLOps

---

*MLOps Assignment - Weeks 4 & 5*  
*Repository: iris-mlops-week4*  
*Student: sathvik-iitm*
