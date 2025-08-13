"""
TIPM ML Models Package
======================

Advanced machine learning models for Tariff Impact Propagation Model (TIPM).
This package provides a comprehensive suite of ML models including:

- Multi-class classifiers for tariff impact analysis
- LSTM-based time series forecasters
- Advanced ensemble methods
- SHAP-based explainability
- Policy insight generation

The package is designed for enterprise-grade performance and interpretability.
"""

__version__ = "1.0.0"
__author__ = "TIPM Development Team"

# Import base classes
from .base import (
    BaseMLModel,
    ModelType,
    ModelStatus,
    PredictionResult,
    TrainingResult,
    ModelMetadata,
)

# Import classifiers
from .classifiers import (
    TariffImpactClassifier,
    EconomicOutcomeClassifier,
    PolicyEffectivenessClassifier,
    IndustryVulnerabilityClassifier,
)

# Import forecasters
from .forecasters import (
    BaseTimeSeriesForecaster,
    GDPImpactForecaster,
    TradeFlowForecaster,
    EmploymentForecaster,
    PriceImpactForecaster,
    LSTMNetwork,
)

# Import ensemble methods
from .ensemble import TIPMEnsemble, ModelVoting, StackingEnsemble, DynamicEnsemble

# Import explainability components
from .explainability import SHAPExplainer, PolicyInsightGenerator

# Import model manager
from .manager import MLModelManager

# Public API
__all__ = [
    # Base classes
    "BaseMLModel",
    "ModelType",
    "ModelStatus",
    "PredictionResult",
    "TrainingResult",
    "ModelMetadata",
    # Classifiers
    "TariffImpactClassifier",
    "EconomicOutcomeClassifier",
    "PolicyEffectivenessClassifier",
    "IndustryVulnerabilityClassifier",
    # Forecasters
    "BaseTimeSeriesForecaster",
    "GDPImpactForecaster",
    "TradeFlowForecaster",
    "EmploymentForecaster",
    "PriceImpactForecaster",
    "LSTMNetwork",
    # Ensemble methods
    "TIPMEnsemble",
    "ModelVoting",
    "StackingEnsemble",
    "DynamicEnsemble",
    # Explainability
    "SHAPExplainer",
    "PolicyInsightGenerator",
    # Model management
    "MLModelManager",
]

# Package metadata
PACKAGE_INFO = {
    "name": "TIPM ML Models",
    "version": __version__,
    "description": "Advanced machine learning models for tariff impact analysis",
    "author": __author__,
    "components": {
        "classifiers": 4,
        "forecasters": 4,
        "ensemble_methods": 4,
        "explainability_tools": 2,
        "total_models": 14,
    },
    "features": [
        "Multi-class classification for tariff impact severity",
        "LSTM-based time series forecasting",
        "Advanced ensemble methods (voting, stacking, dynamic)",
        "SHAP-based model explainability",
        "Policy insight generation",
        "Model lifecycle management",
        "Performance tracking and optimization",
    ],
    "supported_model_types": [
        "Classification",
        "Multi-class Classification",
        "Binary Classification",
        "Time Series Forecasting",
        "Ensemble Methods",
        "Voting Ensembles",
        "Stacking Ensembles",
    ],
}


def get_package_info():
    """Get comprehensive package information"""
    return PACKAGE_INFO.copy()


def get_available_models():
    """Get list of all available model classes"""
    return {
        "classifiers": [
            TariffImpactClassifier,
            EconomicOutcomeClassifier,
            PolicyEffectivenessClassifier,
            IndustryVulnerabilityClassifier,
        ],
        "forecasters": [
            GDPImpactForecaster,
            TradeFlowForecaster,
            EmploymentForecaster,
            PriceImpactForecaster,
        ],
        "ensembles": [TIPMEnsemble, ModelVoting, StackingEnsemble, DynamicEnsemble],
    }


def create_default_model_manager():
    """Create and configure a default ML model manager"""
    manager = MLModelManager()
    manager.create_default_models()
    return manager


def get_model_summary():
    """Get a summary of all available models"""
    models = get_available_models()

    summary = {
        "total_models": sum(len(model_list) for model_list in models.values()),
        "categories": {},
    }

    for category, model_list in models.items():
        summary["categories"][category] = {
            "count": len(model_list),
            "models": [model.__name__ for model in model_list],
        }

    return summary


# Version compatibility check
def check_compatibility():
    """Check package compatibility and dependencies"""
    import sys

    compatibility_info = {
        "python_version": sys.version,
        "python_version_compatible": sys.version_info >= (3, 8),
        "required_packages": ["numpy", "pandas", "scikit-learn", "torch", "shap"],
        "optional_packages": ["xgboost", "lightgbm", "optuna"],
    }

    return compatibility_info


# Quick start function
def quick_start():
    """Quick start guide for using TIPM ML models"""
    print("🚀 TIPM ML Models Quick Start")
    print("=" * 40)

    # Create model manager
    manager = create_default_model_manager()

    print(f"✅ Created {len(manager.models)} default models")
    print(f"📊 Classifiers: {len(manager.classifiers)}")
    print(f"📈 Forecasters: {len(manager.forecasters)}")
    print(f"🎯 Ensembles: {len(manager.ensembles)}")

    print("\n🔧 Next steps:")
    print("1. Prepare your training data (X, y)")
    print("2. Train models: manager.train_all_models(X, y)")
    print("3. Make predictions: manager.predict(model_id, X)")
    print("4. Get explanations: manager.explain_prediction(model_id, X)")
    print(
        "5. Generate insights: manager.generate_policy_insights(model_id, explanation)"
    )

    return manager
