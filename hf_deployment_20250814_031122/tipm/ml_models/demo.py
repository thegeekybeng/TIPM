"""
TIPM ML Models Demo Script
==========================

Comprehensive demonstration of the TIPM ML stack capabilities including:
- Model creation and training
- Predictions and forecasting
- Ensemble methods
- SHAP explainability
- Policy insights generation
"""

import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import warnings

# Suppress warnings for demo
warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import TIPM ML models
from . import (
    MLModelManager,
    TariffImpactClassifier,
    GDPImpactForecaster,
    TIPMEnsemble,
    SHAPExplainer,
    PolicyInsightGenerator,
)


def create_demo_data():
    """Create synthetic demo data for training and testing"""
    logger.info("Creating demo data...")

    # Set random seed for reproducibility
    np.random.seed(42)

    # Create sample size
    n_samples = 1000

    # Generate synthetic features
    data = {
        # Economic indicators
        "gdp_growth": np.random.normal(2.5, 1.0, n_samples),
        "inflation_rate": np.random.normal(2.0, 0.5, n_samples),
        "unemployment_rate": np.random.normal(5.0, 1.5, n_samples),
        "interest_rate": np.random.normal(3.0, 1.0, n_samples),
        # Trade indicators
        "tariff_rate": np.random.uniform(0, 25, n_samples),
        "trade_balance": np.random.normal(0, 50, n_samples),
        "import_volume": np.random.normal(100, 20, n_samples),
        "export_volume": np.random.normal(120, 25, n_samples),
        # Geopolitical factors
        "political_stability": np.random.uniform(0.3, 1.0, n_samples),
        "regulatory_burden": np.random.uniform(0.1, 0.9, n_samples),
        "policy_uncertainty": np.random.uniform(0.1, 0.8, n_samples),
        # Market conditions
        "market_volatility": np.random.uniform(0.1, 0.7, n_samples),
        "commodity_prices": np.random.normal(100, 15, n_samples),
        "supply_chain_disruption": np.random.uniform(0, 1.0, n_samples),
    }

    # Create DataFrame
    X = pd.DataFrame(data)

    # Generate synthetic targets for classification
    # Tariff impact severity (0: Low, 1: Medium, 2: High, 3: Critical)
    tariff_impact = np.zeros(n_samples)

    for i in range(n_samples):
        # Complex logic for tariff impact
        base_score = (
            data["tariff_rate"][i] * 0.3
            + data["trade_balance"][i] * 0.001
            + data["political_stability"][i] * 0.2
            + data["regulatory_burden"][i] * 0.15
            + data["market_volatility"][i] * 0.25
        )

        if base_score < 5:
            tariff_impact[i] = 0  # Low
        elif base_score < 10:
            tariff_impact[i] = 1  # Medium
        elif base_score < 15:
            tariff_impact[i] = 2  # High
        else:
            tariff_impact[i] = 3  # Critical

    # Generate synthetic targets for regression (GDP impact)
    gdp_impact = (
        -data["tariff_rate"] * 0.1
        + data["gdp_growth"] * 0.5
        + data["trade_balance"] * 0.002
        + data["political_stability"] * 0.3
        + np.random.normal(0, 0.5, n_samples)
    )

    # Create target variables
    y_classification = tariff_impact.astype(int)
    y_regression = gdp_impact

    logger.info(f"Created demo data: {n_samples} samples, {len(data)} features")
    logger.info(f"Classification targets: {np.bincount(y_classification)}")
    logger.info(
        f"Regression targets: mean={y_regression.mean():.2f}, std={y_regression.std():.2f}"
    )

    return X, y_classification, y_regression


def demo_classifiers(manager, X, y_classification):
    """Demonstrate classifier models"""
    logger.info("\n" + "=" * 50)
    logger.info("DEMO: CLASSIFIERS")
    logger.info("=" * 50)

    # Train classifiers
    classifier_ids = [model_id for model_id in manager.classifiers.keys()]

    for model_id in classifier_ids:
        logger.info(f"Training {model_id}...")
        success = manager.train_model(model_id, X, y_classification)

        if success:
            # Make predictions
            prediction = manager.predict(model_id, X[:10])  # Test on first 10 samples
            if prediction:
                logger.info(f"✅ {model_id} trained successfully")
                logger.info(
                    f"   Training score: {manager.models[model_id].metadata.training_score:.3f}"
                )
                logger.info(f"   Predictions shape: {prediction.predictions.shape}")
        else:
            logger.error(f"❌ {model_id} training failed")


