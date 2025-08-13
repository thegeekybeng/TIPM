"""
Base ML Model Classes for TIPM
==============================

Foundation classes and interfaces for all ML models in the TIPM system.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.metrics import classification_report, mean_squared_error, r2_score

logger = logging.getLogger(__name__)


class ModelType(Enum):
    """Types of ML models supported by TIPM"""

    # Classification models
    CLASSIFICATION = "classification"
    MULTI_CLASS = "multi_class"
    BINARY = "binary"

    # Regression models
    REGRESSION = "regression"
    TIME_SERIES = "time_series"

    # Forecasting models
    FORECASTING = "forecasting"
    SEQUENCE = "sequence"

    # Anomaly detection
    ANOMALY_DETECTION = "anomaly_detection"
    OUTLIER_DETECTION = "outlier_detection"

    # Ensemble models
    ENSEMBLE = "ensemble"
    VOTING = "voting"
    STACKING = "stacking"

    # Deep learning
    NEURAL_NETWORK = "neural_network"
    LSTM = "lstm"
    TRANSFORMER = "transformer"


class ModelStatus(Enum):
    """Model training and deployment status"""

    NOT_TRAINED = "not_trained"
    TRAINING = "training"
    TRAINED = "trained"
    VALIDATING = "validating"
    VALIDATED = "validated"
    DEPLOYED = "deployed"
    FAILED = "failed"
    DEPRECATED = "deprecated"


@dataclass
class ModelMetadata:
    """Metadata for ML models"""

    model_id: str
    name: str
    description: str
    model_type: ModelType
    version: str = "1.0.0"

    # Training information
    created_at: datetime = field(default_factory=datetime.now)
    last_trained: Optional[datetime] = None
    training_duration: Optional[float] = None  # seconds

    # Performance metrics
    training_score: Optional[float] = None
    validation_score: Optional[float] = None
    test_score: Optional[float] = None

    # Model characteristics
    feature_count: int = 0
    sample_count: int = 0
    hyperparameters: Dict[str, Any] = field(default_factory=dict)

    # Status and deployment
    status: ModelStatus = ModelStatus.NOT_TRAINED
    is_deployed: bool = False
    deployment_date: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "model_id": self.model_id,
            "name": self.name,
            "description": self.description,
            "model_type": self.model_type.value,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "last_trained": (
                self.last_trained.isoformat() if self.last_trained else None
            ),
            "training_duration": self.training_duration,
            "training_score": self.training_score,
            "validation_score": self.validation_score,
            "test_score": self.test_score,
            "feature_count": self.feature_count,
            "sample_count": self.sample_count,
            "hyperparameters": self.hyperparameters,
            "status": self.status.value,
            "is_deployed": self.is_deployed,
            "deployment_date": (
                self.deployment_date.isoformat() if self.deployment_date else None
            ),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModelMetadata":
        """Create from dictionary"""
        return cls(
            model_id=data["model_id"],
            name=data["name"],
            description=data["description"],
            model_type=ModelType(data["model_type"]),
            version=data.get("version", "1.0.0"),
            created_at=(
                datetime.fromisoformat(data["created_at"])
                if data.get("created_at")
                else datetime.now()
            ),
            last_trained=(
                datetime.fromisoformat(data["last_trained"])
                if data.get("last_trained")
                else None
            ),
            training_duration=data.get("training_duration"),
            training_score=data.get("training_score"),
            validation_score=data.get("validation_score"),
            test_score=data.get("test_score"),
            feature_count=data.get("feature_count", 0),
            sample_count=data.get("sample_count", 0),
            hyperparameters=data.get("hyperparameters", {}),
            status=ModelStatus(data.get("status", "not_trained")),
            is_deployed=data.get("is_deployed", False),
            deployment_date=(
                datetime.fromisoformat(data["deployment_date"])
                if data.get("deployment_date")
                else None
            ),
        )


@dataclass
class PredictionResult:
    """Result of a model prediction"""

    prediction_id: str
    model_id: str
    timestamp: datetime

    # Prediction outputs
    predictions: Union[np.ndarray, List, float]
    probabilities: Optional[np.ndarray] = None
    confidence_scores: Optional[np.ndarray] = None

    # Input features
    input_features: Optional[Dict[str, Any]] = None
    feature_names: Optional[List[str]] = None

    # Metadata
    prediction_type: str = "unknown"
    processing_time: Optional[float] = None  # seconds

    # Quality indicators
    confidence_threshold: float = 0.5
    is_high_confidence: bool = False

    def __post_init__(self):
        """Post-initialization processing"""
        if self.probabilities is not None and self.confidence_scores is None:
            # Calculate confidence scores from probabilities
            if isinstance(self.probabilities, np.ndarray):
                self.confidence_scores = (
                    np.max(self.probabilities, axis=1)
                    if self.probabilities.ndim > 1
                    else self.probabilities
                )
            else:
                self.confidence_scores = np.array(
                    [
                        max(p) if isinstance(p, (list, np.ndarray)) else p
                        for p in self.probabilities
                    ]
                )

        # Determine high confidence predictions
        if self.confidence_scores is not None:
            if isinstance(self.confidence_scores, np.ndarray):
                self.is_high_confidence = np.all(
                    self.confidence_scores >= self.confidence_threshold
                )
            else:
                self.is_high_confidence = (
                    self.confidence_scores >= self.confidence_threshold
                )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "prediction_id": self.prediction_id,
            "model_id": self.model_id,
            "timestamp": self.timestamp.isoformat(),
            "predictions": (
                self.predictions.tolist()
                if isinstance(self.predictions, np.ndarray)
                else self.predictions
            ),
            "probabilities": (
                self.probabilities.tolist()
                if isinstance(self.probabilities, np.ndarray)
                else self.probabilities
            ),
            "confidence_scores": (
                self.confidence_scores.tolist()
                if isinstance(self.confidence_scores, np.ndarray)
                else self.confidence_scores
            ),
            "input_features": self.input_features,
            "feature_names": self.feature_names,
            "prediction_type": self.prediction_type,
            "processing_time": self.processing_time,
            "confidence_threshold": self.confidence_threshold,
            "is_high_confidence": self.is_high_confidence,
        }


@dataclass
class TrainingResult:
    """Result of model training"""

    model_id: str
    training_start: datetime
    training_end: datetime

    # Training metrics
    training_score: float
    validation_score: float
    test_score: Optional[float] = None

    # Training details
    epochs: Optional[int] = None
    batch_size: Optional[int] = None
    learning_rate: Optional[float] = None

    # Performance metrics
    loss_history: Optional[List[float]] = None
    accuracy_history: Optional[List[float]] = None

    # Model characteristics
    model_size_mb: Optional[float] = None
    parameters_count: Optional[int] = None

    # Quality indicators
    overfitting_detected: bool = False
    convergence_achieved: bool = True

    @property
    def training_duration(self) -> float:
        """Calculate training duration in seconds"""
        return (self.training_end - self.training_start).total_seconds()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "model_id": self.model_id,
            "training_start": self.training_start.isoformat(),
            "training_end": self.training_end.isoformat(),
            "training_duration": self.training_duration,
            "training_score": self.training_score,
            "validation_score": self.validation_score,
            "test_score": self.test_score,
            "epochs": self.epochs,
            "batch_size": self.batch_size,
            "learning_rate": self.learning_rate,
            "loss_history": self.loss_history,
            "accuracy_history": self.accuracy_history,
            "model_size_mb": self.model_size_mb,
            "parameters_count": self.parameters_count,
            "overfitting_detected": self.overfitting_detected,
            "convergence_achieved": self.convergence_achieved,
        }


class BaseMLModel(ABC, BaseEstimator):
    """
    Base class for all ML models in TIPM

    Provides common interface and functionality for training, prediction,
    and model management.
    """

    def __init__(
        self, model_id: str, name: str, description: str, model_type: ModelType
    ):
        """
        Initialize base ML model

        Args:
            model_id: Unique identifier for the model
            name: Human-readable name
            description: Model description
            model_type: Type of ML model
        """
        self.model_id = model_id
        self.name = name
        self.description = description
        self.model_type = model_type

        # Initialize metadata
        self.metadata = ModelMetadata(
            model_id=model_id, name=name, description=description, model_type=model_type
        )

        # Model state
        self._model = None
        self._is_trained = False
        self._feature_names = None
        self._target_names = None

        # Training history
        self.training_history: List[TrainingResult] = []

        logger.info(f"Initialized {model_type.value} model: {name} ({model_id})")

    @abstractmethod
    def _create_model(self) -> Any:
        """
        Create the underlying ML model

        Returns:
            The ML model instance
        """
        pass

    @abstractmethod
    def _prepare_features(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """
        Prepare features for the model

        Args:
            X: Input features

        Returns:
            Prepared features array
        """
        pass

    @abstractmethod
    def _prepare_targets(self, y: Union[pd.Series, np.ndarray]) -> np.ndarray:
        """
        Prepare target variables for the model

        Args:
            y: Target variables

        Returns:
            Prepared targets array
        """
        pass

    def fit(
        self,
        X: Union[pd.DataFrame, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        **kwargs,
    ) -> "BaseMLModel":
        """
        Train the model

        Args:
            X: Training features
            y: Training targets
            **kwargs: Additional training parameters

        Returns:
            Self for method chaining
        """
        training_start = datetime.now()

        try:
            logger.info(f"Starting training for model {self.model_id}")

            # Update status
            self.metadata.status = ModelStatus.TRAINING

            # Store feature and target names
            if hasattr(X, "columns"):
                self._feature_names = list(X.columns)
            if hasattr(y, "name"):
                self._target_names = [y.name]

            # Prepare data
            X_prepared = self._prepare_features(X)
            y_prepared = self._prepare_targets(y)

            # Create and train model
            self._model = self._create_model()
            self._model.fit(X_prepared, y_prepared, **kwargs)

            # Update metadata
            self._is_trained = True
            self.metadata.status = ModelStatus.TRAINED
            self.metadata.last_trained = datetime.now()
            self.metadata.feature_count = X_prepared.shape[1]
            self.metadata.sample_count = X_prepared.shape[0]

            # Calculate training score
            training_score = (
                self._model.score(X_prepared, y_prepared)
                if hasattr(self._model, "score")
                else None
            )
            self.metadata.training_score = training_score

            # Create training result
            training_result = TrainingResult(
                model_id=self.model_id,
                training_start=training_start,
                training_end=datetime.now(),
                training_score=training_score or 0.0,
                validation_score=0.0,  # Will be updated during validation
            )

            self.training_history.append(training_result)

            logger.info(f"Training completed for model {self.model_id}")
            return self

        except Exception as e:
            self.metadata.status = ModelStatus.FAILED
            logger.error(f"Training failed for model {self.model_id}: {e}")
            raise

    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> PredictionResult:
        """
        Make predictions using the trained model

        Args:
            X: Input features

        Returns:
            PredictionResult with predictions and metadata
        """
        if not self._is_trained:
            raise RuntimeError(
                f"Model {self.model_id} must be trained before making predictions"
            )

        prediction_start = datetime.now()

        try:
            # Prepare features
            X_prepared = self._prepare_features(X)

            # Make predictions
            predictions = self._model.predict(X_prepared)

            # Get probabilities if available
            probabilities = None
            if hasattr(self._model, "predict_proba"):
                probabilities = self._model.predict_proba(X_prepared)

            # Calculate processing time
            processing_time = (datetime.now() - prediction_start).total_seconds()

            # Create prediction result
            result = PredictionResult(
                prediction_id=f"{self.model_id}_{prediction_start.strftime('%Y%m%d_%H%M%S')}",
                model_id=self.model_id,
                timestamp=prediction_start,
                predictions=predictions,
                probabilities=probabilities,
                input_features=X.to_dict() if hasattr(X, "to_dict") else None,
                feature_names=self._feature_names,
                prediction_type=self.model_type.value,
                processing_time=processing_time,
            )

            return result

        except Exception as e:
            logger.error(f"Prediction failed for model {self.model_id}: {e}")
            raise

    def validate(
        self,
        X_val: Union[pd.DataFrame, np.ndarray],
        y_val: Union[pd.Series, np.ndarray],
    ) -> float:
        """
        Validate the model on validation data

        Args:
            X_val: Validation features
            y_val: Validation targets

        Returns:
            Validation score
        """
        if not self._is_trained:
            raise RuntimeError(
                f"Model {self.model_id} must be trained before validation"
            )

        try:
            # Prepare data
            X_val_prepared = self._prepare_features(X_val)
            y_val_prepared = self._prepare_targets(y_val)

            # Make predictions
            y_pred = self._model.predict(X_val_prepared)

            # Calculate validation score
            if self.model_type in [
                ModelType.CLASSIFICATION,
                ModelType.MULTI_CLASS,
                ModelType.BINARY,
            ]:
                validation_score = self._model.score(X_val_prepared, y_val_prepared)
            else:
                validation_score = r2_score(y_val_prepared, y_pred)

            # Update metadata
            self.metadata.validation_score = validation_score

            # Update latest training result
            if self.training_history:
                self.training_history[-1].validation_score = validation_score

            logger.info(
                f"Validation completed for model {self.model_id}: {validation_score:.4f}"
            )
            return validation_score

        except Exception as e:
            logger.error(f"Validation failed for model {self.model_id}: {e}")
            raise

    def evaluate(
        self,
        X_test: Union[pd.DataFrame, np.ndarray],
        y_test: Union[pd.Series, np.ndarray],
    ) -> Dict[str, Any]:
        """
        Evaluate the model on test data

        Args:
            X_test: Test features
            y_test: Test targets

        Returns:
            Dictionary with evaluation metrics
        """
        if not self._is_trained:
            raise RuntimeError(
                f"Model {self.model_id} must be trained before evaluation"
            )

        try:
            # Prepare data
            X_test_prepared = self._prepare_features(X_test)
            y_test_prepared = self._prepare_targets(y_test)

            # Make predictions
            y_pred = self._model.predict(X_test_prepared)

            # Calculate metrics
            if self.model_type in [
                ModelType.CLASSIFICATION,
                ModelType.MULTI_CLASS,
                ModelType.BINARY,
            ]:
                # Classification metrics
                metrics = {
                    "accuracy": self._model.score(X_test_prepared, y_test_prepared),
                    "classification_report": classification_report(
                        y_test_prepared, y_pred, output_dict=True
                    ),
                }
            else:
                # Regression metrics
                metrics = {
                    "r2_score": r2_score(y_test_prepared, y_pred),
                    "mse": mean_squared_error(y_test_prepared, y_pred),
                    "rmse": np.sqrt(mean_squared_error(y_test_prepared, y_pred)),
                }

            # Update metadata
            self.metadata.test_score = metrics.get("accuracy", metrics.get("r2_score"))

            # Update latest training result
            if self.training_history:
                self.training_history[-1].test_score = self.metadata.test_score

            logger.info(f"Evaluation completed for model {self.model_id}")
            return metrics

        except Exception as e:
            logger.error(f"Evaluation failed for model {self.model_id}: {e}")
            raise

    def save_model(self, filepath: Union[str, Path]) -> None:
        """
        Save the trained model to disk

        Args:
            filepath: Path to save the model
        """
        if not self._is_trained:
            raise RuntimeError(f"Model {self.model_id} must be trained before saving")

        try:
            filepath = Path(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # Save the model
            with open(filepath, "wb") as f:
                pickle.dump(self, f)

            # Save metadata separately
            metadata_path = filepath.with_suffix(".json")
            with open(metadata_path, "w") as f:
                json.dump(self.metadata.to_dict(), f, indent=2)

            logger.info(f"Model {self.model_id} saved to {filepath}")

        except Exception as e:
            logger.error(f"Failed to save model {self.model_id}: {e}")
            raise

    @classmethod
    def load_model(cls, filepath: Union[str, Path]) -> "BaseMLModel":
        """
        Load a trained model from disk

        Args:
            filepath: Path to the saved model

        Returns:
            Loaded model instance
        """
        try:
            filepath = Path(filepath)

            with open(filepath, "rb") as f:
                model = pickle.load(f)

            logger.info(f"Model {model.model_id} loaded from {filepath}")
            return model

        except Exception as e:
            logger.error(f"Failed to load model from {filepath}: {e}")
            raise

    def get_feature_importance(self) -> Optional[Dict[str, float]]:
        """
        Get feature importance scores if available

        Returns:
            Dictionary mapping feature names to importance scores, or None if not available
        """
        if not self._is_trained or self._feature_names is None:
            return None

        try:
            if hasattr(self._model, "feature_importances_"):
                importance_scores = self._model.feature_importances_
            elif hasattr(self._model, "coef_"):
                importance_scores = np.abs(self._model.coef_)
                if importance_scores.ndim > 1:
                    importance_scores = np.mean(importance_scores, axis=0)
            else:
                return None

            return dict(zip(self._feature_names, importance_scores))

        except Exception as e:
            logger.warning(
                f"Could not extract feature importance for model {self.model_id}: {e}"
            )
            return None

    def get_model_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the model

        Returns:
            Dictionary with model summary information
        """
        return {
            "model_id": self.model_id,
            "name": self.name,
            "description": self.description,
            "model_type": self.model_type.value,
            "status": self.metadata.status.value,
            "is_trained": self._is_trained,
            "feature_count": self.metadata.feature_count,
            "sample_count": self.metadata.sample_count,
            "training_score": self.metadata.training_score,
            "validation_score": self.metadata.validation_score,
            "test_score": self.metadata.test_score,
            "last_trained": (
                self.metadata.last_trained.isoformat()
                if self.metadata.last_trained
                else None
            ),
            "training_count": len(self.training_history),
        }

    def __repr__(self) -> str:
        """String representation of the model"""
        return f"{self.__class__.__name__}(model_id='{self.model_id}', name='{self.name}', type='{self.model_type.value}')"
