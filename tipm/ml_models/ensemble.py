"""
Advanced Ensemble Methods for TIPM
==================================

Sophisticated ensemble techniques including voting, stacking, and dynamic
ensembles for robust, accurate predictions.
"""

import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime
import numpy as np
import pandas as pd

# ML Libraries
try:
    from sklearn.ensemble import VotingClassifier, VotingRegressor
    from sklearn.linear_model import LogisticRegression, LinearRegression
    from sklearn.model_selection import cross_val_score, StratifiedKFold
    from sklearn.metrics import accuracy_score, r2_score, mean_squared_error

    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# Base classes
from .base import BaseMLModel, ModelType, PredictionResult, ModelStatus, TrainingResult

logger = logging.getLogger(__name__)


class TIPMEnsemble(BaseMLModel):
    """
    Advanced ensemble system for TIPM predictions

    Combines multiple models using sophisticated ensemble techniques
    for maximum accuracy and robustness.
    """

    def __init__(self, model_id: str = "tipm_ensemble"):
        super().__init__(
            model_id=model_id,
            name="TIPM Ensemble System",
            description="Advanced ensemble combining multiple ML models for robust predictions",
            model_type=ModelType.ENSEMBLE,
        )

        # Ensemble configuration
        self.base_models = []
        self.meta_model = None
        self.ensemble_type = "voting"  # voting, stacking, dynamic

        # Performance tracking
        self.model_weights = {}
        self.performance_history = {}

        # Ensemble parameters
        self.hyperparameters = {
            "ensemble_method": "weighted_voting",
            "weight_optimization": True,
            "cross_validation_folds": 5,
            "meta_learning": True,
        }

        logger.info(f"Initialized TIPMEnsemble: {model_id}")

    def add_model(self, model: BaseMLModel, weight: float = 1.0):
        """Add a model to the ensemble"""
        if not model._is_trained:
            raise ValueError(
                f"Model {model.model_id} must be trained before adding to ensemble"
            )

        self.base_models.append(model)
        self.model_weights[model.model_id] = weight

        logger.info(f"Added model {model.model_id} to ensemble with weight {weight}")

    def remove_model(self, model_id: str):
        """Remove a model from the ensemble"""
        self.base_models = [m for m in self.base_models if m.model_id != model_id]
        if model_id in self.model_weights:
            del self.model_weights[model_id]

        logger.info(f"Removed model {model_id} from ensemble")

    def _create_model(self):
        """Create the ensemble model"""
        if not self.base_models:
            raise RuntimeError("No models added to ensemble")

        if self.ensemble_type == "voting":
            return self._create_voting_ensemble()
        elif self.ensemble_type == "stacking":
            return self._create_stacking_ensemble()
        else:
            raise ValueError(f"Unsupported ensemble type: {self.ensemble_type}")

    def _create_voting_ensemble(self):
        """Create voting ensemble"""
        if not SKLEARN_AVAILABLE:
            raise RuntimeError("Scikit-learn required for voting ensembles")

        # Determine if classification or regression
        first_model = self.base_models[0]
        if first_model.model_type in [
            ModelType.CLASSIFICATION,
            ModelType.MULTI_CLASS,
            ModelType.BINARY,
        ]:
            ensemble = VotingClassifier(
                estimators=[(m.model_id, m._model) for m in self.base_models],
                voting=(
                    "soft"
                    if self.hyperparameters["ensemble_method"] == "weighted_voting"
                    else "hard"
                ),
            )
        else:
            ensemble = VotingRegressor(
                estimators=[(m.model_id, m._model) for m in self.base_models]
            )

        return ensemble

    def _create_stacking_ensemble(self):
        """Create stacking ensemble with meta-learner"""
        if not SKLEARN_AVAILABLE:
            raise RuntimeError("Scikit-learn required for stacking ensembles")

        # Determine meta-learner type
        first_model = self.base_models[0]
        if first_model.model_type in [
            ModelType.CLASSIFICATION,
            ModelType.MULTI_CLASS,
            ModelType.BINARY,
        ]:
            self.meta_model = LogisticRegression(random_state=42)
        else:
            self.meta_model = LinearRegression()

        return self.meta_model

    def _prepare_features(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Prepare features for ensemble prediction"""
        # For ensemble, we need predictions from all base models
        if not self.base_models:
            raise RuntimeError("No models in ensemble")

        # Get predictions from all base models
        base_predictions = []
        for model in self.base_models:
            pred_result = model.predict(X)
            base_predictions.append(pred_result.predictions)

        # Stack predictions horizontally
        if isinstance(base_predictions[0], np.ndarray):
            stacked_predictions = np.column_stack(base_predictions)
        else:
            stacked_predictions = np.array(base_predictions).T

        return stacked_predictions

    def _prepare_targets(self, y: Union[pd.Series, np.ndarray]) -> np.ndarray:
        """Prepare targets for ensemble training"""
        if isinstance(y, pd.Series):
            return y.values
        return y

    def fit(
        self,
        X: Union[pd.DataFrame, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        **kwargs,
    ) -> "TIPMEnsemble":
        """Train the ensemble model"""
        if not self.base_models:
            raise RuntimeError("No models added to ensemble")

        training_start = datetime.now()

        try:
            logger.info(f"Starting ensemble training for {self.model_id}")
            self.metadata.status = ModelStatus.TRAINING

            # Create ensemble model
            self._model = self._create_model()

            if self.ensemble_type == "stacking":
                # For stacking, we need to train meta-learner on base model predictions
                base_predictions = self._get_base_predictions(X)
                self._model.fit(base_predictions, y)
            else:
                # For voting, base models are already trained
                pass

            # Optimize weights if enabled
            if self.hyperparameters["weight_optimization"]:
                self._optimize_weights(X, y)

            # Update metadata
            self._is_trained = True
            self.metadata.status = ModelStatus.TRAINED
            self.metadata.last_trained = datetime.now()
            self.metadata.feature_count = len(self.base_models)
            self.metadata.sample_count = X.shape[0] if hasattr(X, "shape") else len(X)

            # Calculate training score
            training_score = self._calculate_ensemble_score(X, y)
            self.metadata.training_score = training_score

            # Create training result
            training_result = TrainingResult(
                model_id=self.model_id,
                training_start=training_start,
                training_end=datetime.now(),
                training_score=training_score,
                validation_score=0.0,
            )
            self.training_history.append(training_result)

            logger.info(f"Ensemble training completed for {self.model_id}")
            return self

        except Exception as e:
            self.metadata.status = ModelStatus.FAILED
            logger.error(f"Ensemble training failed for {self.model_id}: {e}")
            raise

    def _get_base_predictions(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Get predictions from all base models"""
        base_predictions = []

        for model in self.base_models:
            pred_result = model.predict(X)
            predictions = pred_result.predictions

            # Handle different prediction formats
            if isinstance(predictions, np.ndarray):
                if predictions.ndim == 1:
                    base_predictions.append(predictions)
                else:
                    # For multi-output, take first output
                    base_predictions.append(predictions[:, 0])
            else:
                base_predictions.append(np.array(predictions))

        return np.column_stack(base_predictions)

    def _optimize_weights(
        self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray]
    ):
        """Optimize model weights using cross-validation"""
        if not SKLEARN_AVAILABLE:
            return

        logger.info("Optimizing ensemble weights...")

        # Get base predictions
        base_predictions = self._get_base_predictions(X)

        # Optimize weights using cross-validation
        best_score = -1
        best_weights = None

        # Grid search over weight combinations
        weight_combinations = [
            [1.0, 1.0, 1.0],  # Equal weights
            [2.0, 1.0, 1.0],  # Favor first model
            [1.0, 2.0, 1.0],  # Favor second model
            [1.0, 1.0, 2.0],  # Favor third model
            [3.0, 2.0, 1.0],  # Decreasing weights
        ]

        for weights in weight_combinations:
            if len(weights) != len(self.base_models):
                continue

            # Normalize weights
            weights = np.array(weights) / np.sum(weights)

            # Calculate weighted ensemble prediction
            weighted_pred = np.zeros_like(base_predictions[:, 0])
            for i, weight in enumerate(weights):
                weighted_pred += weight * base_predictions[:, i]

            # Calculate score
            if self.base_models[0].model_type in [
                ModelType.CLASSIFICATION,
                ModelType.MULTI_CLASS,
                ModelType.BINARY,
            ]:
                score = accuracy_score(y, np.round(weighted_pred))
            else:
                score = r2_score(y, weighted_pred)

            if score > best_score:
                best_score = score
                best_weights = weights

        # Update weights
        if best_weights is not None:
            for i, model in enumerate(self.base_models):
                self.model_weights[model.model_id] = float(best_weights[i])

            logger.info(
                f"Optimized weights: {dict(zip([m.model_id for m in self.base_models], best_weights))}"
            )

    def _calculate_ensemble_score(
        self, X: Union[pd.DataFrame, np.ndarray], y: Union[pd.Series, np.ndarray]
    ) -> float:
        """Calculate ensemble performance score"""
        try:
            predictions = self.predict(X).predictions

            if self.base_models[0].model_type in [
                ModelType.CLASSIFICATION,
                ModelType.MULTI_CLASS,
                ModelType.BINARY,
            ]:
                return accuracy_score(y, predictions)
            else:
                return r2_score(y, predictions)
        except Exception as e:
            logger.warning(f"Could not calculate ensemble score: {e}")
            return 0.0

    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> PredictionResult:
        """Make ensemble predictions"""
        if not self._is_trained:
            raise RuntimeError(
                f"Ensemble {self.model_id} must be trained before making predictions"
            )

        prediction_start = datetime.now()

        try:
            if self.ensemble_type == "stacking":
                # Stacking ensemble
                base_predictions = self._get_base_predictions(X)
                predictions = self._model.predict(base_predictions)
            else:
                # Voting ensemble
                predictions = self._weighted_voting_predict(X)

            # Calculate processing time
            processing_time = (datetime.now() - prediction_start).total_seconds()

            # Create prediction result
            result = PredictionResult(
                prediction_id=f"{self.model_id}_{prediction_start.strftime('%Y%m%d_%H%M%S')}",
                model_id=self.model_id,
                timestamp=prediction_start,
                predictions=predictions,
                input_features=X.to_dict() if hasattr(X, "to_dict") else None,
                feature_names=[m.model_id for m in self.base_models],
                prediction_type=self.model_type.value,
                processing_time=processing_time,
            )

            return result

        except Exception as e:
            logger.error(f"Ensemble prediction failed for {self.model_id}: {e}")
            raise

    def _weighted_voting_predict(
        self, X: Union[pd.DataFrame, np.ndarray]
    ) -> np.ndarray:
        """Make weighted voting predictions"""
        # Get predictions from all base models
        base_predictions = []
        for model in self.base_models:
            pred_result = model.predict(X)
            predictions = pred_result.predictions

            # Handle different prediction formats and ensure float64
            if isinstance(predictions, np.ndarray):
                if predictions.ndim == 1:
                    base_predictions.append(predictions.astype(np.float64))
                else:
                    base_predictions.append(predictions[:, 0].astype(np.float64))
            else:
                base_predictions.append(np.array(predictions, dtype=np.float64))

        # Calculate weighted average
        weighted_pred = np.zeros_like(base_predictions[0], dtype=np.float64)
        total_weight = 0.0

        for i, model in enumerate(self.base_models):
            weight = float(self.model_weights.get(model.model_id, 1.0))
            weighted_pred += weight * base_predictions[i]
            total_weight += weight

        if total_weight > 0:
            weighted_pred /= total_weight

        return weighted_pred

    def get_ensemble_analysis(self) -> Dict[str, Any]:
        """Get comprehensive ensemble analysis"""
        if not self.base_models:
            return {"error": "No models in ensemble"}

        analysis = {
            "ensemble_type": self.ensemble_type,
            "model_count": len(self.base_models),
            "models": [],
            "weights": self.model_weights.copy(),
            "performance_summary": {},
        }

        # Analyze each model
        for model in self.base_models:
            model_info = {
                "model_id": model.model_id,
                "name": model.name,
                "type": model.model_type.value,
                "training_score": model.metadata.training_score,
                "validation_score": model.metadata.validation_score,
                "last_trained": (
                    model.metadata.last_trained.isoformat()
                    if model.metadata.last_trained
                    else None
                ),
            }
            analysis["models"].append(model_info)

        # Performance summary
        if self._is_trained:
            analysis["performance_summary"] = {
                "ensemble_score": self.metadata.training_score,
                "best_model": max(
                    self.base_models, key=lambda m: m.metadata.training_score or 0
                ).model_id,
                "weight_distribution": self._analyze_weight_distribution(),
            }

        return analysis

    def _analyze_weight_distribution(self) -> Dict[str, Any]:
        """Analyze the distribution of model weights"""
        weights = list(self.model_weights.values())

        return {
            "total_weight": sum(weights),
            "average_weight": np.mean(weights),
            "weight_variance": np.var(weights),
            "dominant_model": max(self.model_weights.items(), key=lambda x: x[1])[0],
            "weight_balance": "Balanced" if np.var(weights) < 0.1 else "Unbalanced",
        }