def demo_forecasters(manager, X, y_regression):
    """Demonstrate forecaster models"""
    logger.info("\n" + "=" * 50)
    logger.info("DEMO: FORECASTERS")
    logger.info("=" * 50)

    # Create time series data for forecasters
    # Convert regression targets to time series format
    time_series_data = pd.DataFrame(
        {
            "gdp_impact": y_regression,
            "tariff_rate": X["tariff_rate"],
            "trade_balance": X["trade_balance"],
        }
    )

    # Add time index
    time_series_data.index = pd.date_range(
        start="2020-01-01", periods=len(time_series_data), freq="M"
    )

    # Train forecasters
    forecaster_ids = [model_id for model_id in manager.forecasters.keys()]

    for model_id in forecaster_ids:
        logger.info(f"Training {model_id}...")

        # For demo, use a subset of data
        subset_size = min(100, len(time_series_data))
        X_subset = time_series_data.iloc[:subset_size]
        y_subset = time_series_data["gdp_impact"].iloc[:subset_size]

        success = manager.train_model(model_id, X_subset, y_subset)

        if success:
            logger.info(f"✅ {model_id} trained successfully")
            logger.info(
                f"   Training score: {manager.models[model_id].metadata.training_score:.3f}"
            )
        else:
            logger.error(f"❌ {model_id} training failed")


def demo_ensembles(manager, X, y_classification):
    """Demonstrate ensemble methods"""
    logger.info("\n" + "=" * 50)
    logger.info("DEMO: ENSEMBLE METHODS")
    logger.info("=" * 50)

    # Create ensemble from trained classifiers
    classifier_ids = [
        model_id
        for model_id in manager.classifiers.keys()
        if manager.models[model_id]._is_trained
    ]

    if len(classifier_ids) >= 2:
        # Create voting ensemble
        ensemble_id = "demo_voting_ensemble"
        success = manager.create_ensemble_from_models(
            ensemble_id, classifier_ids[:2], "voting"
        )

        if success:
            logger.info(f"✅ Created voting ensemble: {ensemble_id}")

            # Test ensemble prediction
            prediction = manager.predict(ensemble_id, X[:10])
            if prediction:
                logger.info(
                    f"   Ensemble predictions shape: {prediction.predictions.shape}"
                )
        else:
            logger.error(f"❌ Failed to create ensemble")
    else:
        logger.warning("Need at least 2 trained classifiers for ensemble demo")


def demo_explainability(manager, X):
    """Demonstrate SHAP explainability and policy insights"""
    logger.info("\n" + "=" * 50)
    logger.info("DEMO: EXPLAINABILITY & POLICY INSIGHTS")
    logger.info("=" * 50)

    # Get a trained classifier for explanation
    trained_classifiers = [
        model_id
        for model_id in manager.classifiers.keys()
        if manager.models[model_id]._is_trained
    ]

    if not trained_classifiers:
        logger.warning("No trained classifiers available for explainability demo")
        return

    model_id = trained_classifiers[0]
    logger.info(f"Demonstrating explainability for {model_id}")

    # Explain a prediction
    explanation = manager.explain_prediction(model_id, X[:5])

    if explanation:
        logger.info("✅ SHAP explanation generated")
        logger.info(
            f"   Feature importance: {len(explanation['feature_importance'])} features"
        )

        # Show top features
        top_features = list(explanation["feature_importance"].items())[:5]
        logger.info("   Top 5 important features:")
        for feature, importance in top_features:
            logger.info(f"     {feature}: {importance:.3f}")

        # Generate policy insights
        context = {
            "analysis_date": datetime.now().isoformat(),
            "policy_focus": "tariff_impact_mitigation",
            "stakeholder": "government_policy_maker",
        }

        insights = manager.generate_policy_insights(model_id, explanation, context)

        if insights:
            logger.info("✅ Policy insights generated")
            logger.info(f"   Key drivers: {len(insights['key_drivers'])}")
            logger.info(f"   Policy levers: {len(insights['policy_levers'])}")
            logger.info(f"   Risk factors: {len(insights['risk_factors'])}")
            logger.info(f"   Opportunities: {len(insights['opportunity_areas'])}")

            # Show sample recommendations
            if insights["policy_recommendations"]:
                logger.info("   Sample policy recommendations:")
                for i, rec in enumerate(insights["policy_recommendations"][:3]):
                    logger.info(f"     {i+1}. {rec['specific_action']}")
        else:
            logger.error("❌ Failed to generate policy insights")
    else:
        logger.error("❌ Failed to generate SHAP explanation")


