# Week 5 Assignment - Final Summary

## ✅ Assignment Completion Status: 100%

### 📦 Repository Information
- **GitHub URL**: https://github.com/sathvik-iitm/iris-mlops-week4
- **Week 5 Branch**: main (integrated with Week 4)
- **Total Commits (Week 5)**: 3
- **MLflow Status**: ✅ 6 experiments tracked, 6 models registered

---

## 🎯 Requirements Checklist

### ✅ Part A: MLflow Integration
- [x] Installed MLflow and dependencies
- [x] Set up MLflow tracking URI (local: ./mlruns)
- [x] Integrated MLflow into training pipeline
- [x] Logged experiments, parameters, and metrics
- [x] Created model registry

### ✅ Part B: Hyperparameter Tuning
- [x] Implemented 6 different hyperparameter combinations
- [x] Tested: max_depth (3, 5, 7, 10)
- [x] Tested: min_samples_split (2, 5, 10)
- [x] Tested: min_samples_leaf (1, 2, 4)
- [x] Logged all parameters to MLflow

### ✅ Part C: Experiment Tracking & Metrics
- [x] Logged training accuracy
- [x] Logged test accuracy
- [x] Logged precision, recall, F1-score
- [x] Logged model artifacts
- [x] Tracked 6 complete experiments

### ✅ Part D: Model Registry
- [x] Registered 6 model versions
- [x] Models accessible via MLflow API
- [x] Implemented model loading from registry
- [x] Created inference script using registry

