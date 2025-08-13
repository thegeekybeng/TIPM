"""
Advanced Time Series Forecasters for TIPM
========================================

LSTM-based forecasting models for GDP impact, trade flows, employment,
and price impacts with enterprise-grade quality and performance.
"""

import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Deep Learning Libraries
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None
    nn = None
    optim = None
    DataLoader = None
    TensorDataset = None

# Time Series Libraries
try:
    from sklearn.preprocessing import MinMaxScaler, StandardScaler
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    MinMaxScaler = None
    StandardScaler = None

# Base classes
from .base import BaseMLModel, ModelType, PredictionResult, ModelStatus

logger = logging.getLogger(__name__)


class LSTMNetwork(nn.Module):
    """Advanced LSTM network for time series forecasting"""

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        num_layers: int,
        output_size: int,
        dropout: float = 0.2,
    ):
        super(LSTMNetwork, self).__init__()

        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # LSTM layers
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
            bidirectional=False,
        )

        # Attention mechanism
        self.attention = nn.MultiheadAttention(
            embed_dim=hidden_size, num_heads=4, dropout=dropout
        )

        # Output layers
        self.fc1 = nn.Linear(hidden_size, hidden_size // 2)
        self.dropout = nn.Dropout(dropout)
        self.fc2 = nn.Linear(hidden_size // 2, output_size)
        self.relu = nn.ReLU()

    def forward(self, x):
        # LSTM forward pass
        lstm_out, _ = self.lstm(x)

        # Apply attention
        attn_out, _ = self.attention(lstm_out, lstm_out, lstm_out)

        # Take last output and apply final layers
        out = self.fc1(attn_out[:, -1, :])
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc2(out)

        return out


class BaseTimeSeriesForecaster(BaseMLModel):
    """Base class for time series forecasting models"""

    def __init__(
        self,
        model_id: str,
        name: str,
        description: str,
        sequence_length: int = 12,
        forecast_horizon: int = 6,
    ):
        super().__init__(
            model_id=model_id,
            name=name,
            description=description,
            model_type=ModelType.TIME_SERIES,
        )

        # Time series configuration
        self.sequence_length = sequence_length
        self.forecast_horizon = forecast_horizon

        # Data preprocessing
        self.scaler = None
        self.feature_scaler = None

        # Model state
        self._model = None
        self._device = None

        # Training configuration
        self.hyperparameters = {
            "hidden_size": 128,
            "num_layers": 3,
            "learning_rate": 0.001,
            "batch_size": 32,
            "epochs": 100,
            "dropout": 0.2,
            "patience": 10,
        }

        logger.info(f"Initialized {name}: {model_id}")

    def _create_model(self):
        """Create the LSTM model"""
        if not TORCH_AVAILABLE:
            raise RuntimeError("PyTorch is required for LSTM models")

        # Determine input size (features + time features)
        input_size = self._get_input_size()

        model = LSTMNetwork(
            input_size=input_size,
            hidden_size=self.hyperparameters["hidden_size"],
            num_layers=self.hyperparameters["num_layers"],
            output_size=self.forecast_horizon,
            dropout=self.hyperparameters["dropout"],
        )

        return model

    def _get_input_size(self) -> int:
        """Get input size for the model"""
        # Base features + time features
        base_features = getattr(self, "_feature_count", 1)
        time_features = 4  # year, month, quarter, day_of_week
        return base_features + time_features

    def _prepare_features(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Prepare features for time series forecasting"""
        if isinstance(X, pd.DataFrame):
            # Handle time index
            if hasattr(X, "index") and isinstance(X.index, pd.DatetimeIndex):
                X = self._add_time_features(X)

            # Convert to numpy
            X = X.values

        # Ensure 3D shape for LSTM: (samples, sequence_length, features)
        if X.ndim == 2:
            X = self._create_sequences(X)

        return X.astype(np.float32)

    def _prepare_targets(self, y: Union[pd.Series, np.ndarray]) -> np.ndarray:
        """Prepare target variables for time series forecasting"""
        if isinstance(y, pd.Series):
            y = y.values

        # Create sequences for targets
        y_sequences = self._create_target_sequences(y)
        return y_sequences.astype(np.float32)

    def _add_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add time-based features to the dataframe"""
        df = df.copy()

        # Extract time components
        df["year"] = df.index.year
        df["month"] = df.index.month
        df["quarter"] = df.index.quarter
        df["day_of_week"] = df.index.dayofweek

        return df

    def _create_sequences(self, data: np.ndarray) -> np.ndarray:
        """Create sliding window sequences for LSTM"""
        sequences = []
        for i in range(len(data) - self.sequence_length + 1):
            sequences.append(data[i : i + self.sequence_length])
        return np.array(sequences)

    def _create_target_sequences(self, data: np.ndarray) -> np.ndarray:
        """Create target sequences for forecasting"""
        targets = []
        for i in range(self.sequence_length, len(data) - self.forecast_horizon + 1):
            targets.append(data[i : i + self.forecast_horizon])
        return np.array(targets)

    def fit(
        self,
        X: Union[pd.DataFrame, np.ndarray],
        y: Union[pd.Series, np.ndarray],
        **kwargs,
    ) -> "BaseTimeSeriesForecaster":
        """Train the time series forecasting model"""
        training_start = datetime.now()

        try:
            logger.info(f"Starting training for {self.model_id}")
            self.metadata.status = ModelStatus.TRAINING

            # Prepare data
            X_prepared = self._prepare_features(X)
            y_prepared = self._prepare_targets(y)

            # Update metadata
            self.metadata.feature_count = X_prepared.shape[2]
            self.metadata.sample_count = X_prepared.shape[0]

            # Create and train model
            self._model = self._create_model()
            self._train_lstm_model(X_prepared, y_prepared, **kwargs)

            # Update status
            self._is_trained = True
            self.metadata.status = ModelStatus.TRAINED
            self.metadata.last_trained = datetime.now()

            # Calculate training score
            training_score = self._calculate_training_score(X_prepared, y_prepared)
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

            logger.info(f"Training completed for {self.model_id}")
            return self

        except Exception as e:
            self.metadata.status = ModelStatus.FAILED
            logger.error(f"Training failed for {self.model_id}: {e}")
            raise

    def _train_lstm_model(self, X: np.ndarray, y: np.ndarray, **kwargs):
        """Train the LSTM model with advanced techniques"""
        # Set device
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._model.to(self._device)

        # Convert to tensors
        X_tensor = torch.FloatTensor(X).to(self._device)
        y_tensor = torch.FloatTensor(y).to(self._device)

        # Create data loader
        dataset = TensorDataset(X_tensor, y_tensor)
        dataloader = DataLoader(
            dataset, batch_size=self.hyperparameters["batch_size"], shuffle=True
        )

        # Loss and optimizer
        criterion = nn.MSELoss()
        optimizer = optim.Adam(
            self._model.parameters(), lr=self.hyperparameters["learning_rate"]
        )

        # Learning rate scheduler
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode="min", patience=5, factor=0.5
        )

        # Training loop with early stopping
        best_loss = float("inf")
        patience_counter = 0
        loss_history = []

        for epoch in range(self.hyperparameters["epochs"]):
            self._model.train()
            total_loss = 0

            for batch_X, batch_y in dataloader:
                optimizer.zero_grad()
                outputs = self._model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()

            avg_loss = total_loss / len(dataloader)
            loss_history.append(avg_loss)

            # Learning rate scheduling
            scheduler.step(avg_loss)

            # Early stopping
            if avg_loss < best_loss:
                best_loss = avg_loss
                patience_counter = 0
            else:
                patience_counter += 1

            if patience_counter >= self.hyperparameters["patience"]:
                logger.info(f"Early stopping at epoch {epoch}")
                break

            if epoch % 10 == 0:
                logger.info(f"Epoch {epoch}, Loss: {avg_loss:.6f}")

        # Update training result
        if self.training_history:
            self.training_history[-1].loss_history = loss_history
            self.training_history[-1].epochs = epoch + 1
            self.training_history[-1].learning_rate = self.hyperparameters[
                "learning_rate"
            ]

    def _calculate_training_score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Calculate training score (R² for regression)"""
        self._model.eval()
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self._device)
            y_pred = self._model(X_tensor).cpu().numpy()
            return r2_score(y.flatten(), y_pred.flatten())

    def predict(self, X: Union[pd.DataFrame, np.ndarray]) -> PredictionResult:
        """Make time series forecasts"""
        if not self._is_trained:
            raise RuntimeError(
                f"Model {self.model_id} must be trained before forecasting"
            )

        prediction_start = datetime.now()

        try:
            # Prepare features
            X_prepared = self._prepare_features(X)

            # Make predictions
            self._model.eval()
            with torch.no_grad():
                X_tensor = torch.FloatTensor(X_prepared).to(self._device)
                predictions = self._model(X_tensor).cpu().numpy()

            # Calculate processing time
            processing_time = (datetime.now() - prediction_start).total_seconds()

            # Create prediction result
            result = PredictionResult(
                prediction_id=f"{self.model_id}_{prediction_start.strftime('%Y%m%d_%H%M%S')}",
                model_id=self.model_id,
                timestamp=prediction_start,
                predictions=predictions,
                input_features=X.to_dict() if hasattr(X, "to_dict") else None,
                feature_names=getattr(self, "_feature_names", None),
                prediction_type=self.model_type.value,
                processing_time=processing_time,
            )

            return result

        except Exception as e:
            logger.error(f"Forecasting failed for {self.model_id}: {e}")
            raise

    def forecast_future(self, steps: int, last_sequence: np.ndarray) -> np.ndarray:
        """Forecast future values beyond training data"""
        if not self._is_trained:
            raise RuntimeError("Model must be trained before forecasting")

        self._model.eval()
        forecasts = []
        current_sequence = last_sequence.copy()

        with torch.no_grad():
            for _ in range(steps):
                # Prepare input
                X_input = (
                    torch.FloatTensor(current_sequence).unsqueeze(0).to(self._device)
                )

                # Get prediction
                pred = self._model(X_input).cpu().numpy()[0]
                forecasts.append(pred)

                # Update sequence for next prediction
                current_sequence = np.roll(current_sequence, -1, axis=0)
                current_sequence[-1] = pred

        return np.array(forecasts)


class GDPImpactForecaster(BaseTimeSeriesForecaster):
    """LSTM forecaster for GDP impact predictions"""

    def __init__(self, model_id: str = "gdp_impact_forecaster"):
        super().__init__(
            model_id=model_id,
            name="GDP Impact Forecaster",
            description="LSTM-based forecaster for predicting GDP impacts from tariff policies",
            sequence_length=24,  # 2 years of monthly data
            forecast_horizon=12,  # 1 year forecast
        )

        # GDP-specific configuration
        self.hyperparameters.update(
            {
                "hidden_size": 256,
                "num_layers": 4,
                "learning_rate": 0.0005,
                "epochs": 150,
            }
        )

        logger.info(f"Initialized GDPImpactForecaster: {model_id}")

    def get_gdp_forecast(self, X: Union[pd.DataFrame, np.ndarray]) -> Dict[str, Any]:
        """Get comprehensive GDP impact forecast"""
        prediction_result = self.predict(X)

        forecast = {
            "predictions": prediction_result.predictions.tolist(),
            "forecast_horizon": self.forecast_horizon,
            "confidence_intervals": self._calculate_confidence_intervals(
                prediction_result.predictions
            ),
            "economic_indicators": self._analyze_gdp_indicators(
                prediction_result.predictions
            ),
            "policy_implications": self._generate_policy_implications(
                prediction_result.predictions
            ),
        }

        return forecast

    def _calculate_confidence_intervals(
        self, predictions: np.ndarray
    ) -> Dict[str, List[float]]:
        """Calculate confidence intervals for GDP forecasts"""
        # Simple confidence intervals based on historical variance
        # In production, use more sophisticated methods like conformal prediction

        confidence_levels = [0.68, 0.95, 0.99]  # 1σ, 2σ, 3σ
        intervals = {}

        for level in confidence_levels:
            if level == 0.68:
                multiplier = 1.0
            elif level == 0.95:
                multiplier = 1.96
            else:  # 0.99
                multiplier = 2.58

            # Calculate intervals (simplified)
            lower = predictions * (1 - 0.05 * multiplier)
            upper = predictions * (1 + 0.05 * multiplier)

            intervals[f"{int(level*100)}%_lower"] = lower.tolist()
            intervals[f"{int(level*100)}%_upper"] = upper.tolist()

        return intervals

    def _analyze_gdp_indicators(self, predictions: np.ndarray) -> Dict[str, Any]:
        """Analyze GDP indicators from forecasts"""
        # Calculate growth rates
        growth_rates = np.diff(predictions) / predictions[:-1] * 100

        # Analyze trends
        trend = "Growing" if np.mean(growth_rates) > 0 else "Declining"
        volatility = np.std(growth_rates)

        # Identify turning points
        turning_points = []
        for i in range(1, len(growth_rates) - 1):
            if (
                growth_rates[i - 1] < growth_rates[i] > growth_rates[i + 1]
                or growth_rates[i - 1] > growth_rates[i] < growth_rates[i + 1]
            ):
                turning_points.append(i + 1)  # +1 because of diff

        return {
            "trend": trend,
            "average_growth_rate": float(np.mean(growth_rates)),
            "volatility": float(volatility),
            "turning_points": turning_points,
            "growth_acceleration": float(np.mean(np.diff(growth_rates))),
        }

    def _generate_policy_implications(self, predictions: np.ndarray) -> List[str]:
        """Generate policy implications from GDP forecasts"""
        implications = []

        # Analyze growth trajectory
        if np.all(np.diff(predictions) > 0):
            implications.append(
                "Sustained GDP growth expected - maintain current policies"
            )
        elif np.any(np.diff(predictions) < 0):
            implications.append("GDP contraction possible - consider stimulus measures")

        # Analyze growth rate changes
        growth_changes = np.diff(np.diff(predictions))
        if np.any(growth_changes < 0):
            implications.append(
                "Growth deceleration detected - monitor economic indicators"
            )

        # Volatility assessment
        if np.std(np.diff(predictions)) > np.mean(np.diff(predictions)) * 0.5:
            implications.append(
                "High GDP volatility expected - implement stabilization measures"
            )

        return implications


class TradeFlowForecaster(BaseTimeSeriesForecaster):
    """LSTM forecaster for trade flow predictions"""

    def __init__(self, model_id: str = "trade_flow_forecaster"):
        super().__init__(
            model_id=model_id,
            name="Trade Flow Forecaster",
            description="LSTM-based forecaster for predicting trade flow impacts from tariffs",
            sequence_length=18,  # 1.5 years of monthly data
            forecast_horizon=6,  # 6 months forecast
        )

        # Trade-specific configuration
        self.hyperparameters.update(
            {"hidden_size": 192, "num_layers": 3, "learning_rate": 0.001, "epochs": 120}
        )

        logger.info(f"Initialized TradeFlowForecaster: {model_id}")

    def get_trade_forecast(self, X: Union[pd.DataFrame, np.ndarray]) -> Dict[str, Any]:
        """Get comprehensive trade flow forecast"""
        prediction_result = self.predict(X)

        forecast = {
            "predictions": prediction_result.predictions.tolist(),
            "forecast_horizon": self.forecast_horizon,
            "trade_balance_analysis": self._analyze_trade_balance(
                prediction_result.predictions
            ),
            "sector_impacts": self._analyze_sector_impacts(
                prediction_result.predictions
            ),
            "policy_recommendations": self._generate_trade_policy_recommendations(
                prediction_result.predictions
            ),
        }

        return forecast

    def _analyze_trade_balance(self, predictions: np.ndarray) -> Dict[str, Any]:
        """Analyze trade balance from forecasts"""
        # Assuming predictions include imports and exports
        if predictions.shape[1] >= 2:
            imports = predictions[:, 0]
            exports = predictions[:, 1]
            balance = exports - imports

            return {
                "trade_balance": balance.tolist(),
                "balance_trend": (
                    "Improving" if np.all(np.diff(balance) > 0) else "Deteriorating"
                ),
                "average_balance": float(np.mean(balance)),
                "balance_volatility": float(np.std(balance)),
            }
        else:
            return {"error": "Insufficient data for trade balance analysis"}

    def _analyze_sector_impacts(self, predictions: np.ndarray) -> Dict[str, Any]:
        """Analyze sector-specific impacts"""
        # This would be enhanced with actual sector data
        return {
            "manufacturing": "Moderate impact expected",
            "agriculture": "High sensitivity to trade policy changes",
            "services": "Limited direct impact",
            "technology": "Varies by export dependency",
        }

    def _generate_trade_policy_recommendations(
        self, predictions: np.ndarray
    ) -> List[str]:
        """Generate trade policy recommendations"""
        recommendations = []

        # Analyze trade volume trends
        if np.all(np.diff(predictions.sum(axis=1)) > 0):
            recommendations.append(
                "Trade volume growing - maintain open trade policies"
            )
        else:
            recommendations.append("Trade volume declining - review trade restrictions")

        # Analyze balance trends
        if predictions.shape[1] >= 2:
            balance = predictions[:, 1] - predictions[:, 0]  # exports - imports
            if np.any(balance < 0):
                recommendations.append(
                    "Trade deficit detected - consider export promotion"
                )

        return recommendations


class EmploymentForecaster(BaseTimeSeriesForecaster):
    """LSTM forecaster for employment impact predictions"""

    def __init__(self, model_id: str = "employment_forecaster"):
        super().__init__(
            model_id=model_id,
            name="Employment Impact Forecaster",
            description="LSTM-based forecaster for predicting employment impacts from tariff policies",
            sequence_length=36,  # 3 years of monthly data
            forecast_horizon=12,  # 1 year forecast
        )

        # Employment-specific configuration
        self.hyperparameters.update(
            {"hidden_size": 128, "num_layers": 3, "learning_rate": 0.001, "epochs": 100}
        )

        logger.info(f"Initialized EmploymentForecaster: {model_id}")


class PriceImpactForecaster(BaseTimeSeriesForecaster):
    """LSTM forecaster for price impact predictions"""

    def __init__(self, model_id: str = "price_impact_forecaster"):
        super().__init__(
            model_id=model_id,
            name="Price Impact Forecaster",
            description="LSTM-based forecaster for predicting price impacts from tariff policies",
            sequence_length=24,  # 2 years of monthly data
            forecast_horizon=6,  # 6 months forecast
        )

        # Price-specific configuration
        self.hyperparameters.update(
            {"hidden_size": 160, "num_layers": 3, "learning_rate": 0.001, "epochs": 120}
        )

        logger.info(f"Initialized PriceImpactForecaster: {model_id}")
