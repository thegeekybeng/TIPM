"""
Advanced Explainability Layer for TIPM
======================================

SHAP-based model explanation, feature importance analysis, and policy
insight generation for interpretable ML predictions.
"""

import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime
import numpy as np
import pandas as pd

# Explainability Libraries
try:
    import shap

    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    shap = None

# Base classes
from .base import BaseMLModel, ModelType, PredictionResult

logger = logging.getLogger(__name__)


class SHAPExplainer:
    """Advanced SHAP-based model explainer for TIPM"""

    def __init__(self, model: BaseMLModel):
        self.model = model
        self.explainer = None
        self.feature_names = None
        self.background_data = None

        logger.info(f"Initialized SHAPExplainer for model: {model.model_id}")

    def fit_explainer(
        self, X: Union[pd.DataFrame, np.ndarray], background_samples: int = 100
    ):
        """Fit the SHAP explainer to the data"""
        try:
            logger.info("Fitting SHAP explainer...")

            # Prepare data
            if isinstance(X, pd.DataFrame):
                self.feature_names = list(X.columns)
                X_array = X.values
            else:
                X_array = X
                self.feature_names = [f"feature_{i}" for i in range(X_array.shape[1])]

            # Select background samples
            if len(X_array) > background_samples:
                indices = np.random.choice(
                    len(X_array), background_samples, replace=False
                )
                self.background_data = X_array[indices]
            else:
                self.background_data = X_array

            # Create explainer
            if self.model.model_type in [
                ModelType.CLASSIFICATION,
                ModelType.MULTI_CLASS,
                ModelType.BINARY,
            ]:
                self.explainer = shap.KernelExplainer(
                    self._classification_predict_proba, self.background_data
                )
            else:
                self.explainer = shap.KernelExplainer(
                    self._regression_predict, self.background_data
                )

            logger.info("SHAP explainer fitted successfully")

        except Exception as e:
            logger.error(f"Failed to fit SHAP explainer: {e}")
            raise

    def _classification_predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Wrapper for classification probability prediction"""
        try:
            if hasattr(X, "shape") and len(X.shape) == 1:
                X = X.reshape(1, -1)

            pred_result = self.model.predict(X)

            if pred_result.probabilities is not None:
                return pred_result.probabilities
            else:
                predictions = pred_result.predictions
                unique_classes = np.unique(predictions)
                one_hot = np.zeros((len(predictions), len(unique_classes)))
                for i, pred in enumerate(predictions):
                    class_idx = np.where(unique_classes == pred)[0][0]
                    one_hot[i, class_idx] = 1.0
                return one_hot

        except Exception as e:
            logger.error(f"Classification prediction failed: {e}")
            return np.zeros((X.shape[0], 2))

    def _regression_predict(self, X: np.ndarray) -> np.ndarray:
        """Wrapper for regression prediction"""
        try:
            if hasattr(X, "shape") and len(X.shape) == 1:
                X = X.reshape(1, -1)

            pred_result = self.model.predict(X)
            return pred_result.predictions

        except Exception as e:
            logger.error(f"Regression prediction failed: {e}")
            return np.zeros(X.shape[0])

    def explain_prediction(self, X: Union[pd.DataFrame, np.ndarray]) -> Dict[str, Any]:
        """Explain a single prediction using SHAP"""
        if self.explainer is None:
            raise RuntimeError(
                "SHAP explainer must be fitted before explaining predictions"
            )

        try:
            if isinstance(X, pd.DataFrame):
                X_array = X.values
            else:
                X_array = X

            # Get SHAP values
            shap_values = self.explainer.shap_values(X_array)

            # Handle different SHAP output formats
            if isinstance(shap_values, list):
                shap_values = np.array(shap_values)
                if len(shap_values.shape) == 3:
                    shap_values = np.mean(shap_values, axis=0)

            # Create explanation
            explanation = {
                "shap_values": (
                    shap_values.tolist()
                    if isinstance(shap_values, np.ndarray)
                    else shap_values
                ),
                "feature_names": self.feature_names,
                "feature_importance": self._calculate_feature_importance(shap_values),
                "prediction_breakdown": self._create_prediction_breakdown(
                    X_array, shap_values
                ),
                "explanation_timestamp": datetime.now().isoformat(),
            }

            return explanation

        except Exception as e:
            logger.error(f"Failed to explain prediction: {e}")
            raise

    def _calculate_feature_importance(
        self, shap_values: np.ndarray
    ) -> Dict[str, float]:
        """Calculate feature importance from SHAP values"""
        if self.feature_names is None:
            return {}

        abs_shap = np.abs(shap_values)

        importance_dict = {}
        for i, feature_name in enumerate(self.feature_names):
            if i < len(abs_shap):
                importance_dict[feature_name] = float(abs_shap[i])

        sorted_importance = dict(
            sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
        )
        return sorted_importance

    def _create_prediction_breakdown(
        self, features: np.ndarray, shap_values: np.ndarray
    ) -> List[Dict[str, Any]]:
        """Create detailed breakdown of how each feature contributes to the prediction"""
        breakdown = []

        if self.feature_names is None:
            return breakdown

        for i, feature_name in enumerate(self.feature_names):
            if i < len(features) and i < len(shap_values):
                feature_contribution = {
                    "feature_name": feature_name,
                    "feature_value": float(features[i]),
                    "shap_value": float(shap_values[i]),
                    "contribution_type": (
                        "positive" if shap_values[i] > 0 else "negative"
                    ),
                    "contribution_magnitude": abs(float(shap_values[i])),
                }
                breakdown.append(feature_contribution)

        breakdown.sort(key=lambda x: x["contribution_magnitude"], reverse=True)
        return breakdown


class PolicyInsightGenerator:
    """Generate policy insights from ML model explanations"""

    def __init__(self, model: BaseMLModel):
        self.model = model
        self.feature_categories = self._initialize_feature_categories()

        logger.info(f"Initialized PolicyInsightGenerator for model: {model.model_id}")

    def _initialize_feature_categories(self) -> Dict[str, List[str]]:
        """Initialize feature categories for policy analysis"""
        return {
            "economic_indicators": [
                "gdp",
                "inflation",
                "unemployment",
                "interest_rate",
                "exchange_rate",
                "trade_balance",
                "current_account",
                "fiscal_deficit",
            ],
            "trade_policy": [
                "tariff_rate",
                "import_quota",
                "export_subsidy",
                "trade_agreement",
                "sanctions",
                "embargo",
                "trade_partner",
            ],
            "geopolitical": [
                "political_stability",
                "regime_type",
                "alliance_membership",
                "conflict_status",
                "diplomatic_relations",
            ],
            "market_conditions": [
                "market_volatility",
                "commodity_prices",
                "supply_chain_disruption",
                "demand_shock",
                "capacity_utilization",
            ],
            "regulatory": [
                "regulatory_burden",
                "compliance_cost",
                "policy_uncertainty",
                "regulatory_change",
                "enforcement_level",
            ],
        }

    def generate_policy_insights(
        self, explanation: Dict[str, Any], context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Generate policy insights from model explanation"""
        try:
            logger.info("Generating policy insights...")

            feature_importance = explanation.get("feature_importance", {})
            prediction_breakdown = explanation.get("prediction_breakdown", [])

            insights = {
                "key_drivers": self._identify_key_drivers(feature_importance),
                "policy_levers": self._identify_policy_levers(feature_importance),
                "risk_factors": self._identify_risk_factors(prediction_breakdown),
                "opportunity_areas": self._identify_opportunity_areas(
                    prediction_breakdown
                ),
                "policy_recommendations": self._generate_policy_recommendations(
                    feature_importance, prediction_breakdown, context
                ),
                "monitoring_priorities": self._identify_monitoring_priorities(
                    feature_importance
                ),
                "insight_timestamp": datetime.now().isoformat(),
            }

            logger.info("Policy insights generated successfully")
            return insights

        except Exception as e:
            logger.error(f"Failed to generate policy insights: {e}")
            raise

    def _identify_key_drivers(
        self, feature_importance: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Identify key drivers of the prediction"""
        key_drivers = []

        sorted_features = sorted(
            feature_importance.items(), key=lambda x: x[1], reverse=True
        )
        top_features = sorted_features[:5]

        for feature_name, importance_score in top_features:
            category = self._categorize_feature(feature_name)
            driver_info = {
                "feature_name": feature_name,
                "importance_score": importance_score,
                "category": category,
                "policy_relevance": self._assess_policy_relevance(
                    feature_name, category
                ),
                "interpretation": self._interpret_feature_importance(
                    feature_name, importance_score
                ),
            }
            key_drivers.append(driver_info)

        return key_drivers

    def _identify_policy_levers(
        self, feature_importance: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Identify features that can be influenced by policy"""
        policy_levers = []

        for feature_name, importance_score in feature_importance.items():
            if self._is_policy_controllable(feature_name):
                lever_info = {
                    "feature_name": feature_name,
                    "importance_score": importance_score,
                    "policy_category": self._categorize_feature(feature_name),
                    "controllability": self._assess_controllability(feature_name),
                    "expected_impact": self._estimate_policy_impact(
                        feature_name, importance_score
                    ),
                }
                policy_levers.append(lever_info)

        policy_levers.sort(key=lambda x: x["expected_impact"], reverse=True)
        return policy_levers

    def _identify_risk_factors(
        self, prediction_breakdown: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify risk factors from prediction breakdown"""
        risk_factors = []

        for breakdown in prediction_breakdown:
            feature_name = breakdown.get("feature_name", "")
            shap_value = breakdown.get("shap_value", 0.0)
            contribution_type = breakdown.get("contribution_type", "neutral")

            if contribution_type == "negative" and abs(shap_value) > 0.1:
                risk_info = {
                    "feature_name": feature_name,
                    "risk_level": self._assess_risk_level(abs(shap_value)),
                    "contribution_magnitude": abs(shap_value),
                    "mitigation_strategies": self._suggest_mitigation_strategies(
                        feature_name
                    ),
                    "monitoring_priority": (
                        "high" if abs(shap_value) > 0.5 else "medium"
                    ),
                }
                risk_factors.append(risk_info)

        risk_factors.sort(key=lambda x: x["contribution_magnitude"], reverse=True)
        return risk_factors

    def _identify_opportunity_areas(
        self, prediction_breakdown: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify opportunity areas from prediction breakdown"""
        opportunities = []

        for breakdown in prediction_breakdown:
            feature_name = breakdown.get("feature_name", "")
            shap_value = breakdown.get("shap_value", 0.0)
            contribution_type = breakdown.get("contribution_type", "neutral")

            if contribution_type == "positive" and abs(shap_value) > 0.1:
                opportunity_info = {
                    "feature_name": feature_name,
                    "opportunity_level": self._assess_opportunity_level(
                        abs(shap_value)
                    ),
                    "contribution_magnitude": abs(shap_value),
                    "leverage_strategies": self._suggest_leverage_strategies(
                        feature_name
                    ),
                    "priority": "high" if abs(shap_value) > 0.5 else "medium",
                }
                opportunities.append(opportunity_info)

        opportunities.sort(key=lambda x: x["contribution_magnitude"], reverse=True)
        return opportunities

    def _generate_policy_recommendations(
        self,
        feature_importance: Dict[str, float],
        prediction_breakdown: List[Dict[str, Any]],
        context: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:
        """Generate specific policy recommendations"""
        recommendations = []

        sorted_features = sorted(
            feature_importance.items(), key=lambda x: x[1], reverse=True
        )

        for feature_name, importance_score in sorted_features[:10]:
            if self._is_policy_controllable(feature_name):
                recommendation = {
                    "feature_name": feature_name,
                    "importance_score": importance_score,
                    "recommendation_type": self._determine_recommendation_type(
                        feature_name, importance_score
                    ),
                    "specific_action": self._suggest_specific_action(
                        feature_name, importance_score
                    ),
                    "expected_outcome": self._predict_policy_outcome(
                        feature_name, importance_score
                    ),
                    "implementation_timeline": self._suggest_implementation_timeline(
                        feature_name
                    ),
                }
                recommendations.append(recommendation)

        recommendations.sort(key=lambda x: x["expected_outcome"], reverse=True)
        return recommendations

    def _categorize_feature(self, feature_name: str) -> str:
        """Categorize a feature based on its name and context"""
        feature_lower = feature_name.lower()

        for category, keywords in self.feature_categories.items():
            if any(keyword in feature_lower for keyword in keywords):
                return category

        return "other"

    def _assess_policy_relevance(self, feature_name: str, category: str) -> str:
        """Assess the policy relevance of a feature"""
        high_relevance_categories = ["trade_policy", "regulatory", "fiscal_policy"]
        medium_relevance_categories = ["economic_indicators", "market_conditions"]

        if category in high_relevance_categories:
            return "high"
        elif category in medium_relevance_categories:
            return "medium"
        else:
            return "low"

    def _is_policy_controllable(self, feature_name: str) -> bool:
        """Determine if a feature can be influenced by policy"""
        controllable_keywords = [
            "tariff",
            "quota",
            "subsidy",
            "tax",
            "regulation",
            "policy",
            "agreement",
            "sanction",
            "embargo",
            "incentive",
            "restriction",
        ]

        feature_lower = feature_name.lower()
        return any(keyword in feature_lower for keyword in controllable_keywords)

    def _assess_controllability(self, feature_name: str) -> str:
        """Assess the degree of policy controllability"""
        if "tariff" in feature_name.lower():
            return "high"
        elif "regulation" in feature_name.lower():
            return "medium"
        else:
            return "low"

    def _estimate_policy_impact(
        self, feature_name: str, importance_score: float
    ) -> float:
        """Estimate the expected impact of policy intervention"""
        base_impact = importance_score

        controllability = self._assess_controllability(feature_name)
        if controllability == "high":
            controllability_multiplier = 1.0
        elif controllability == "medium":
            controllability_multiplier = 0.7
        else:
            controllability_multiplier = 0.3

        return base_impact * controllability_multiplier

    def _assess_risk_level(self, contribution_magnitude: float) -> str:
        """Assess the risk level based on contribution magnitude"""
        if contribution_magnitude > 0.5:
            return "high"
        elif contribution_magnitude > 0.2:
            return "medium"
        else:
            return "low"

    def _assess_opportunity_level(self, contribution_magnitude: float) -> str:
        """Assess the opportunity level based on contribution magnitude"""
        if contribution_magnitude > 0.5:
            return "high"
        elif contribution_magnitude > 0.2:
            return "medium"
        else:
            return "low"

    def _suggest_mitigation_strategies(self, feature_name: str) -> List[str]:
        """Suggest strategies to mitigate risks"""
        strategies = []

        if "tariff" in feature_name.lower():
            strategies.extend(
                [
                    "Diversify supply sources",
                    "Negotiate trade agreements",
                    "Implement tariff exemptions",
                    "Develop domestic alternatives",
                ]
            )
        elif "regulation" in feature_name.lower():
            strategies.extend(
                [
                    "Engage in regulatory dialogue",
                    "Prepare compliance frameworks",
                    "Seek regulatory clarity",
                    "Develop compliance monitoring",
                ]
            )
        else:
            strategies.append("Monitor and assess impact")

        return strategies

    def _suggest_leverage_strategies(self, feature_name: str) -> List[str]:
        """Suggest strategies to leverage opportunities"""
        strategies = []

        if "tariff" in feature_name.lower():
            strategies.extend(
                [
                    "Expand market access",
                    "Strengthen trade relationships",
                    "Develop export capabilities",
                    "Leverage competitive advantages",
                ]
            )
        elif "regulation" in feature_name.lower():
            strategies.extend(
                [
                    "Advocate for favorable policies",
                    "Demonstrate compliance leadership",
                    "Participate in policy development",
                    "Build regulatory expertise",
                ]
            )
        else:
            strategies.append("Monitor and capitalize on trends")

        return strategies

    def _determine_recommendation_type(
        self, feature_name: str, importance_score: float
    ) -> str:
        """Determine the type of policy recommendation"""
        if importance_score > 0.5:
            return "immediate_action"
        elif importance_score > 0.2:
            return "strategic_planning"
        else:
            return "monitoring"

    def _suggest_specific_action(
        self, feature_name: str, importance_score: float
    ) -> str:
        """Suggest specific actions for policy implementation"""
        if "tariff" in feature_name.lower():
            if importance_score > 0.5:
                return "Review and adjust tariff rates within 30 days"
            else:
                return "Monitor tariff impacts and prepare adjustment framework"
        elif "regulation" in feature_name.lower():
            if importance_score > 0.5:
                return "Initiate regulatory review process immediately"
            else:
                return "Assess regulatory impact and develop response strategy"
        else:
            return "Conduct detailed analysis and develop targeted intervention"

    def _predict_policy_outcome(
        self, feature_name: str, importance_score: float
    ) -> str:
        """Predict the expected outcome of policy intervention"""
        if importance_score > 0.5:
            return "Significant positive impact expected"
        elif importance_score > 0.2:
            return "Moderate positive impact expected"
        else:
            return "Limited impact expected"

    def _suggest_implementation_timeline(self, feature_name: str) -> str:
        """Suggest implementation timeline for policy changes"""
        if "tariff" in feature_name.lower():
            return "30-90 days"
        elif "regulation" in feature_name.lower():
            return "6-18 months"
        else:
            return "3-12 months"

    def _identify_monitoring_priorities(
        self, feature_importance: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Identify monitoring priorities based on feature importance"""
        monitoring_priorities = []

        sorted_features = sorted(
            feature_importance.items(), key=lambda x: x[1], reverse=True
        )
        top_features = sorted_features[:10]

        for feature_name, importance_score in top_features:
            priority_info = {
                "feature_name": feature_name,
                "importance_score": importance_score,
                "monitoring_frequency": self._determine_monitoring_frequency(
                    importance_score
                ),
                "alert_thresholds": self._suggest_alert_thresholds(importance_score),
                "data_sources": self._suggest_data_sources(feature_name),
            }
            monitoring_priorities.append(priority_info)

        return monitoring_priorities

    def _determine_monitoring_frequency(self, importance_score: float) -> str:
        """Determine monitoring frequency based on importance"""
        if importance_score > 0.5:
            return "daily"
        elif importance_score > 0.2:
            return "weekly"
        else:
            return "monthly"

    def _suggest_alert_thresholds(self, importance_score: float) -> Dict[str, float]:
        """Suggest alert thresholds for monitoring"""
        if importance_score > 0.5:
            return {"warning": 0.1, "critical": 0.3}
        elif importance_score > 0.2:
            return {"warning": 0.2, "critical": 0.4}
        else:
            return {"warning": 0.3, "critical": 0.5}

    def _suggest_data_sources(self, feature_name: str) -> List[str]:
        """Suggest data sources for monitoring"""
        if "tariff" in feature_name.lower():
            return ["Customs data", "Trade statistics", "Industry reports"]
        elif "regulation" in feature_name.lower():
            return [
                "Regulatory databases",
                "Policy announcements",
                "Compliance reports",
            ]
        else:
            return ["Economic indicators", "Market data", "Industry surveys"]

    def _interpret_feature_importance(
        self, feature_name: str, importance_score: float
    ) -> str:
        """Provide interpretation of feature importance"""
        if importance_score > 0.5:
            return f"{feature_name} is a critical driver requiring immediate attention"
        elif importance_score > 0.2:
            return f"{feature_name} is an important factor that should be monitored closely"
        else:
            return f"{feature_name} has limited impact but should be tracked for trends"
