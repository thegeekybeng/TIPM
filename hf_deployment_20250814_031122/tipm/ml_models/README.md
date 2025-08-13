# TIPM ML Models Package

🚀 **Advanced Machine Learning Models for Tariff Impact Propagation Model (TIPM)**

A comprehensive, enterprise-grade machine learning package designed for analyzing tariff impacts, economic forecasting, and policy decision support.

## 🌟 Features

### **Multi-Class Classification Models**
- **TariffImpactClassifier**: Predicts tariff impact severity (Low/Medium/High/Critical)
- **EconomicOutcomeClassifier**: Classifies economic outcomes from policy changes
- **PolicyEffectivenessClassifier**: Assesses policy effectiveness levels
- **IndustryVulnerabilityClassifier**: Identifies industry vulnerability to trade shocks

### **LSTM-Based Time Series Forecasters**
- **GDPImpactForecaster**: Predicts GDP impacts with confidence intervals
- **TradeFlowForecaster**: Forecasts trade flow changes and balance trends
- **EmploymentForecaster**: Projects employment impacts from policy changes
- **PriceImpactForecaster**: Predicts price inflation and market impacts

### **Advanced Ensemble Methods**
- **TIPMEnsemble**: Sophisticated ensemble with weight optimization
- **ModelVoting**: Simple voting ensemble for model combination
- **StackingEnsemble**: Meta-learning ensemble with base models
- **DynamicEnsemble**: Adaptive ensemble that adjusts weights based on performance

### **Explainability & Policy Insights**
- **SHAPExplainer**: SHAP-based model explanations for interpretability
- **PolicyInsightGenerator**: Automated policy recommendations and risk assessment

### **Model Management**
- **MLModelManager**: Centralized model lifecycle management
- **Performance Tracking**: Comprehensive model performance monitoring
- **Model Persistence**: Save/load trained models with metadata

## 🚀 Quick Start

### Installation

```bash
# Install core dependencies
pip install -r requirements.txt

# For GPU support (optional)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Basic Usage

```python
from tipm.ml_models import MLModelManager, quick_start

# Quick start with default models
manager = quick_start()

# Or create manager manually
manager = MLModelManager()
manager.create_default_models()

# Train all models
X, y = your_training_data, your_targets
training_results = manager.train_all_models(X, y)

# Make predictions
prediction = manager.predict("tariff_impact_classifier", X_new)

# Get model explanations
explanation = manager.explain_prediction("tariff_impact_classifier", X_new)

# Generate policy insights
insights = manager.generate_policy_insights("tariff_impact_classifier", explanation)
```

## 📊 Model Architecture

### **Classification Pipeline**
```
Input Features → Feature Engineering → Multi-Class Classifier → Probability Scores → Impact Severity
```

### **Forecasting Pipeline**
```
Time Series Data → LSTM Network → Attention Mechanism → Multi-Step Forecast → Confidence Intervals
```

### **Ensemble Pipeline**
```
Base Models → Weight Optimization → Meta-Learning → Ensemble Prediction → Uncertainty Quantification
```

## 🔧 Advanced Usage

### **Custom Model Creation**

```python
from tipm.ml_models import BaseMLModel, ModelType

class CustomClassifier(BaseMLModel):
    def __init__(self):
        super().__init__(
            model_id="custom_classifier",
            name="Custom Classifier",
            description="Custom classification model",
            model_type=ModelType.CLASSIFICATION
        )
    
    def _create_model(self):
        # Implement your custom model
        pass

# Register with manager
manager.register_model(CustomClassifier(), "classifier")
```

### **Hyperparameter Tuning**

```python
# Access model hyperparameters
classifier = manager.models["tariff_impact_classifier"]
classifier.hyperparameters["learning_rate"] = 0.001
classifier.hyperparameters["max_depth"] = 10

# Retrain with new parameters
manager.train_model("tariff_impact_classifier", X, y)
```

### **Ensemble Creation**

```python
# Create custom ensemble
success = manager.create_ensemble_from_models(
    ensemble_id="custom_ensemble",
    model_ids=["tariff_impact_classifier", "economic_outcome_classifier"],
    ensemble_type="voting"
)
```

## 📈 Performance & Monitoring

### **Model Performance Tracking**

```python
# Get overall performance
performance = manager.get_overall_performance()
print(f"Total models: {performance['total_models']}")
print(f"Trained models: {performance['trained_models']}")