### ✅ Part E: Remove DVC Dependency
- [x] Removed DVC references (wasn't implemented)
- [x] Using MLflow for model logging instead
- [x] All models stored in MLflow artifacts

### ✅ Part F: Fetch Best Model
- [x] Created function to find best model by metrics
- [x] Implemented model loading from experiments
- [x] Tested inference with best model
- [x] Validated predictions

### ✅ Part G (Optional): Update CI/CD
- [ ] CI still uses original train.py (Week 4 workflow)
- [ ] Can be enhanced to use train_mlflow.py
- Note: Core functionality complete, CI enhancement optional

---

## 📊 Technical Implementation

### MLflow Experiments Conducted

| Experiment | max_depth | min_samples_split | min_samples_leaf | Train Acc | Test Acc |
|------------|-----------|-------------------|------------------|-----------|----------|
| 1          | 3         | 2                 | 1                | 0.9524    | 1.0000   |
| 2          | 5         | 2                 | 1                | 0.9905    | 1.0000   |
| 3          | 7         | 2                 | 1                | 1.0000    | 1.0000   |
| 4          | 3         | 5                 | 2                | 0.9429    | 1.0000   |
| 5          | 5         | 5                 | 2                | 0.9714    | 1.0000   |
| 6          | 10        | 10                | 4                | 0.9429    | 1.0000   |

**Best Model**: max_depth=10, achieving 1.000 test accuracy

### Project Structure (Week 5 Additions)
```
iris-mlops-week4/
├── train_mlflow.py              # ⭐ NEW: MLflow training with hyperparameter tuning
├── inference_mlflow.py          # ⭐ NEW: MLflow-based inference
├── mlruns/                      # ⭐ NEW: MLflow tracking data (gitignored)
│   ├── 0/                       # Default experiment
│   ├── 823270064895723401/      # iris_hyperparameter_tuning
│   └── models/                  # Model registry
├── requirements.txt             # Updated with MLflow
├── README.md                    # Updated with Week 5 docs
└── [Week 4 files remain unchanged]
```

### MLflow Features Implemented

1. **Experiment Tracking**
   - Automatic parameter logging
   - Comprehensive metric tracking
   - Run comparison capabilities
   - Experiment organization

2. **Model Registry**
   - 6 model versions registered
   - Version management
   - Easy model retrieval
   - Model metadata storage

3. **Hyperparameter Tuning**
   - Grid search implementation
   - Multiple experiments
   - Automated logging
   - Best model identification

---

## 🔄 Week 5 Workflow

### Training Workflow
```bash
# Run MLflow experiments
python train_mlflow.py

# This will:
# 1. Load IRIS dataset (150 rows)
# 2. Split into train/test (105/45)
# 3. Run 6 experiments with different hyperparameters
# 4. Log all parameters and metrics to MLflow
# 5. Register all models in MLflow Registry
# 6. Identify and report best model
```

### Inference Workflow
```bash
# Run MLflow inference
python inference_mlflow.py

# This will:
# 1. Load latest model from registry
# 2. Load best model from experiments
# 3. Make predictions on test samples
# 4. Validate results
```

### MLflow UI
```bash
# Launch MLflow UI
mlflow ui

# Access at: http://localhost:5000
# View:
# - All experiments and runs
# - Parameter comparisons
# - Metric visualizations
# - Model artifacts
```

---

## 📈 Results & Metrics

### Model Performance
- **Best Test Accuracy**: 100%
- **Best Train Accuracy**: 100% (max_depth=7)
- **Best F1 Score**: 1.000
- **Best Precision**: 1.000
- **Best Recall**: 1.000

### MLflow Metrics
- **Total Experiments**: 1 (iris_hyperparameter_tuning)
- **Total Runs**: 6
- **Models Registered**: 6 versions
- **Parameters Tracked**: 8 per run
- **Metrics Tracked**: 5 per run

### Code Quality
- **Python Scripts**: 2 new MLflow-enabled scripts
- **Lines of Code**: ~400+ new lines
- **Documentation**: Comprehensive README update
- **Dependencies**: MLflow 3.5.1, GCS integration

---

## 🎓 Learning Outcomes

### Week 5 Skills Acquired

1. ✅ **MLflow Setup & Configuration**
   - Installing and configuring MLflow
   - Setting up tracking URI
   - Managing MLflow server

2. ✅ **Experiment Tracking**
   - Logging parameters automatically
   - Tracking metrics across runs
   - Organizing experiments
   - Comparing results

3. ✅ **Model Registry**
   - Registering models
   - Version management
   - Model lifecycle management
   - Programmatic model access

4. ✅ **Hyperparameter Tuning**
   - Grid search implementation
   - Parameter space exploration
   - Best model selection
   - Reproducible experiments

5. ✅ **MLOps Best Practices**
   - Experiment reproducibility
   - Model versioning
   - Automated tracking
   - Centralized model storage

---

## 🔗 Key Files Created/Modified

### New Files (Week 5)
1. **train_mlflow.py** - MLflow training with hyperparameter tuning
2. **inference_mlflow.py** - Model loading from MLflow registry
3. **WEEK5_SUMMARY.md** - This summary document

### Modified Files
1. **requirements.txt** - Added MLflow and GCS dependencies
2. **README.md** - Comprehensive Week 5 documentation
3. **.gitignore** - Added mlruns/ to ignore list
4. **data/data.csv** - Updated to full 150-row dataset

---

## 💡 Key Code Snippets

### Training with MLflow
```python
import mlflow
import mlflow.sklearn

with mlflow.start_run(run_name=f"dt_depth{max_depth}"):
    # Log parameters
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("min_samples_split", min_samples_split)
    
    # Train model
    model.fit(X_train, y_train)
    
    # Log metrics
    mlflow.log_metric("test_accuracy", accuracy)
    
    # Log model
    mlflow.sklearn.log_model(
        model, "model",
        registered_model_name="iris_decision_tree"
    )
```

### Loading from Registry
```python
# Load latest version
model = mlflow.sklearn.load_model(
    "models:/iris_decision_tree/latest"
)

# Make predictions
predictions = model.predict(X_test)
```

---

## 📝 Submission Checklist

- [x] GitHub repository updated with Week 5 code
- [x] MLflow integration complete
- [x] 6 experiments conducted and logged
- [x] Model registry populated with 6 versions
- [x] Inference script loads from MLflow
- [x] README documentation updated
- [x] All code tested and working
- [x] Requirements.txt updated
- [x] Week 5 summary document created

---

## 🎯 Assignment Objectives - Verification

✅ **Integrate MLflow into homework pipeline** - Complete
✅ **Introduce hyperparameter tuning** - Complete (6 experiments)
✅ **Log experiments, parameters, metrics** - Complete (all tracked)
✅ **Compare experiments using MLflow UI** - Complete (UI accessible)
✅ **Remove DVC dependency** - Complete (not applicable)
✅ **Modify evaluation to fetch from MLflow** - Complete
✅ **(Optional) Update CI for MLflow** - Pending (enhancement opportunity)

---

## ✨ Conclusion

Successfully integrated MLflow into the IRIS classification pipeline, implementing:
- Comprehensive experiment tracking
- Automated hyperparameter tuning
- Model registry with versioning
- MLflow-based model inference
- Professional documentation

**Week 5 Status**: ✅ COMPLETE  
**Ready for**: Submission and presentation

---

*Generated on: October 30, 2025*  
*Student: sathvik-iitm*  
*Course: MLOps - Week 5*  
*Assignment: MLflow Integration*
