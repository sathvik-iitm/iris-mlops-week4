# IRIS Classifier - MLOps Week 4

## 🎯 Project Overview
This project demonstrates MLOps best practices including:
- ✅ Git version control with branching strategy (dev → main)
- ✅ Automated unit testing with pytest (10 tests)
- ✅ CI/CD with GitHub Actions (separate workflows for dev and main)
- ✅ Code quality and validation
- ✅ Pull Request workflow with automated checks

## 📊 Dataset
IRIS dataset (150 samples) with 4 features:
- sepal_length, sepal_width, petal_length, petal_width
- Target: species (setosa, versicolor, virginica)
- Training: 105 samples, Test: 45 samples
- Model Accuracy: 100%

## 🚀 Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Train Model
```bash
python train.py
```

### Run Inference
```bash
python inference.py
```

### Run Tests
```bash
pytest tests/ -v
```

## 📁 Project Structure
```
.
├── .github/workflows/
│   ├── dev-ci.yml         # CI for dev branch
│   └── main-ci.yml        # CI for main branch
├── data/
│   └── data.csv           # IRIS dataset (150 rows)
├── models/
│   └── iris_model.joblib  # Trained model
├── tests/
│   ├── test_train.py      # Training tests
│   └── test_inference.py  # Inference tests
├── train.py               # Training pipeline
├── inference.py           # Inference script
├── requirements.txt       # Dependencies
└── README.md             # This file
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

## 📈 Results
- **Training Accuracy**: 100%
- **Test Coverage**: 10 unit tests
- **CI Status**: ✅ All checks passing
