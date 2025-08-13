"""
ML Model Manager for TIPM
=========================

Centralized management and orchestration of all ML models,
including training, prediction, and model lifecycle management.
"""

import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime
import json
import pickle
from pathlib import Path

# ML Libraries
try:
    import numpy as np
    import pandas as pd

    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None
    pd = None

# Base classes
from .base import BaseMLModel, ModelType, PredictionResult, ModelStatus
from .classifiers import (
    TariffImpactClassifier,
    EconomicOutcomeClassifier,
    PolicyEffectivenessClassifier,
    IndustryVulnerabilityClassifier,
)
from .forecasters import (
    GDPImpactForecaster,
    TradeFlowForecaster,
    EmploymentForecaster,
    PriceImpactForecaster,
)
from .ensemble import TIPMEnsemble, ModelVoting, StackingEnsemble, DynamicEnsemble
from .explainability import SHAPExplainer, PolicyInsightGenerator

logger = logging.getLogger(__name__)


class MLModelManager:
    """
    Centralized ML model manager for TIPM

    Manages all ML models, their training, predictions, and lifecycle.
    Provides unified interface for model operations.
    """

    def __init__(self, models_dir: str = "models"):
        """
        Initialize the ML model manager

        Args:
            models_dir: Directory to store trained models
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)

        # Model registry
        self.models: Dict[str, BaseMLModel] = {}
        self.model_configs: Dict[str, Dict[str, Any]] = {}

        # Model categories
        self.classifiers: Dict[str, BaseMLModel] = {}
        self.forecasters: Dict[str, BaseMLModel] = {}
        self.ensembles: Dict[str, BaseMLModel] = {}

        # Explainability components
        self.explainers: Dict[str, SHAPExplainer] = {}
        self.insight_generators: Dict[str, PolicyInsightGenerator] = {}

        # Performance tracking
        self.performance_history: Dict[str, List[Dict[str, Any]]] = {}

        logger.info(f"Initialized MLModelManager with models directory: {models_dir}")

    def register_model(self, model: BaseMLModel, category: str = "general"):
        """
        Register a model with the manager

        Args:
            model: ML model to register
            category: Category of the model (classifier, forecaster, ensemble)
        """
        try:
            model_id = model.model_id

            if model_id in self.models:
                logger.warning(f"Model {model_id} already registered, overwriting")

            # Register model
            self.models[model_id] = model

            # Categorize model
            if category == "classifier" or model.model_type in [
                ModelType.CLASSIFICATION,
                ModelType.MULTI_CLASS,
                ModelType.BINARY,
            ]:
                self.classifiers[model_id] = model
            elif category == "forecaster" or model.model_type == ModelType.TIME_SERIES:
                self.forecasters[model_id] = model
            elif category == "ensemble" or model.model_type == ModelType.ENSEMBLE:
                self.ensembles[model_id] = model

            # Initialize explainability components
            if hasattr(model, "predict"):
                self.explainers[model_id] = SHAPExplainer(model)
                self.insight_generators[model_id] = PolicyInsightGenerator(model)

            # Initialize performance tracking
            self.performance_history[model_id] = []

            logger.info(f"Registered model {model_id} in category {category}")

        except Exception as e:
            logger.error(f"Failed to register model {model.model_id}: {e}")
            raise

    def create_default_models(self):
        """Create and register default TIPM models"""
        try:
            logger.info("Creating default TIPM models...")

            # Create classifiers
            classifiers = [
                TariffImpactClassifier(),
                EconomicOutcomeClassifier(),
                PolicyEffectivenessClassifier(),
                IndustryVulnerabilityClassifier(),
            ]

            for classifier in classifiers:
                self.register_model(classifier, "classifier")

            # Create forecasters
            forecasters = [
                GDPImpactForecaster(),
                TradeFlowForecaster(),
                EmploymentForecaster(),
                PriceImpactForecaster(),
            ]

            for forecaster in forecasters:
                self.register_model(forecaster, "forecaster")

            # Create ensemble
            ensemble = TIPMEnsemble()
            self.register_model(ensemble, "ensemble")

            logger.info(
                f"Created {len(classifiers)} classifiers, {len(forecasters)} forecasters, and 1 ensemble"
            )

        except Exception as e:
            logger.error(f"Failed to create default models: {e}")
            raise

    def train_model(
        self,
        model_id: str,
        X: Union[pd.DataFrame, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        **kwargs,
    ) -> bool:
        """
        Train a specific model

        Args:
            model_id: ID of the model to train
            X: Training features
            y: Training targets
            **kwargs: Additional training parameters

        Returns:
            True if training successful, False otherwise
        """
        try:
            if model_id not in self.models:
                logger.error(f"Model {model_id} not found")
                return False

            model = self.models[model_id]
            logger.info(f"Starting training for model {model_id}")

            # Train the model
            trained_model = model.fit(X, y, **kwargs)

            if trained_model._is_trained:
                logger.info(f"Successfully trained model {model_id}")

                # Save model
                self.save_model(model_id)

                # Update performance history
                self._update_performance_history(
                    model_id,
                    "training",
                    {
                        "training_score": model.metadata.training_score,
                        "feature_count": model.metadata.feature_count,
                        "sample_count": model.metadata.sample_count,
                    },
                )

                return True
            else:
                logger.error(f"Model {model_id} training failed")
                return False

        except Exception as e:
            logger.error(f"Failed to train model {model_id}: {e}")
            return False

    def train_all_models(
        self,
        X: Union[pd.DataFrame, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        **kwargs,
    ) -> Dict[str, bool]:
        """
        Train all registered models

        Args:
            X: Training features
            y: Training targets
            **kwargs: Additional training parameters

        Returns:
            Dictionary mapping model IDs to training success status
        """
        results = {}

        for model_id in self.models:
            logger.info(f"Training model {model_id}")
            success = self.train_model(model_id, X, y, **kwargs)
            results[model_id] = success

        return results

    def predict(
        self, model_id: str, X: Union[pd.DataFrame, np.ndarray]
    ) -> Optional[PredictionResult]:
        """
        Make predictions using a specific model

        Args:
            model_id: ID of the model to use
            X: Input features

        Returns:
            Prediction result or None if failed
        """
        try:
            if model_id not in self.models:
                logger.error(f"Model {model_id} not found")
                return None

            model = self.models[model_id]

            if not model._is_trained:
                logger.error(f"Model {model_id} is not trained")
                return None

            # Make prediction
            prediction = model.predict(X)

            # Update performance history
            self._update_performance_history(
                model_id,
                "prediction",
                {
                    "processing_time": prediction.processing_time,
                    "prediction_count": (
                        len(prediction.predictions)
                        if hasattr(prediction.predictions, "__len__")
                        else 1
                    ),
                },
            )

            return prediction

        except Exception as e:
            logger.error(f"Failed to make prediction with model {model_id}: {e}")
            return None

    def predict_with_ensemble(
        self, X: Union[pd.DataFrame, np.ndarray]
    ) -> Dict[str, PredictionResult]:
        """
        Make predictions using all models and ensemble

        Args:
            X: Input features

        Returns:
            Dictionary mapping model IDs to prediction results
        """
        results = {}

        # Get predictions from individual models
        for model_id in self.models:
            if model_id not in self.ensembles:  # Skip ensemble models
                prediction = self.predict(model_id, X)
                if prediction:
                    results[model_id] = prediction

        # Get ensemble prediction if available
        for ensemble_id in self.ensembles:
            prediction = self.predict(ensemble_id, X)
            if prediction:
                results[ensemble_id] = prediction

        return results

    def explain_prediction(
        self, model_id: str, X: Union[pd.DataFrame, np.ndarray]
    ) -> Optional[Dict[str, Any]]:
        """
        Explain a prediction using SHAP

        Args:
            model_id: ID of the model to explain
            X: Input features for explanation

        Returns:
            SHAP explanation or None if failed
        """
        try:
            if model_id not in self.explainers:
                logger.error(f"No explainer available for model {model_id}")
                return None

            explainer = self.explainers[model_id]

            # Fit explainer if not already fitted
            if explainer.explainer is None:
                explainer.fit_explainer(X)

            # Generate explanation
            explanation = explainer.explain_prediction(X)

            return explanation

        except Exception as e:
            logger.error(f"Failed to explain prediction for model {model_id}: {e}")
            return None

    def generate_policy_insights(
        self, model_id: str, explanation: Dict[str, Any], context: Dict[str, Any] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Generate policy insights from model explanation

        Args:
            model_id: ID of the model
            explanation: SHAP explanation
            context: Additional context for insight generation

        Returns:
            Policy insights or None if failed
        """
        try:
            if model_id not in self.insight_generators:
                logger.error(f"No insight generator available for model {model_id}")
                return None

            insight_generator = self.insight_generators[model_id]
            insights = insight_generator.generate_policy_insights(explanation, context)

            return insights

        except Exception as e:
            logger.error(
                f"Failed to generate policy insights for model {model_id}: {e}"
            )
            return None

    def get_model_status(self, model_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status information for a specific model

        Args:
            model_id: ID of the model

        Returns:
            Model status information or None if not found
        """
        if model_id not in self.models:
            return None

        model = self.models[model_id]

        status = {
            "model_id": model_id,
            "name": model.name,
            "description": model.description,
            "model_type": model.model_type.value,
            "is_trained": model._is_trained,
            "status": (
                model.metadata.status.value if model.metadata.status else "unknown"
            ),
            "training_score": model.metadata.training_score,
            "validation_score": model.metadata.validation_score,
            "last_trained": (
                model.metadata.last_trained.isoformat()
                if model.metadata.last_trained
                else None
            ),
            "feature_count": model.metadata.feature_count,
            "sample_count": model.metadata.sample_count,
        }

        return status

    def get_all_model_status(self) -> Dict[str, Dict[str, Any]]:
        """
        Get status information for all models

        Returns:
            Dictionary mapping model IDs to status information
        """
        status = {}

        for model_id in self.models:
            model_status = self.get_model_status(model_id)
            if model_status:
                status[model_id] = model_status

        return status

    def save_model(self, model_id: str) -> bool:
        """
        Save a trained model to disk

        Args:
            model_id: ID of the model to save

        Returns:
            True if save successful, False otherwise
        """
        try:
            if model_id not in self.models:
                logger.error(f"Model {model_id} not found")
                return False

            model = self.models[model_id]

            if not model._is_trained:
                logger.warning(f"Model {model_id} is not trained, skipping save")
                return False

            # Create model directory
            model_dir = self.models_dir / model_id
            model_dir.mkdir(exist_ok=True)

            # Save model file
            model_path = model_dir / "model.pkl"
            with open(model_path, "wb") as f:
                pickle.dump(model, f)

            # Save metadata
            metadata_path = model_dir / "metadata.json"
            metadata = {
                "model_id": model_id,
                "name": model.name,
                "description": model.description,
                "model_type": model.model_type.value,
                "training_score": model.metadata.training_score,
                "validation_score": model.metadata.validation_score,
                "last_trained": (
                    model.metadata.last_trained.isoformat()
                    if model.metadata.last_trained
                    else None
                ),
                "feature_count": model.metadata.feature_count,
                "sample_count": model.metadata.sample_count,
                "saved_at": datetime.now().isoformat(),
            }

            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)

            logger.info(f"Saved model {model_id} to {model_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save model {model_id}: {e}")
            return False

    def load_model(self, model_id: str) -> bool:
        """
        Load a saved model from disk

        Args:
            model_id: ID of the model to load

        Returns:
            True if load successful, False otherwise
        """
        try:
            model_dir = self.models_dir / model_id
            model_path = model_dir / "model.pkl"
            metadata_path = model_dir / "metadata.json"

            if not model_path.exists():
                logger.error(f"Model file not found: {model_path}")
                return False

            # Load model
            with open(model_path, "rb") as f:
                model = pickle.load(f)

            # Verify metadata
            if metadata_path.exists():
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)

                # Update model metadata
                if hasattr(model, "metadata"):
                    model.metadata.last_trained = datetime.fromisoformat(
                        metadata.get("last_trained", "")
                    )
                    model.metadata.training_score = metadata.get("training_score", 0.0)
                    model.metadata.validation_score = metadata.get(
                        "validation_score", 0.0
                    )
                    model.metadata.feature_count = metadata.get("feature_count", 0)
                    model.metadata.sample_count = metadata.get("sample_count", 0)

            # Register loaded model
            self.register_model(model)

            logger.info(f"Loaded model {model_id} from {model_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to load model {model_id}: {e}")
            return False

    def save_all_models(self) -> Dict[str, bool]:
        """
        Save all trained models to disk

        Returns:
            Dictionary mapping model IDs to save success status
        """
        results = {}

        for model_id in self.models:
            success = self.save_model(model_id)
            results[model_id] = success

        return results

    def load_all_models(self) -> Dict[str, bool]:
        """
        Load all saved models from disk

        Returns:
            Dictionary mapping model IDs to load success status
        """
        results = {}

        # Find all model directories
        for model_dir in self.models_dir.iterdir():
            if model_dir.is_dir() and (model_dir / "model.pkl").exists():
                model_id = model_dir.name
                success = self.load_model(model_id)
                results[model_id] = success

        return results

    def delete_model(self, model_id: str) -> bool:
        """
        Delete a model and its files

        Args:
            model_id: ID of the model to delete

        Returns:
            True if deletion successful, False otherwise
        """
        try:
            # Remove from registries
            if model_id in self.models:
                del self.models[model_id]

            if model_id in self.classifiers:
                del self.classifiers[model_id]

            if model_id in self.forecasters:
                del self.forecasters[model_id]

            if model_id in self.ensembles:
                del self.ensembles[model_id]

            if model_id in self.explainers:
                del self.explainers[model_id]

            if model_id in self.insight_generators:
                del self.insight_generators[model_id]

            if model_id in self.performance_history:
                del self.performance_history[model_id]

            # Remove files
            model_dir = self.models_dir / model_id
            if model_dir.exists():
                import shutil

                shutil.rmtree(model_dir)

            logger.info(f"Deleted model {model_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete model {model_id}: {e}")
            return False

    def get_model_performance(self, model_id: str) -> List[Dict[str, Any]]:
        """
        Get performance history for a specific model

        Args:
            model_id: ID of the model

        Returns:
            List of performance records
        """
        return self.performance_history.get(model_id, [])

    def get_overall_performance(self) -> Dict[str, Any]:
        """
        Get overall performance summary for all models

        Returns:
            Overall performance summary
        """
        summary = {
            "total_models": len(self.models),
            "trained_models": sum(1 for m in self.models.values() if m._is_trained),
            "model_categories": {
                "classifiers": len(self.classifiers),
                "forecasters": len(self.forecasters),
                "ensembles": len(self.ensembles),
            },
            "performance_summary": {},
        }

        # Calculate performance metrics for each model
        for model_id in self.models:
            model = self.models[model_id]
            if model._is_trained:
                performance = {
                    "training_score": model.metadata.training_score or 0.0,
                    "validation_score": model.metadata.validation_score or 0.0,
                    "feature_count": model.metadata.feature_count or 0,
                    "sample_count": model.metadata.sample_count or 0,
                }
                summary["performance_summary"][model_id] = performance

        return summary

    def _update_performance_history(
        self, model_id: str, operation: str, metrics: Dict[str, Any]
    ):
        """Update performance history for a model"""
        if model_id not in self.performance_history:
            self.performance_history[model_id] = []

        record = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "metrics": metrics,
        }

        self.performance_history[model_id].append(record)

        # Keep only last 100 records
        if len(self.performance_history[model_id]) > 100:
            self.performance_history[model_id] = self.performance_history[model_id][
                -100:
            ]

    def export_model_report(self, model_id: str, output_path: str) -> bool:
        """
        Export a comprehensive report for a model

        Args:
            model_id: ID of the model
            output_path: Path to save the report

        Returns:
            True if export successful, False otherwise
        """
        try:
            if model_id not in self.models:
                logger.error(f"Model {model_id} not found")
                return False

            model = self.models[model_id]

            # Gather report data
            report = {
                "model_info": self.get_model_status(model_id),
                "performance_history": self.get_model_performance(model_id),
                "training_history": (
                    model.training_history if hasattr(model, "training_history") else []
                ),
                "hyperparameters": (
                    model.hyperparameters if hasattr(model, "hyperparameters") else {}
                ),
                "export_timestamp": datetime.now().isoformat(),
            }

            # Save report
            with open(output_path, "w") as f:
                json.dump(report, f, indent=2)

            logger.info(f"Exported model report for {model_id} to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to export model report for {model_id}: {e}")
            return False

    def create_ensemble_from_models(
        self, ensemble_id: str, model_ids: List[str], ensemble_type: str = "voting"
    ) -> bool:
        """
        Create an ensemble from existing models

        Args:
            ensemble_id: ID for the new ensemble
            model_ids: List of model IDs to include in ensemble
            ensemble_type: Type of ensemble (voting, stacking, dynamic)

        Returns:
            True if ensemble creation successful, False otherwise
        """
        try:
            # Verify all models exist and are trained
            for model_id in model_ids:
                if model_id not in self.models:
                    logger.error(f"Model {model_id} not found")
                    return False

                if not self.models[model_id]._is_trained:
                    logger.error(f"Model {model_id} is not trained")
                    return False

            # Create appropriate ensemble
            if ensemble_type == "voting":
                ensemble = ModelVoting(ensemble_id)
                for model_id in model_ids:
                    ensemble.add_model(self.models[model_id])

            elif ensemble_type == "stacking":
                ensemble = StackingEnsemble(ensemble_id)
                for model_id in model_ids:
                    ensemble.add_base_model(self.models[model_id])

                # Use first model as meta-learner (simplified approach)
                if model_ids:
                    ensemble.set_meta_model(self.models[model_ids[0]])

            elif ensemble_type == "dynamic":
                ensemble = DynamicEnsemble(ensemble_id)
                for model_id in model_ids:
                    ensemble.add_model(self.models[model_id])

            else:
                logger.error(f"Unsupported ensemble type: {ensemble_type}")
                return False

            # Register ensemble
            self.register_model(ensemble, "ensemble")

            logger.info(
                f"Created {ensemble_type} ensemble {ensemble_id} with {len(model_ids)} models"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to create ensemble {ensemble_id}: {e}")
            return False