class ModelVoting(BaseMLModel):
    """Simple voting ensemble for model combination"""

    def __init__(self, model_id: str = "model_voting"):
        super().__init__(
            model_id=model_id,
            name="Model Voting Ensemble",
            description="Simple voting ensemble combining multiple models",
            model_type=ModelType.VOTING,
        )

        self.models = []
        self.voting_method = "hard"  # hard, soft

        logger.info(f"Initialized ModelVoting: {model_id}")

    def add_model(self, model: BaseMLModel):
        """Add a model to the voting ensemble"""
        if not model._is_trained:
            raise ValueError(
                f"Model {model.model_id} must be trained before adding to voting ensemble"
            )

        self.models.append(model)
        logger.info(f"Added model {model.model_id} to voting ensemble")

    def _create_model(self):
        """Voting ensemble doesn't need a separate model"""
        return None

    def _prepare_features(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Features are handled by individual models"""
        return X

    def _prepare_targets(self, y: Union[pd.Series, np.ndarray]) -> np.ndarray:
        """Targets are handled by individual models"""
        if isinstance(y, pd.Series):
            return y.values
        return y

    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> PredictionResult:
        """Make voting predictions"""
        if not self.models:
            raise RuntimeError("No models in voting ensemble")

        prediction_start = datetime.now()

        try:
            # Get predictions from all models
            all_predictions = []
            for model in self.models:
                pred_result = model.predict(X)
                all_predictions.append(pred_result.predictions)

            # Combine predictions based on voting method
            if self.voting_method == "hard":
                # Hard voting: majority class
                predictions = self._hard_voting(all_predictions)
            else:
                # Soft voting: average probabilities
                predictions = self._soft_voting(all_predictions)

            # Calculate processing time
            processing_time = (datetime.now() - prediction_start).total_seconds()

            # Create prediction result
            result = PredictionResult(
                prediction_id=f"{self.model_id}_{prediction_start.strftime('%Y%m%d_%H%M%S')}",
                model_id=self.model_id,
                timestamp=prediction_start,
                predictions=predictions,
                input_features=X.to_dict() if hasattr(X, "to_dict") else None,
                feature_names=[m.model_id for m in self.models],
                prediction_type=self.model_type.value,
                processing_time=processing_time,
            )

            return result

        except Exception as e:
            logger.error(f"Voting prediction failed for {self.model_id}: {e}")
            raise

    def _hard_voting(self, all_predictions: List[np.ndarray]) -> np.ndarray:
        """Hard voting: majority class prediction"""
        # Convert to numpy arrays
        predictions_array = np.array(all_predictions)

        # For classification, take mode (majority)
        if predictions_array.ndim == 2:
            from scipy.stats import mode

            predictions, _ = mode(predictions_array, axis=0)
            return predictions.flatten()
        else:
            # For single predictions
            from scipy.stats import mode

            predictions, _ = mode(predictions_array, axis=0)
            return predictions

    def _soft_voting(self, all_predictions: List[np.ndarray]) -> np.ndarray:
        """Soft voting: average of probabilities"""
        # Convert to numpy arrays
        predictions_array = np.array(all_predictions)

        # Average predictions
        return np.mean(predictions_array, axis=0)


class StackingEnsemble(BaseMLModel):
    """Stacking ensemble with meta-learner"""

    def __init__(self, model_id: str = "stacking_ensemble"):
        super().__init__(
            model_id=model_id,
            name="Stacking Ensemble",
            description="Stacking ensemble with meta-learner for optimal combination",
            model_type=ModelType.STACKING,
        )

        self.base_models = []
        self.meta_model = None

        logger.info(f"Initialized StackingEnsemble: {model_id}")

    def add_base_model(self, model: BaseMLModel):
        """Add a base model to the stacking ensemble"""
        if not model._is_trained:
            raise ValueError(
                f"Model {model.model_id} must be trained before adding to stacking ensemble"
            )

        self.base_models.append(model)
        logger.info(f"Added base model {model.model_id} to stacking ensemble")

    def set_meta_model(self, model: BaseMLModel):
        """Set the meta-learner model"""
        if not model._is_trained:
            raise ValueError(
                f"Meta model {model.model_id} must be trained before setting"
            )

        self.meta_model = model
        logger.info(f"Set meta model {model.model_id} for stacking ensemble")

    def _create_model(self):
        """Stacking ensemble uses base models and meta model"""
        return None

    def _prepare_features(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Features are handled by base models"""
        return X

    def _prepare_targets(self, y: Union[pd.Series, np.ndarray]) -> np.ndarray:
        """Targets are handled by base models"""
        if isinstance(y, pd.Series):
            return y.values
        return y

    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> PredictionResult:
        """Make stacking ensemble predictions"""
        if not self.base_models or not self.meta_model:
            raise RuntimeError("Stacking ensemble requires base models and meta model")

        prediction_start = datetime.now()

        try:
            # Get predictions from base models
            base_predictions = []
            for model in self.base_models:
                pred_result = model.predict(X)
                predictions = pred_result.predictions

                # Handle different prediction formats
                if isinstance(predictions, np.ndarray):
                    if predictions.ndim == 1:
                        base_predictions.append(predictions)
                    else:
                        base_predictions.append(predictions[:, 0])
                else:
                    base_predictions.append(np.array(predictions))

            # Stack predictions
            stacked_features = np.column_stack(base_predictions)

            # Get meta model predictions
            meta_predictions = self.meta_model.predict(stacked_features).predictions

            # Calculate processing time
            processing_time = (datetime.now() - prediction_start).total_seconds()

            # Create prediction result
            result = PredictionResult(
                prediction_id=f"{self.model_id}_{prediction_start.strftime('%Y%m%d_%H%M%S')}",
                model_id=self.model_id,
                timestamp=prediction_start,
                predictions=meta_predictions,
                input_features=X.to_dict() if hasattr(X, "to_dict") else None,
                feature_names=[m.model_id for m in self.base_models],
                prediction_type=self.model_type.value,
                processing_time=processing_time,
            )

            return result

        except Exception as e:
            logger.error(f"Stacking prediction failed for {self.model_id}: {e}")
            raise


class DynamicEnsemble(BaseMLModel):
    """Dynamic ensemble that adapts based on performance"""

    def __init__(self, model_id: str = "dynamic_ensemble"):
        super().__init__(
            model_id=model_id,
            name="Dynamic Ensemble",
            description="Dynamic ensemble that adapts model weights based on recent performance",
            model_type=ModelType.ENSEMBLE,
        )

        self.models = []
        self.performance_window = 10  # Number of recent predictions to consider
        self.performance_history = {}
        self.adaptive_weights = {}

        logger.info(f"Initialized DynamicEnsemble: {model_id}")

    def add_model(self, model: BaseMLModel, initial_weight: float = 1.0):
        """Add a model to the dynamic ensemble"""
        if not model._is_trained:
            raise ValueError(
                f"Model {model.model_id} must be trained before adding to dynamic ensemble"
            )

        self.models.append(model)
        self.adaptive_weights[model.model_id] = initial_weight
        self.performance_history[model.model_id] = []

        logger.info(
            f"Added model {model.model_id} to dynamic ensemble with initial weight {initial_weight}"
        )

    def _create_model(self):
        """Dynamic ensemble doesn't need a separate model"""
        return None

    def _prepare_features(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Features are handled by individual models"""
        return X

    def _prepare_targets(self, y: Union[pd.Series, np.ndarray]) -> np.ndarray:
        """Targets are handled by individual models"""
        if isinstance(y, pd.Series):
            return y.values
        return y

    def update_performance(
        self, model_id: str, actual: np.ndarray, predicted: np.ndarray
    ):
        """Update performance history for a model"""
        if model_id not in self.performance_history:
            return

        # Calculate performance metric
        if len(actual) == len(predicted):
            if isinstance(predicted[0], (int, str)):  # Classification
                performance = accuracy_score(actual, predicted)
            else:  # Regression
                performance = r2_score(actual, predicted)

            # Add to performance history
            self.performance_history[model_id].append(performance)

            # Keep only recent performance
            if len(self.performance_history[model_id]) > self.performance_window:
                self.performance_history[model_id].pop(0)

            # Update weights based on recent performance
            self._update_weights()

    def _update_weights(self):
        """Update model weights based on recent performance"""
        if not self.models:
            return

        # Calculate average recent performance for each model
        avg_performance = {}
        for model_id in self.performance_history:
            if self.performance_history[model_id]:
                avg_performance[model_id] = np.mean(self.performance_history[model_id])
            else:
                avg_performance[model_id] = 0.5  # Default performance

        # Normalize weights based on performance
        total_performance = sum(avg_performance.values())
        if total_performance > 0:
            for model_id in avg_performance:
                self.adaptive_weights[model_id] = (
                    avg_performance[model_id] / total_performance
                )

        logger.info(f"Updated weights: {self.adaptive_weights}")

    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> PredictionResult:
        """Make dynamic ensemble predictions"""
        if not self.models:
            raise RuntimeError("No models in dynamic ensemble")

        prediction_start = datetime.now()

        try:
            # Get predictions from all models
            all_predictions = []
            for model in self.models:
                pred_result = model.predict(X)
                predictions = pred_result.predictions

                # Handle different prediction formats
                if isinstance(predictions, np.ndarray):
                    if predictions.ndim == 1:
                        all_predictions.append(predictions)
                    else:
                        all_predictions.append(predictions[:, 0])
                else:
                    all_predictions.append(np.array(predictions))

            # Calculate weighted average using adaptive weights
            weighted_pred = np.zeros_like(all_predictions[0])
            total_weight = 0

            for i, model in enumerate(self.models):
                weight = self.adaptive_weights.get(model.model_id, 1.0)
                weighted_pred += weight * all_predictions[i]
                total_weight += weight

            if total_weight > 0:
                weighted_pred /= total_weight

            # Calculate processing time
            processing_time = (datetime.now() - prediction_start).total_seconds()

            # Create prediction result
            result = PredictionResult(
                prediction_id=f"{self.model_id}_{prediction_start.strftime('%Y%m%d_%H%M%S')}",
                model_id=self.model_id,
                timestamp=prediction_start,
                predictions=weighted_pred,
                input_features=X.to_dict() if hasattr(X, "to_dict") else None,
                feature_names=[m.model_id for m in self.models],
                prediction_type=self.model_type.value,
                processing_time=processing_time,
            )

            return result

        except Exception as e:
            logger.error(f"Dynamic ensemble prediction failed for {self.model_id}: {e}")
            raise

    def get_dynamic_analysis(self) -> Dict[str, Any]:
        """Get comprehensive dynamic ensemble analysis"""
        analysis = {
            "model_count": len(self.models),
            "models": [],
            "current_weights": self.adaptive_weights.copy(),
            "performance_summary": {},
            "adaptation_history": {},
        }

        # Analyze each model
        for model in self.models:
            model_info = {
                "model_id": model.model_id,
                "name": model.name,
                "type": model.model_type.value,
                "current_weight": self.adaptive_weights.get(model.model_id, 0.0),
                "recent_performance": self.performance_history.get(model.model_id, []),
            }
            analysis["models"].append(model_info)

        # Performance summary
        if self.models:
            analysis["performance_summary"] = {
                "best_performing_model": max(
                    self.adaptive_weights.items(), key=lambda x: x[1]
                )[0],
                "weight_variance": np.var(list(self.adaptive_weights.values())),
                "adaptation_active": any(
                    len(hist) > 0 for hist in self.performance_history.values()
                ),
            }

        return analysis