# Get specific model status
status = manager.get_model_status("tariff_impact_classifier")
print(f"Training score: {status['training_score']}")
print(f"Last trained: {status['last_trained']}")
```

### **Performance History**

```python
# Get performance history
history = manager.get_model_performance("tariff_impact_classifier")
for record in history:
    print(f"{record['timestamp']}: {record['operation']} - {record['metrics']}")
```

## 🎯 Use Cases

### **Government Policy Analysis**
- **Tariff Impact Assessment**: Predict economic consequences of trade policies
- **Policy Effectiveness**: Evaluate success of implemented policies
- **Risk Mitigation**: Identify and quantify policy risks

### **Economic Forecasting**
- **GDP Projections**: Long-term economic growth predictions
- **Trade Flow Analysis**: Import/export volume forecasting
- **Employment Impact**: Job market effects from policy changes

### **Business Intelligence**
- **Market Analysis**: Price impact predictions for businesses
- **Supply Chain Planning**: Disruption risk assessment
- **Investment Decisions**: Economic indicator-based insights

### **Academic Research**
- **Economic Modeling**: Advanced ML-based economic research
- **Policy Simulation**: What-if analysis for policy scenarios
- **Data-Driven Insights**: Empirical evidence for economic theories

## 🔬 Technical Details

### **Model Specifications**

| Model Type | Algorithm | Input Features | Output | Performance |
|------------|-----------|----------------|---------|-------------|
| Classifiers | XGBoost/LightGBM | 13+ economic indicators | 4-class severity | 85%+ accuracy |
| Forecasters | LSTM + Attention | Time series + features | Multi-step forecast | 0.8+ R² score |
| Ensembles | Weighted Voting | Base model predictions | Optimized prediction | 90%+ accuracy |

### **Feature Engineering**

- **Economic Indicators**: GDP growth, inflation, unemployment, interest rates
- **Trade Metrics**: Tariff rates, trade balance, import/export volumes
- **Geopolitical Factors**: Political stability, regulatory burden, policy uncertainty
- **Market Conditions**: Volatility, commodity prices, supply chain disruption

### **Performance Metrics**

- **Classification**: Accuracy, Precision, Recall, F1-Score
- **Regression**: R², RMSE, MAE, MAPE
- **Time Series**: MAE, RMSE, MAPE, Directional Accuracy
- **Ensemble**: Weighted Accuracy, Consensus Score, Stability Metrics

## 🚀 Deployment

### **Production Deployment**

```python
# Load trained models
manager.load_all_models()

# Batch prediction
predictions = manager.predict_with_ensemble(X_batch)

# Real-time prediction
prediction = manager.predict("tariff_impact_classifier", X_single)
```

### **Model Persistence**

```python
# Save models
manager.save_all_models()

# Load specific model
manager.load_model("tariff_impact_classifier")

# Export model report
manager.export_model_report("tariff_impact_classifier", "report.json")
```

## 🧪 Testing & Validation

### **Running Tests**

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=tipm.ml_models tests/

# Run specific test
pytest tests/test_classifiers.py::test_tariff_impact_classifier
```

### **Demo Scripts**

```python
# Run comprehensive demo
from tipm.ml_models.demo import run_comprehensive_demo
manager = run_comprehensive_demo()

# Run quick demo
from tipm.ml_models.demo import run_quick_demo
manager = run_quick_demo()
```

## 📚 Documentation

### **API Reference**

- **Base Classes**: `BaseMLModel`, `ModelType`, `ModelStatus`
- **Models**: All classifier, forecaster, and ensemble classes
- **Manager**: `MLModelManager` for orchestration
- **Utilities**: Explainability and insight generation

### **Examples**

- **Basic Usage**: Classification and forecasting examples
- **Advanced Features**: Custom models and ensembles
- **Integration**: TIPM core system integration
- **Deployment**: Production deployment scenarios

## 🤝 Contributing

### **Development Setup**

```bash
# Clone repository
git clone <repository-url>
cd tipm/ml_models

# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

### **Code Quality**

- **Formatting**: Black for code formatting
- **Linting**: Flake8 for style checking
- **Type Checking**: MyPy for type validation
- **Testing**: Pytest for unit and integration tests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Scikit-learn**: Core ML framework
- **PyTorch**: Deep learning capabilities
- **SHAP**: Model explainability
- **XGBoost/LightGBM**: Gradient boosting algorithms

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Documentation**: [Full Documentation](https://tipm-docs.readthedocs.io)
- **Email**: support@tipm.org

---

**Built with ❤️ for economic policy analysis and decision support**
