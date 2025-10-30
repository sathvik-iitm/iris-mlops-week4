# IRIS Classifier - MLOps Week 4

## 🎯 Project Overview
This project demonstrates MLOps best practices including:
- ✅ Git version control with branching strategy
- ✅ Automated unit testing with pytest
- ✅ CI/CD with GitHub Actions
- ✅ Code quality and validation

## 📊 Dataset
IRIS dataset with 4 features:
- sepal_length, sepal_width, petal_length, petal_width
- Target: species (setosa, versicolor, virginica)

## 🚀 Usage

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
├── data/
│   └── data.csv           # IRIS dataset
├── models/
│   └── iris_model.joblib  # Trained model
├── tests/
│   ├── test_train.py      # Training tests
│   └── test_inference.py  # Inference tests
├── train.py               # Training pipeline
├── inference.py           # Inference script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🧪 Testing
Unit tests cover:
- Data loading and validation
- Feature preparation
- Model training
- Model evaluation
- Inference functionality

## 🔄 CI/CD
GitHub Actions automatically:
- Runs all tests on push/PR
- Reports test results as comments
- Validates code quality