def demo_model_management(manager):
    """Demonstrate model management capabilities"""
    logger.info("\n" + "=" * 50)
    logger.info("DEMO: MODEL MANAGEMENT")
    logger.info("=" * 50)

    # Get model status
    status = manager.get_all_model_status()
    logger.info(f"Model Status Summary:")
    logger.info(f"  Total models: {len(status)}")

    trained_count = sum(1 for s in status.values() if s["is_trained"])
    logger.info(f"  Trained models: {trained_count}")

    # Show model categories
    logger.info(f"  Classifiers: {len(manager.classifiers)}")
    logger.info(f"  Forecasters: {len(manager.forecasters)}")
    logger.info(f"  Ensembles: {len(manager.ensembles)}")

    # Get performance summary
    performance = manager.get_overall_performance()
    logger.info(f"Performance Summary:")
    logger.info(
        f"  Overall performance tracked for {len(performance['performance_summary'])} models"
    )

    # Save models
    logger.info("Saving all models...")
    save_results = manager.save_all_models()
    saved_count = sum(1 for success in save_results.values() if success)
    logger.info(f"  Saved {saved_count}/{len(save_results)} models")


def run_comprehensive_demo():
    """Run the comprehensive TIPM ML models demo"""
    logger.info("🚀 TIPM ML Models Comprehensive Demo")
    logger.info("=" * 60)

    try:
        # Create model manager
        logger.info("Initializing ML Model Manager...")
        manager = MLModelManager(models_dir="demo_models")
        manager.create_default_models()

        # Create demo data
        X, y_classification, y_regression = create_demo_data()

        # Run demos
        demo_classifiers(manager, X, y_classification)
        demo_forecasters(manager, X, y_regression)
        demo_ensembles(manager, X, y_classification)
        demo_explainability(manager, X)
        demo_model_management(manager)

        # Final summary
        logger.info("\n" + "=" * 60)
        logger.info("🎉 DEMO COMPLETED SUCCESSFULLY!")
        logger.info("=" * 60)

        logger.info("✅ What was demonstrated:")
        logger.info("  • Multi-class classification models")
        logger.info("  • LSTM-based time series forecasting")
        logger.info("  • Advanced ensemble methods")
        logger.info("  • SHAP-based model explainability")
        logger.info("  • Policy insight generation")
        logger.info("  • Comprehensive model management")

        logger.info("\n🔧 Next steps:")
        logger.info("  • Use real economic data for training")
        logger.info("  • Fine-tune hyperparameters")
        logger.info("  • Deploy models in production")
        logger.info("  • Integrate with TIPM core system")

        return manager

    except Exception as e:
        logger.error(f"Demo failed: {e}")
        raise


def run_quick_demo():
    """Run a quick demo focusing on key features"""
    logger.info("⚡ TIPM ML Models Quick Demo")
    logger.info("=" * 40)

    try:
        # Create manager and models
        manager = MLModelManager(models_dir="quick_demo_models")
        manager.create_default_models()

        # Create minimal demo data
        X, y_classification, _ = create_demo_data()
        X_subset = X[:100]  # Use smaller dataset
        y_subset = y_classification[:100]

        # Train one classifier
        classifier_id = list(manager.classifiers.keys())[0]
        logger.info(f"Training {classifier_id}...")
        success = manager.train_model(classifier_id, X_subset, y_subset)

        if success:
            # Make prediction
            prediction = manager.predict(classifier_id, X_subset[:5])
            if prediction:
                logger.info(f"✅ Prediction successful: {prediction.predictions.shape}")

            # Generate explanation
            explanation = manager.explain_prediction(classifier_id, X_subset[:3])
            if explanation:
                logger.info(
                    f"✅ Explainability working: {len(explanation['feature_importance'])} features"
                )

        logger.info("🎯 Quick demo completed!")
        return manager

    except Exception as e:
        logger.error(f"Quick demo failed: {e}")
        raise


if __name__ == "__main__":
    # Run the comprehensive demo
    try:
        manager = run_comprehensive_demo()
        print("\n🎉 Demo completed successfully! Check the logs for details.")

    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Try running the quick demo instead: run_quick_demo()")
