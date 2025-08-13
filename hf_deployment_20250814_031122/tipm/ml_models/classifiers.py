"""
Advanced Multi-Class Classifiers for TIPM
========================================

Specialized classifiers for tariff impact prediction, economic outcomes,
policy effectiveness, and industry vulnerability assessment.
"""

import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime
import numpy as np
import pandas as pd

# ML libraries
try:
    import xgboost as xgb

    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    xgb = None

try:
    import lightgbm as lgb

    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    lgb = None

try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.model_selection import cross_val_score, StratifiedKFold

    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    RandomForestClassifier = None
    GradientBoostingClassifier = None
    LogisticRegression = None
    StandardScaler = None
    LabelEncoder = None
    cross_val_score = None
    StratifiedKFold = None

# Base classes
from .base import BaseMLModel, ModelType, PredictionResult

logger = logging.getLogger(__name__)


class TariffImpactClassifier(BaseMLModel):
    """
    Multi-class classifier for predicting tariff impact severity

    Predicts: High/Medium/Low impact based on economic indicators,
    trade patterns, and policy characteristics.
    """

    def __init__(self, model_id: str = "tariff_impact_classifier"):
        super().__init__(
            model_id=model_id,
            name="Tariff Impact Severity Classifier",
            description="Multi-class classifier for predicting tariff impact severity (High/Medium/Low)",
            model_type=ModelType.MULTI_CLASS,
        )

        # Model configuration
        self.class_labels = ["Low", "Medium", "High"]
        self.feature_scaler = None
        self.label_encoder = None

        # Hyperparameters
        self.hyperparameters = {
            "n_estimators": 200,
            "max_depth": 6,
            "learning_rate": 0.1,
            "random_state": 42,
        }

        logger.info(f"Initialized TariffImpactClassifier: {model_id}")

    def _create_model(self):
        """Create the underlying ML model"""
        if XGBOOST_AVAILABLE:
            # XGBoost for best performance
            model = xgb.XGBClassifier(
                n_estimators=self.hyperparameters["n_estimators"],
                max_depth=self.hyperparameters["max_depth"],
                learning_rate=self.hyperparameters["learning_rate"],
                random_state=self.hyperparameters["random_state"],
                objective="multi:softprob",
                eval_metric="mlogloss",
            )
        elif LIGHTGBM_AVAILABLE:
            # LightGBM as alternative
            model = lgb.LGBMClassifier(
                n_estimators=self.hyperparameters["n_estimators"],
                max_depth=self.hyperparameters["max_depth"],
                learning_rate=self.hyperparameters["learning_rate"],
                random_state=self.hyperparameters["random_state"],
                objective="multiclass",
                metric="multi_logloss",
            )
        elif SKLEARN_AVAILABLE:
            # Gradient Boosting as fallback
            model = GradientBoostingClassifier(
                n_estimators=self.hyperparameters["n_estimators"],
                max_depth=self.hyperparameters["max_depth"],
                learning_rate=self.hyperparameters["learning_rate"],
                random_state=self.hyperparameters["random_state"],
            )
        else:
            raise RuntimeError(
                "No suitable ML library available. Install xgboost, lightgbm, or scikit-learn."
            )

        return model

    def _prepare_features(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Prepare features for classification"""
        if isinstance(X, pd.DataFrame):
            # Handle categorical features
            X_processed = X.copy()

            # Convert categorical columns to numerical
            for col in X_processed.select_dtypes(include=["object", "category"]):
                X_processed[col] = X_processed[col].astype("category").cat.codes

            # Fill missing values
            X_processed = X_processed.fillna(X_processed.mean())

            # Scale features
            if self.feature_scaler is None:
                self.feature_scaler = StandardScaler()
                X_scaled = self.feature_scaler.fit_transform(X_processed)
            else:
                X_scaled = self.feature_scaler.transform(X_processed)

            return X_scaled
        else:
            # Assume numpy array
            return X

    def _prepare_targets(self, y: Union[pd.Series, np.ndarray]) -> np.ndarray:
        """Prepare target variables for classification"""
        if self.label_encoder is None:
            self.label_encoder = LabelEncoder()
            y_encoded = self.label_encoder.fit_transform(y)
        else:
            y_encoded = self.label_encoder.transform(y)

        return y_encoded

    def predict_with_confidence(
        self, X: Union[pd.DataFrame, np.ndarray]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Make predictions with confidence scores"""
        if not self._is_trained:
            raise RuntimeError("Model must be trained before making predictions")

        X_prepared = self._prepare_features(X)

        # Get predictions and probabilities
        predictions = self._model.predict(X_prepared)
        probabilities = self._model.predict_proba(X_prepared)

        # Convert back to original labels
        if self.label_encoder is not None:
            predictions = self.label_encoder.inverse_transform(predictions)

        return predictions, probabilities

    def get_impact_analysis(self, X: Union[pd.DataFrame, np.ndarray]) -> Dict[str, Any]:
        """Get detailed impact analysis with confidence intervals"""
        predictions, probabilities = self.predict_with_confidence(X)

        analysis = {
            "predictions": (
                predictions.tolist()
                if isinstance(predictions, np.ndarray)
                else predictions
            ),
            "probabilities": (
                probabilities.tolist()
                if isinstance(probabilities, np.ndarray)
                else probabilities
            ),
            "confidence_scores": np.max(probabilities, axis=1).tolist(),
            "risk_assessment": [],
        }

        # Risk assessment for each prediction
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            confidence = np.max(prob)
            risk_level = (
                "High" if confidence < 0.6 else "Medium" if confidence < 0.8 else "Low"
            )

            analysis["risk_assessment"].append(
                {
                    "prediction": pred,
                    "confidence": confidence,
                    "risk_level": risk_level,
                    "class_probabilities": {
                        label: prob[j] for j, label in enumerate(self.class_labels)
                    },
                }
            )

        return analysis


class EconomicOutcomeClassifier(BaseMLModel):
    """
    Multi-class classifier for predicting economic outcomes

    Predicts: Recession/Growth/Stagnation based on economic indicators,
    policy changes, and market conditions.
    """

    def __init__(self, model_id: str = "economic_outcome_classifier"):
        super().__init__(
            model_id=model_id,
            name="Economic Outcome Classifier",
            description="Multi-class classifier for predicting economic outcomes (Recession/Growth/Stagnation)",
            model_type=ModelType.MULTI_CLASS,
        )

        # Model configuration
        self.class_labels = ["Recession", "Stagnation", "Growth"]
        self.feature_scaler = None
        self.label_encoder = None

        # Hyperparameters
        self.hyperparameters = {
            "n_estimators": 300,
            "max_depth": 8,
            "learning_rate": 0.05,
            "random_state": 42,
        }

        logger.info(f"Initialized EconomicOutcomeClassifier: {model_id}")

    def _create_model(self):
        """Create the underlying ML model"""
        if XGBOOST_AVAILABLE:
            model = xgb.XGBClassifier(
                n_estimators=self.hyperparameters["n_estimators"],
                max_depth=self.hyperparameters["max_depth"],
                learning_rate=self.hyperparameters["learning_rate"],
                random_state=self.hyperparameters["random_state"],
                objective="multi:softprob",
                eval_metric="mlogloss",
            )
        elif LIGHTGBM_AVAILABLE:
            model = lgb.LGBMClassifier(
                n_estimators=self.hyperparameters["n_estimators"],
                max_depth=self.hyperparameters["max_depth"],
                learning_rate=self.hyperparameters["learning_rate"],
                random_state=self.hyperparameters["random_state"],
                objective="multiclass",
                metric="multi_logloss",
            )
        elif SKLEARN_AVAILABLE:
            model = RandomForestClassifier(
                n_estimators=self.hyperparameters["n_estimators"],
                max_depth=self.hyperparameters["max_depth"],
                random_state=self.hyperparameters["random_state"],
            )
        else:
            raise RuntimeError("No suitable ML library available.")

        return model

    def _prepare_features(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Prepare features for classification"""
        if isinstance(X, pd.DataFrame):
            X_processed = X.copy()

            # Handle categorical features
            for col in X_processed.select_dtypes(include=["object", "category"]):
                X_processed[col] = X_processed[col].astype("category").cat.codes

            # Fill missing values
            X_processed = X_processed.fillna(X_processed.mean())

            # Scale features
            if self.feature_scaler is None:
                self.feature_scaler = StandardScaler()
                X_scaled = self.feature_scaler.fit_transform(X_processed)
            else:
                X_scaled = self.feature_scaler.transform(X_processed)

            return X_scaled
        else:
            return X

    def _prepare_targets(self, y: Union[pd.Series, np.ndarray]) -> np.ndarray:
        """Prepare target variables for classification"""
        if self.label_encoder is None:
            self.label_encoder = LabelEncoder()
            y_encoded = self.label_encoder.fit_transform(y)
        else:
            y_encoded = self.label_encoder.transform(y)

        return y_encoded

    def get_economic_forecast(
        self, X: Union[pd.DataFrame, np.ndarray]
    ) -> Dict[str, Any]:
        """Get economic forecast with detailed analysis"""
        predictions, probabilities = self.predict_with_confidence(X)

        forecast = {
            "predictions": (
                predictions.tolist()
                if isinstance(predictions, np.ndarray)
                else predictions
            ),
            "probabilities": (
                probabilities.tolist()
                if isinstance(probabilities, np.ndarray)
                else probabilities
            ),
            "economic_indicators": [],
            "policy_recommendations": [],
        }

        # Analyze each prediction
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            confidence = np.max(prob)

            # Economic indicators
            indicators = {
                "gdp_growth": (
                    "Negative"
                    if pred == "Recession"
                    else "Stable" if pred == "Stagnation" else "Positive"
                ),
                "inflation": (
                    "High"
                    if pred == "Recession"
                    else "Moderate" if pred == "Stagnation" else "Low"
                ),
                "unemployment": (
                    "High"
                    if pred == "Recession"
                    else "Moderate" if pred == "Stagnation" else "Low"
                ),
                "trade_balance": (
                    "Deficit"
                    if pred == "Recession"
                    else "Balanced" if pred == "Stagnation" else "Surplus"
                ),
            }

            # Policy recommendations
            if pred == "Recession":
                recommendations = [
                    "Implement expansionary fiscal policy",
                    "Lower interest rates",
                    "Increase government spending",
                    "Provide economic stimulus packages",
                ]
            elif pred == "Stagnation":
                recommendations = [
                    "Structural reforms",
                    "Investment incentives",
                    "Trade policy optimization",
                    "Infrastructure development",
                ]
            else:  # Growth
                recommendations = [
                    "Maintain current policies",
                    "Monitor inflation",
                    "Prepare for overheating",
                    "Sustainable growth measures",
                ]

            forecast["economic_indicators"].append(indicators)
            forecast["policy_recommendations"].append(recommendations)

        return forecast


class PolicyEffectivenessClassifier(BaseMLModel):
    """
    Multi-class classifier for predicting policy effectiveness

    Predicts: Effective/Partially Effective/Ineffective based on
    policy characteristics, implementation context, and historical data.
    """

    def __init__(self, model_id: str = "policy_effectiveness_classifier"):
        super().__init__(
            model_id=model_id,
            name="Policy Effectiveness Classifier",
            description="Multi-class classifier for predicting policy effectiveness (Effective/Partially Effective/Ineffective)",
            model_type=ModelType.MULTI_CLASS,
        )

        # Model configuration
        self.class_labels = ["Ineffective", "Partially Effective", "Effective"]
        self.feature_scaler = None
        self.label_encoder = None

        # Hyperparameters
        self.hyperparameters = {
            "n_estimators": 250,
            "max_depth": 7,
            "learning_rate": 0.08,
            "random_state": 42,
        }

        logger.info(f"Initialized PolicyEffectivenessClassifier: {model_id}")

    def _create_model(self):
        """Create the underlying ML model"""
        if XGBOOST_AVAILABLE:
            model = xgb.XGBClassifier(
                n_estimators=self.hyperparameters["n_estimators"],
                max_depth=self.hyperparameters["max_depth"],
                learning_rate=self.hyperparameters["learning_rate"],
                random_state=self.hyperparameters["random_state"],
                objective="multi:softprob",
                eval_metric="mlogloss",
            )
        elif LIGHTGBM_AVAILABLE:
            model = lgb.LGBMClassifier(
                n_estimators=self.hyperparameters["n_estimators"],
                max_depth=self.hyperparameters["max_depth"],
                learning_rate=self.hyperparameters["learning_rate"],
                random_state=self.hyperparameters["random_state"],
                objective="multiclass",
                metric="multi_logloss",
            )
        elif SKLEARN_AVAILABLE:
            model = GradientBoostingClassifier(
                n_estimators=self.hyperparameters["n_estimators"],
                max_depth=self.hyperparameters["max_depth"],
                learning_rate=self.hyperparameters["learning_rate"],
                random_state=self.hyperparameters["random_state"],
            )
        else:
            raise RuntimeError("No suitable ML library available.")

        return model

    def _prepare_features(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Prepare features for classification"""
        if isinstance(X, pd.DataFrame):
            X_processed = X.copy()

            # Handle categorical features
            for col in X_processed.select_dtypes(include=["object", "category"]):
                X_processed[col] = X_processed[col].astype("category").cat.codes

            # Fill missing values
            X_processed = X_processed.fillna(X_processed.mean())

            # Scale features
            if self.feature_scaler is None:
                self.feature_scaler = StandardScaler()
                X_scaled = self.feature_scaler.fit_transform(X_processed)
            else:
                X_scaled = self.feature_scaler.transform(X_processed)

            return X_scaled
        else:
            return X

    def _prepare_targets(self, y: Union[pd.Series, np.ndarray]) -> np.ndarray:
        """Prepare target variables for classification"""
        if self.label_encoder is None:
            self.label_encoder = LabelEncoder()
            y_encoded = self.label_encoder.fit_transform(y)
        else:
            y_encoded = self.label_encoder.transform(y)

        return y_encoded

    def get_policy_analysis(self, X: Union[pd.DataFrame, np.ndarray]) -> Dict[str, Any]:
        """Get policy effectiveness analysis with recommendations"""
        predictions, probabilities = self.predict_with_confidence(X)

        analysis = {
            "predictions": (
                predictions.tolist()
                if isinstance(predictions, np.ndarray)
                else predictions
            ),
            "probabilities": (
                probabilities.tolist()
                if isinstance(probabilities, np.ndarray)
                else probabilities
            ),
            "effectiveness_metrics": [],
            "improvement_suggestions": [],
        }

        # Analyze each policy
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            confidence = np.max(prob)

            # Effectiveness metrics
            metrics = {
                "overall_effectiveness": pred,
                "confidence": confidence,
                "success_probability": (
                    prob[2]
                    if pred == "Effective"
                    else prob[1] if pred == "Partially Effective" else prob[0]
                ),
                "risk_factors": [],
            }

            # Risk factors based on prediction
            if pred == "Ineffective":
                metrics["risk_factors"] = [
                    "Poor implementation strategy",
                    "Insufficient resources",
                    "Lack of stakeholder buy-in",
                    "Unrealistic timelines",
                ]
            elif pred == "Partially Effective":
                metrics["risk_factors"] = [
                    "Mixed stakeholder support",
                    "Resource constraints",
                    "Implementation delays",
                    "Scope creep",
                ]
            else:  # Effective
                metrics["risk_factors"] = [
                    "Strong stakeholder support",
                    "Adequate resources",
                    "Clear implementation plan",
                    "Regular monitoring",
                ]

            # Improvement suggestions
            if pred == "Ineffective":
                suggestions = [
                    "Revise implementation strategy",
                    "Increase resource allocation",
                    "Improve stakeholder communication",
                    "Set realistic milestones",
                ]
            elif pred == "Partially Effective":
                suggestions = [
                    "Address resource gaps",
                    "Strengthen stakeholder engagement",
                    "Streamline processes",
                    "Enhance monitoring",
                ]
            else:  # Effective
                suggestions = [
                    "Maintain current approach",
                    "Document best practices",
                    "Scale successful elements",
                    "Continuous improvement",
                ]

            analysis["effectiveness_metrics"].append(metrics)
            analysis["improvement_suggestions"].append(suggestions)

        return analysis


class IndustryVulnerabilityClassifier(BaseMLModel):
    """
    Multi-class classifier for predicting industry vulnerability to tariff impacts

    Predicts: High/Medium/Low vulnerability based on industry characteristics,
    trade dependencies, and economic resilience factors.
    """

    def __init__(self, model_id: str = "industry_vulnerability_classifier"):
        super().__init__(
            model_id=model_id,
            name="Industry Vulnerability Classifier",
            description="Multi-class classifier for predicting industry vulnerability to tariff impacts (High/Medium/Low)",
            model_type=ModelType.MULTI_CLASS,
        )

        # Model configuration
        self.class_labels = ["Low", "Medium", "High"]
        self.feature_scaler = None
        self.label_encoder = None

        # Hyperparameters
        self.hyperparameters = {
            "n_estimators": 200,
            "max_depth": 6,
            "learning_rate": 0.1,
            "random_state": 42,
        }

        logger.info(f"Initialized IndustryVulnerabilityClassifier: {model_id}")

    def _create_model(self):
        """Create the underlying ML model"""
        if XGBOOST_AVAILABLE:
            model = xgb.XGBClassifier(
                n_estimators=self.hyperparameters["n_estimators"],
                max_depth=self.hyperparameters["max_depth"],
                learning_rate=self.hyperparameters["learning_rate"],
                random_state=self.hyperparameters["random_state"],
                objective="multi:softprob",
                eval_metric="mlogloss",
            )
        elif LIGHTGBM_AVAILABLE:
            model = lgb.LGBMClassifier(
                n_estimators=self.hyperparameters["n_estimators"],
                max_depth=self.hyperparameters["max_depth"],
                learning_rate=self.hyperparameters["learning_rate"],
                random_state=self.hyperparameters["random_state"],
                objective="multiclass",
                metric="multi_logloss",
            )
        elif SKLEARN_AVAILABLE:
            model = RandomForestClassifier(
                n_estimators=self.hyperparameters["n_estimators"],
                max_depth=self.hyperparameters["max_depth"],
                random_state=self.hyperparameters["random_state"],
            )
        else:
            raise RuntimeError("No suitable ML library available.")

        return model

    def _prepare_features(self, X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
        """Prepare features for classification"""
        if isinstance(X, pd.DataFrame):
            X_processed = X.copy()

            # Handle categorical features
            for col in X_processed.select_dtypes(include=["object", "category"]):
                X_processed[col] = X_processed[col].astype("category").cat.codes

            # Fill missing values
            X_processed = X_processed.fillna(X_processed.mean())

            # Scale features
            if self.feature_scaler is None:
                self.feature_scaler = StandardScaler()
                X_scaled = self.feature_scaler.fit_transform(X_processed)
            else:
                X_scaled = self.feature_scaler.transform(X_processed)

            return X_scaled
        else:
            return X

    def _prepare_targets(self, y: Union[pd.Series, np.ndarray]) -> np.ndarray:
        """Prepare target variables for classification"""
        if self.label_encoder is None:
            self.label_encoder = LabelEncoder()
            y_encoded = self.label_encoder.fit_transform(y)
        else:
            y_encoded = self.label_encoder.transform(y)

        return y_encoded

    def get_vulnerability_assessment(
        self, X: Union[pd.DataFrame, np.ndarray]
    ) -> Dict[str, Any]:
        """Get industry vulnerability assessment with mitigation strategies"""
        predictions, probabilities = self.predict_with_confidence(X)

        assessment = {
            "predictions": (
                predictions.tolist()
                if isinstance(predictions, np.ndarray)
                else predictions
            ),
            "probabilities": (
                probabilities.tolist()
                if isinstance(probabilities, np.ndarray)
                else probabilities
            ),
            "vulnerability_factors": [],
            "mitigation_strategies": [],
            "resilience_indicators": [],
        }

        # Analyze each industry
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            confidence = np.max(prob)

            # Vulnerability factors
            if pred == "High":
                factors = [
                    "High import dependency",
                    "Limited domestic alternatives",
                    "Low profit margins",
                    "Concentrated supply chains",
                ]
            elif pred == "Medium":
                factors = [
                    "Moderate import dependency",
                    "Some domestic alternatives",
                    "Medium profit margins",
                    "Diversified supply chains",
                ]
            else:  # Low
                factors = [
                    "Low import dependency",
                    "Strong domestic alternatives",
                    "High profit margins",
                    "Resilient supply chains",
                ]

            # Mitigation strategies
            if pred == "High":
                strategies = [
                    "Diversify supply sources",
                    "Develop domestic capabilities",
                    "Implement cost controls",
                    "Seek policy exemptions",
                ]
            elif pred == "Medium":
                strategies = [
                    "Optimize supply chains",
                    "Enhance operational efficiency",
                    "Develop contingency plans",
                    "Monitor policy changes",
                ]
            else:  # Low
                strategies = [
                    "Maintain current advantages",
                    "Invest in innovation",
                    "Expand market presence",
                    "Leverage competitive position",
                ]

            # Resilience indicators
            resilience = {
                "financial_strength": (
                    "Weak"
                    if pred == "High"
                    else "Moderate" if pred == "Medium" else "Strong"
                ),
                "operational_flexibility": (
                    "Low"
                    if pred == "High"
                    else "Medium" if pred == "Medium" else "High"
                ),
                "market_position": (
                    "Vulnerable"
                    if pred == "High"
                    else "Stable" if pred == "Medium" else "Robust"
                ),
                "adaptation_capacity": (
                    "Limited"
                    if pred == "High"
                    else "Moderate" if pred == "Medium" else "High"
                ),
            }

            assessment["vulnerability_factors"].append(factors)
            assessment["mitigation_strategies"].append(strategies)
            assessment["resilience_indicators"].append(resilience)

        return assessment
